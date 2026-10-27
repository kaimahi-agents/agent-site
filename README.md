# kmx site

Static HTML/CSS marketing site for [kmx](https://github.com/kaimahi-agents/kaimahi)
at [agent.kaimahi.dev](https://agent.kaimahi.dev). No framework or build step.

## Preview and tests

From the repository root:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Open <http://127.0.0.1:8765>. Run the checks separately:

```sh
python3 -m unittest discover -s tests -v
```

## Publishing

GitHub Pages serves the root of `main`. `.nojekyll` disables Jekyll processing;
`CNAME` names `agent.kaimahi.dev`. Deployment settings and DNS are maintainer-owned.

The visible `[VERSION]` placeholder is intentionally unreleased. The “What's
next” cards mark future work as in progress or planned, not released features.

[Contributing](CONTRIBUTING.md) · [Code of conduct](CODE_OF_CONDUCT.md) ·
[Security reporting](SECURITY.md) · [MIT license](LICENSE)
