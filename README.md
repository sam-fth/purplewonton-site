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
| `i18n/` | The words of every page, one file per language: `en.json` (English), `de.json` (German), `fr.json` (French), `ja.json` (Japanese), `es.json` (Spanish) |
| `de/`, `fr/`, `ja/`, `es/` | The pages in each language (English pages are at the top level) |
| `build.py` | Makes every page in every language from shared templates, plus the sitemap with Google's language tags. Run `python3 build.py` after any change |
| `CNAME` | Tells GitHub Pages the site lives at www.purplewonton.com |

## Updating the site

1. Change wording in `i18n/*.json` (update every language), settings at the top
   of `build.py` (Chrome Web Store link, price, India price), or `content/`.
   To add a language: copy `i18n/en.json`, translate it, and add it to
   `LANGUAGES` in `build.py`.
2. Run `python3 build.py` (needs Python 3 and the `markdown` package).
3. Commit and push. GitHub Pages publishes the change within a minute or two.

The privacy policy and terms are in English only; translated pages say the
English version is the official one.

No fonts, scripts or trackers are loaded from other companies, so visiting the
site sends nothing to third parties.
