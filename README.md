# purplewonton.com

The public website of Purple Wonton, a small software studio in Bengaluru,
and its first product, DupTabOff (a Chrome extension that removes duplicate tabs).

This repository holds **only the website pages**. The extension's code is kept
in a separate private repository, and no personal details are stored here.

## What's here

| Path | What it is |
| --- | --- |
| `index.html` | Home page: Purple Wonton and DupTabOff |
| `duptaboff/` | The DupTabOff product page (screenshots, Free vs Lifetime Pro, questions) |
| `support/` | Contact, license keys, refunds |
| `privacy/`, `terms/` | Privacy policy and terms (made from `content/PRIVACY.md` and `content/TERMS.md`) |
| `assets/` | The stylesheet (`site.css`), logo, icons and screenshots |
| `build.py` | Makes every page from shared templates. Edit it (or the files in `content/`), then run `python3 build.py` |
| `CNAME` | Tells GitHub Pages the site lives at www.purplewonton.com |

## Updating the site

1. Change the text in `build.py` (the SETTINGS section has the Chrome Web Store
   link, price and India price) or in `content/`.
2. Run `python3 build.py` (needs Python 3 and the `markdown` package).
3. Commit and push. GitHub Pages publishes the change within a minute or two.

No fonts, scripts or trackers are loaded from other companies, so visiting the
site sends nothing to third parties.
