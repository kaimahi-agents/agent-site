# Contributing to the kmx site

This repository contains the static marketing site for kmx. Focus contributions
on fixes, documentation corrections, accessibility, and small, well-tested changes.
Start with the organization
[contribution expectations](https://github.com/kaimahi-agents/.github/blob/main/CONTRIBUTING.md)
and follow the [Microsoft Open Source Code of Conduct](CODE_OF_CONDUCT.md).

## Local development

The site uses plain HTML and CSS, with no framework or build step. From the
repository root, start a local preview:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Open <http://127.0.0.1:8765>. Check changes at desktop and phone widths, including
image alt text, keyboard navigation, and links.

Run the site checks:

```sh
python3 -m unittest discover -s tests -v
```

## Pull requests

- Keep each pull request focused on a user problem.
- List exact verification commands and results.
- Distinguish what you verified directly from what you inferred.
- Keep the page's product claims consistent with what has shipped.
- Never include credentials, tokens, private endpoints, tenant identifiers,
  or unsanitized user data.

Changes land through pull requests. Deployment settings and DNS are maintained
by the maintainers; see the [README](README.md).
