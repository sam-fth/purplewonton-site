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
| `prycehunt/` | The PryceHunt product page (English only for now): screenshots, privacy summary, questions. Its menu entries and home-page card appear in every language, in English, and link to this page |
| `support/` | Contact, license keys, refunds |
| `privacy/`, `terms/` | Privacy policy and terms (made from `content/PRIVACY.md` and `content/TERMS.md`) |
| `assets/` | The stylesheet (`site.css`), logo and icons |
| `assets/shots/` | DupTabOff screenshots, one set per language: English at the top, then `de/`, `fr/`, `ja/`, `es/`. `sizes.json` lists each picture's size. Copied here automatically from the extension's repository; don't edit them by hand |
| `assets/shots/prycehunt/` | PryceHunt screenshots (six, 1280 x 800), copied from the `store/screenshots` folder of the PryceHunt repository and converted to WebP; `sizes.json` lists their sizes. `assets/prycehunt-icon.png` and `assets/og-prycehunt.jpg` (the link-preview picture) belong to it too |
| `i18n/` | The words of every page, one file per language: `en.json` (English), `de.json` (German), `fr.json` (French), `ja.json` (Japanese), `es.json` (Spanish) |
| `de/`, `fr/`, `ja/`, `es/` | The pages in each language (English pages are at the top level) |
| `build.py` | Makes every page in every language from shared templates, plus the sitemap with Google's language tags. Run `python3 build.py` after any change |
| `CNAME` | Tells GitHub Pages the site lives at www.purplewonton.com |

## Updating the site

1. Change wording in `i18n/*.json` (update every language), settings at the top
   of `build.py` (Chrome Web Store links for DupTabOff and PryceHunt, price, India price), or `content/`.
   The PryceHunt wording (keys starting `pw_`) exists in English only for now; the other language files
   fall back to it automatically until someone translates it.
   To add a language: copy `i18n/en.json`, translate it, and add it to
   `LANGUAGES` in `build.py`.
2. Run `python3 build.py` (needs Python 3 and the `markdown` package).
3. Commit and push. GitHub Pages publishes the change within a minute or two.

## When the DupTabOff pictures change

The screenshots are made in the extension's (private) repository and copied
here, picture files only:

1. In the extension repository: `node tools/store-shots.js <language>` for each
   language, then `python3 tools/sync-site-images.py`. That copies the pictures
   into `assets/shots/` here (one folder per language) and writes `sizes.json`.
2. Here: `python3 build.py`. Each language's pages pick their own pictures
   (English if a language has none yet), and each picture address gets a short
   fingerprint (`light.webp?v=1a2b3c4d`) so visitors see the new picture right
   away and the sitemap tells Google the page changed.
3. Commit and push.

The privacy policy and terms are in English only; translated pages say the
English version is the official one.

No fonts, scripts or trackers are loaded from other companies, so visiting the
site sends nothing to third parties.

## When PryceHunt changes

Its page uses the pictures in `assets/shots/prycehunt/`. To refresh them, run `npm run store-assets` in the PryceHunt
repository, convert the six PNGs in its `store/screenshots` to WebP (quality 84) into that folder, update `sizes.json`,
then run `python3 build.py`. When PryceHunt is published, paste its Chrome Web Store address into `PRYCEHUNT_STORE_URL`
at the top of `build.py` and rebuild: the "Coming soon" button becomes "Add to Chrome".

