"""Dependency-free checks for the landing page's static contract."""
import re
import struct
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.elements = []
        self.text = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))

    def handle_data(self, data):
        self.text.append(data)

    def attrs(self, tag):
        return [attrs for name, attrs in self.elements if name == tag]


class SiteTests(unittest.TestCase):
    def setUp(self):
        self.source = (ROOT / 'index.html').read_text()
        self.doc = Document(self.source)

    def test_document_and_navigation(self):
        self.assertTrue(self.source.lower().startswith('<!doctype html>'))
        self.assertEqual(self.doc.attrs('html')[0]['lang'], 'en')
        self.assertEqual(len(self.doc.attrs('h1')), 1)
        self.assertTrue(self.doc.attrs('title'))
        self.assertIn('width=device-width', next(
            a['content'] for a in self.doc.attrs('meta') if a.get('name') == 'viewport'))
        ids = [a['id'] for _, a in self.doc.elements if 'id' in a]
        self.assertEqual(len(ids), len(set(ids)))
        for a in self.doc.attrs('a'):
            href = a['href']
            if href.startswith('#'):
                self.assertIn(href[1:], ids)
        self.assertTrue(self.doc.attrs('main'))

    def test_truth_and_public_links(self):
        text = ' '.join(self.doc.text)
        self.assertIn('Unit tests for your agent\'s prompt.', text)
        self.assertIn('[VERSION]', text)
        self.assertNotIn('The same file in your terminal and CI', text)
        self.assertNotIn('kmx test release-notes.agent.md', text)
        self.assertNotIn('AFTER THE CLI', text)
        links = [a['href'] for a in self.doc.attrs('a')]
        self.assertIn('https://github.com/kaimahi-agents/kaimahi', links)
        self.assertIn('https://kaimahi.dev/docs/suite-workspace', links)

    def test_images_are_local_accessible_and_dimensioned(self):
        images = self.doc.attrs('img')
        self.assertEqual(len(images), 2)
        for image in images:
            with self.subTest(src=image['src']):
                self.assertTrue(image.get('alt', '').strip())
                self.assertFalse(urlsplit(image['src']).scheme)
                data = (ROOT / image['src']).read_bytes()
                self.assertEqual(data[:8], b'\x89PNG\r\n\x1a\n')
                width, height = struct.unpack('>II', data[16:24])
                self.assertEqual((int(image['width']), int(image['height'])), (width, height))

    def test_no_artifact_runtime_or_private_text(self):
        self.assertFalse(self.doc.attrs('script'))
        for marker in ('{{', '}}', '/_blob/', 'x-dc', 'support.js', 'DCLogic'):
            self.assertNotIn(marker, self.source)
        public_text = self.source + (ROOT / 'styles.css').read_text()
        self.assertIsNone(re.search(r'(?i)\bW\d{3}\b|/home/|C:\\', public_text))

    def test_installer_path_and_model_access(self):
        self.assertIn('--version=[VERSION] --bin-dir=/usr/local/bin', self.source)
        self.assertIn('https://kaimahi.dev/docs/copilot-app#check-model-access',
                      [a['href'] for a in self.doc.attrs('a')])
        self.assertIn('Sign in separately for', ' '.join(self.doc.text))

    def test_platform_plugin_instructions(self):
        snippets = ['Windows terminal (not WSL)',
                    'copilot plugin install kmx-agent-builder@kmx-plugins',
                    'macOS terminal</p>',
                    'copilot plugin install kmx-agent-builder-path@kmx-plugins']
        for snippet in snippets:
            self.assertIn(snippet, self.source)
        positions = [self.source.index(snippet) for snippet in snippets]
        self.assertEqual(positions, sorted(positions))
        self.assertEqual(self.source.count('copilot plugin marketplace add '), 2)

    def test_recorded_tools_are_an_explicit_choice(self):
        text = ' '.join(self.doc.text)
        self.assertIn("Choose Recorded for a test's tool", text)
        self.assertIn('Live tools run every time.', text)
        self.assertNotIn('The first run calls the real tool and saves the result.', text)

    def test_commands_wrap_without_hiding_text(self):
        css = (ROOT / 'styles.css').read_text()
        match = re.search(r'\npre \{([^}]+)\}', css)
        assert match is not None, 'Expected a pre rule for command blocks'
        pre_rule = match.group(1)
        self.assertIn('white-space: pre-wrap;', pre_rule)
        self.assertIn('overflow-wrap: anywhere;', pre_rule)

    def test_css_and_pages_contract(self):
        stylesheets = [a['href'] for a in self.doc.attrs('link')
                       if a.get('rel') == 'stylesheet']
        self.assertIn('styles.css', stylesheets)
        self.assertTrue((ROOT / 'styles.css').read_text().strip())
        self.assertTrue(any('IBM+Plex+Sans' in url and 'IBM+Plex+Mono' in url
                            for url in stylesheets))
        self.assertEqual((ROOT / 'CNAME').read_text(), 'agent.kaimahi.dev\n')
        self.assertEqual((ROOT / '.nojekyll').read_bytes(), b'')


if __name__ == '__main__':
    unittest.main()
