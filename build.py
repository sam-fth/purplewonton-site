"""
build.py: MAKES EVERY PAGE OF PURPLEWONTON.COM, IN EVERY LANGUAGE

In plain words:
  Every page shares the same header (logo, menu, language menu) and footer.
  This script writes all the pages from the templates below, once per language,
  so a change to a template happens on every page in every language at once.

  The WORDS live in the i18n/ folder, one file per language:
      i18n/en.json  English (the original)     i18n/de.json  German
      i18n/fr.json  French                     i18n/ja.json  Japanese
      i18n/es.json  Spanish
  To change wording, edit those files (keep the {words in brackets} as they are).
  To add a language, copy en.json to a new file (e.g. pt.json), translate it,
  and add it to LANGUAGES below.

  English pages are at the top of the site (purplewonton.com/duptaboff/);
  other languages have their own folder (purplewonton.com/de/duptaboff/), so
  Google can show each visitor the page in their language.

  The privacy policy and terms are English only (made from content/PRIVACY.md and
  content/TERMS.md); other languages link to them with a note that the English
  version is the official one.

How to use it:
  1. Change wording in i18n/*.json, or settings below.
  2. Run:  python3 build.py     (needs Python 3 and the "markdown" package)
  3. Commit and push. GitHub Pages publishes the new pages within a minute or two.
"""
import datetime
import hashlib
import html
import json
import os
import re

import markdown  # turns the .md text files into web page text

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------------------------
SITE = 'https://www.purplewonton.com'
SUPPORT_EMAIL = 'support@purplewonton.com'
# Paste the Chrome Web Store address here once DupTabOff is published.
# While it's empty, the button says "Coming soon to the Chrome Web Store".
CHROME_STORE_URL = ''
PRICE = '$4.99'
# Set to '₹199' once the India discount code exists in Gumroad; empty hides the line.
INDIA_PRICE = ''
YEAR = '2026'

# Languages, in the order they appear in the language menu.
# (code, folder): English lives at the top of the site; the others in a folder.
LANGUAGES = [('en', ''), ('de', 'de/'), ('fr', 'fr/'), ('ja', 'ja/'), ('es', 'es/')]

# The pages that exist in every language (folder names, '' is the home page).
TRANSLATED_PAGES = ['', 'duptaboff/', 'support/']

# Load every language's words.
T = {}
for code, _ in LANGUAGES:
    with open(os.path.join(ROOT, 'i18n', code + '.json'), encoding='utf-8') as f:
        T[code] = json.load(f)


def strip_tags(text):
    """Plain text without HTML tags (for page titles, descriptions and picture descriptions)."""
    return re.sub(r'<[^>]+>', '', text)


def attr(text):
    """Make text safe to put inside an HTML attribute like alt="..." or content="..."."""
    return html.escape(strip_tags(text), quote=True)


class Words:
    """The words for one language. w['key'] fills in {price}, {email} and the other
    placeholders automatically, so templates stay short."""

    def __init__(self, code, values):
        self.code = code
        self.v = values
        self.vars = {}

    def __getitem__(self, key):
        return self.fill(self.v.get(key, T['en'][key]))

    def fill(self, value):
        if isinstance(value, list):
            return [self.fill(x) for x in value]
        out = value
        for name, val in self.vars.items():
            out = out.replace('{' + name + '}', val)
        return out


def url_of(code, rel):
    """Full web address of a page in a language, e.g. ('de', 'duptaboff/')."""
    prefix = dict(LANGUAGES)[code]
    return SITE + '/' + prefix + rel


def page(code, rel, title, description, body, nav='', jsonld=None, translated=True):
    """Wrap a page's content in the shared header and footer, then save it.

    code:        language code ('en', 'de', ...)
    rel:         the page's folder ('' for home, 'duptaboff/', 'support/', ...)
    title:       text in the browser tab and in search results
    description: short summary shown by search engines and link previews
    body:        the page's own content
    nav:         which menu item to show as "you are here"
    jsonld:      facts for Google ("structured data"), invisible to visitors
    translated:  False for English-only pages (privacy, terms): no language menu entries
    """
    w = Words(code, T[code])
    prefix = dict(LANGUAGES)[code]
    path = prefix + rel + 'index.html' if rel != '404.html' else '404.html'
    depth = path.count('/')
    up = '../' * depth            # from this page back to the top of the site
    home = up + prefix            # this language's home page
    url = url_of(code, rel)

    def cur(name):
        return ' aria-current="page"' if nav == name else ''

    # Tell Google which pages are translations of each other ("hreflang").
    alternates = ''
    lang_menu = ''
    if translated:
        alternates = '\n'.join(
            f'<link rel="alternate" hreflang="{c}" href="{url_of(c, rel)}">' for c, _ in LANGUAGES)
        alternates += f'\n<link rel="alternate" hreflang="x-default" href="{url_of("en", rel)}">'
        items = '\n'.join(
            f'        <li><a href="{up}{p}{rel}" hreflang="{c}" lang="{c}"'
            + (' aria-current="true"' if c == code else '') + f'>{T[c]["lang_name"]}</a></li>'
            for c, p in LANGUAGES)
        # A menu that opens and closes without any script (<details>).
        lang_menu = f'''
    <details class="lang">
      <summary aria-label="{attr(w["lang_label"])}"><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 1.8a8.2 8.2 0 1 0 0 16.4 8.2 8.2 0 0 0 0-16.4Zm5.9 7.4h-2.6a13 13 0 0 0-1.1-5 6.6 6.6 0 0 1 3.7 5ZM10 3.4c.7.9 1.5 2.9 1.7 5.8H8.3c.2-2.9 1-4.9 1.7-5.8Zm-2.2.8a13 13 0 0 0-1.1 5H4.1a6.6 6.6 0 0 1 3.7-5Zm-3.7 6.6h2.6a13 13 0 0 0 1.1 5 6.6 6.6 0 0 1-3.7-5Zm5.9 5.8c-.7-.9-1.5-2.9-1.7-5.8h3.4c-.2 2.9-1 4.9-1.7 5.8Zm2.2-.8a13 13 0 0 0 1.1-5h2.6a6.6 6.6 0 0 1-3.7 5Z"/></svg><span>{T[code]["lang_name"]}</span></summary>
      <ul>
{items}
      </ul>
    </details>'''

    ld = ''
    if jsonld:
        ld = '<script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False) + '</script>'

    legal = ''
    if w['legal_note']:
        legal = f'\n  <div class="wrap legal-note">{w["legal_note"]}</div>'

    doc = f'''<!doctype html>
<html lang="{code}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{attr(title)}</title>
<meta name="description" content="{attr(description)}">
<link rel="canonical" href="{url}">
{alternates}
<link rel="icon" href="{up}assets/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="{up}assets/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:title" content="{attr(title)}">
<meta property="og:description" content="{attr(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og-duptaboff.jpg">
<meta property="og:site_name" content="Purple Wonton">
<meta property="og:locale" content="{T[code]["locale"]}">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="#7140e0">
{ld}
<link rel="stylesheet" href="{up}assets/site.css">
</head>
<body>
<a class="skip" href="#main">{w["skip"]}</a>
<header class="site-head">
  <div class="wrap">
    <a class="brand" href="{home}"><img src="{up}assets/mark.png" width="36" height="36" alt=""><span>Purple Wonton</span></a>
    <div class="head-right">
      <nav class="nav" aria-label="Main">
        <a href="{home}#products"{cur('products')}>{w["nav_products"]}</a>
        <a href="{home}duptaboff/"{cur('duptaboff')}>DupTabOff</a>
        <a href="{home}support/"{cur('support')}>{w["nav_support"]}</a>
      </nav>{lang_menu}
    </div>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-foot">{legal}
  <div class="wrap">
    <span>{w["footer_copy"].replace("{year}", YEAR)}</span>
    <nav aria-label="Footer">
      <a href="{home}duptaboff/">DupTabOff</a>
      <a href="{home}support/">{w["nav_support"]}</a>
      <a href="{up}privacy/">{w["footer_privacy"]}</a>
      <a href="{up}terms/">{w["footer_terms"]}</a>
      <a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a>
    </nav>
  </div>
</footer>
</body>
</html>
'''
    out = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(out) or ROOT, exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(doc)
    print('wrote', path)


def org(w):
    """Facts about Purple Wonton for Google (an "Organization")."""
    return {
        '@type': 'Organization', '@id': SITE + '/#org', 'name': 'Purple Wonton', 'url': SITE + '/',
        'logo': SITE + '/assets/mark.png', 'email': SUPPORT_EMAIL, 'description': w['org_desc'],
        'address': {'@type': 'PostalAddress', 'addressLocality': 'Bengaluru', 'addressRegion': 'Karnataka', 'addressCountry': 'IN'},
    }


def store_button(w):
    """The "Add to Chrome" button. Before the store link exists it says "coming soon"."""
    if CHROME_STORE_URL:
        return f'<a class="btn" href="{CHROME_STORE_URL}" rel="noopener">{w["store_add"]}</a>'
    return f'<span class="btn" aria-disabled="true">{w["store_soon"]}</span>'


def tab_strip(w):
    """The animated row of browser tabs (the site's signature picture): three copies
    of the same page glow red, then fold into the green copy that stays.
    The animation itself lives in assets/site.css."""
    inbox, flight, report, weather = w['strip_tabs']
    return f'''<div class="strip-demo" role="img" aria-label="{attr(w['strip_label'])}">
  <div class="strip" aria-hidden="true">
    <div class="tab"><i></i><span>{inbox}</span></div>
    <div class="tab kept"><i></i><span>{flight}</span></div>
    <div class="tab hide-sm"><i></i><span>{report}</span></div>
    <div class="tab dup"><i></i><span>{flight}</span></div>
    <div class="tab dup hide-sm"><i></i><span>{flight}</span></div>
    <div class="tab hide-sm"><i></i><span>{weather}</span></div>
  </div>
  <div class="strip-body" aria-hidden="true">
    <div class="addr"><i></i><span>flights.farefinder.in/blr-goi</span></div>
    <div class="page-lines"><b></b><b></b><b></b></div>
  </div>
  <p class="strip-caption">{w['strip_caption']}</p>
</div>'''


def points(items, cls='points'):
    return f'<ul class="{cls}">' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>'


# ---------------------------------------------------------------------------
# BUILD EVERY TRANSLATED PAGE, LANGUAGE BY LANGUAGE
# ---------------------------------------------------------------------------
for code, prefix in LANGUAGES:
    up_home = '../' if prefix else ''           # from a language's home page back to the site's top
    w = Words(code, T[code])
    email_link = f'<a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a>'
    pro = f'<span class="pro-tag">{T[code]["pro_tag"]}</span>'
    w.vars = {'price': PRICE, 'email': SUPPORT_EMAIL, 'email_link': email_link, 'india': INDIA_PRICE,
              'name': 'DupTabOff', 'pro': pro}

    # ----- HOME PAGE -----
    a = up_home + 'assets/'  # where the pictures are, seen from this language's home page
    page(code, '', w['home_title'], w['home_desc'], f'''
<section class="home-hero wrap">
  <div>
    <h1>{w['hero_h1']}</h1>
    <p class="lead">{w['hero_lead']}</p>
    <div class="actions">
      <a class="btn" href="#products">{w['btn_products']}</a>
      <a class="btn ghost" href="mailto:{SUPPORT_EMAIL}">{w['btn_talk']}</a>
    </div>
  </div>
  <div class="hero-logo">
    <img class="logo-light" src="{a}logo.png" width="240" height="325" alt="{attr(w['logo_alt'])}">
    <img class="logo-dark" src="{a}logo-dark.png" width="240" height="325" alt="{attr(w['logo_alt'])}">
  </div>
</section>

<section class="wrap capabilities" aria-labelledby="what-we-build">
  <h2 id="what-we-build">{w['build_h2']}</h2>
  <div class="cap-grid">
    <div class="cap"><h3>{w['cap_soft_h']}</h3><p>{w['cap_soft_p']}</p></div>
    <div class="cap"><h3>{w['cap_ai_h']}</h3><p>{w['cap_ai_p']}</p></div>
    <div class="cap"><h3>{w['cap_auto_h']}</h3><p>{w['cap_auto_p']}</p></div>
  </div>
</section>

<section class="wrap products" id="products" aria-labelledby="products-title">
  <h2 id="products-title">{w['products_h2']}</h2>
  <p class="lead">{w['products_lead']}</p>
  <article class="product-card">
    <div>
      <img class="icon" src="{a}duptaboff-icon.png" width="56" height="56" alt="">
      <p class="kind">{w['dup_kind']}</p>
      <h3 class="product-name">DupTabOff</h3>
      <p class="lead">{w['dup_pitch']}</p>
      <div class="actions">
        <a class="btn" href="duptaboff/">{w['explore']}</a>
        <span class="fine">{w['dup_price']}</span>
      </div>
    </div>
    <img class="shot" src="{a}shots/light.webp" width="720" height="1150" loading="lazy" alt="{attr(w['dup_shot_alt'])}">
  </article>
  <p class="more">{w['more_products']}</p>
</section>

<section class="wrap how" aria-labelledby="how-title">
  <h2 id="how-title">{w['how_h2']}</h2>
  <dl class="how-list">
{''.join(f"    <div><dt>{t}</dt><dd>{d}</dd></div>" for t, d in w['how'])}
  </dl>
</section>

<section class="wrap contact-band">
  <h2>{w['contact_h2']}</h2>
  <p>{w['contact_p']}</p>
</section>
''', nav='products', jsonld={
        '@context': 'https://schema.org',
        '@graph': [org(w), {'@type': 'WebSite', '@id': url_of(code, '') + '#site', 'url': url_of(code, ''),
                            'name': 'Purple Wonton', 'publisher': {'@id': SITE + '/#org'}, 'inLanguage': code}],
    })

    # ----- DUPTABOFF PAGE -----
    a = '../' + up_home + 'assets/'
    w.vars.update({'privacy_url': '../' + up_home + 'privacy/', 'support_url': '../support/'})
    faq = w['faq']
    faq_html = '\n'.join(f'    <details><summary>{q}</summary><p>{ans}</p></details>' for q, ans in faq)
    shots = [('light', 1150, 'f1'), ('guard', 1200, 'f2'), ('search', 820, 'f3'), ('snooze', 1256, 'f4'), ('restore', 1250, 'f5')]

    def feature(i, flip):
        name, h, k = shots[i]
        pts = points(w[k + '_pts']) if (k + '_pts') in T['en'] else ''
        return f'''
  <section class="feature{' flip' if flip else ''}">
    <div>
      <h2>{w[k + '_h']}</h2>
      <p>{w[k + '_p']}</p>
      {pts}
    </div>
    <div class="shot-wrap"><img src="{a}shots/{name}.webp" width="720" height="{h}" loading="lazy" alt="{attr(w[k + '_alt'])}"></div>
  </section>'''

    india = f'<p class="fine">{w["india_note"]}</p>' if INDIA_PRICE else ''
    page(code, 'duptaboff/', w['dt_title'], w['dt_desc'], f'''
<section class="p-hero wrap">
  <div>
    <p class="title"><img src="{a}duptaboff-icon.png" width="44" height="44" alt="">{w['dt_for_chrome']}</p>
    <h1>{w['dt_h1']}</h1>
    <p class="lead">{w['dt_lead']}</p>
    <div class="actions">
      {store_button(w)}
      <a class="btn ghost" href="#pricing">{w['btn_compare']}</a>
    </div>
  </div>
  {tab_strip(w)}
</section>

<div class="wrap">{''.join(feature(i, i % 2 == 1) for i in range(5))}

  <section class="promise">
    <h2>{w['promise_h']}</h2>
    <p>{w['promise_p']}</p>
  </section>

  <section class="pricing" id="pricing">
    <h2>{w['pricing_h']}</h2>
    <p class="lead">{w['pricing_lead']}</p>
    <div class="plans">
      <div class="plan">
        <h3>{w['free_h']}</h3>
        <p class="price">$0</p>
        {points(w['free_items'])}
        <ul class="points missing" aria-label="{attr(w['missing_label'])}">{''.join(f'<li>{x}</li>' for x in w['free_missing'])}</ul>
      </div>
      <div class="plan pro">
        <h3>{w['pro_h']}</h3>
        <p class="price">{PRICE} <small>{w['pro_price_note']}</small></p>
        {india}
        {points(w['pro_headline'], 'points headline')}
        <p class="also">{w['also']}</p>
        {points(w['pro_more'])}
      </div>
    </div>
    <div class="actions">{store_button(w)}</div>
  </section>

  <section class="faq narrow" style="margin-left:0">
    <h2>{w['faq_h']}</h2>
{faq_html}
    <p class="fine" style="margin-top:20px">{w['faq_more']}</p>
  </section>
</div>
''', nav='duptaboff', jsonld={
        '@context': 'https://schema.org',
        '@graph': [org(w), {
            '@type': 'SoftwareApplication', 'name': 'DupTabOff: Duplicate Tab Remover',
            'url': url_of(code, 'duptaboff/'), 'inLanguage': code,
            'applicationCategory': 'BrowserApplication', 'operatingSystem': w['app_os'],
            'description': w['app_desc'], 'image': SITE + '/assets/og-duptaboff.jpg',
            'screenshot': SITE + '/assets/shots/light.webp', 'publisher': {'@id': SITE + '/#org'},
            'offers': [
                {'@type': 'Offer', 'name': w['free_h'], 'price': '0', 'priceCurrency': 'USD'},
                {'@type': 'Offer', 'name': 'Lifetime Pro', 'price': PRICE.lstrip('$'), 'priceCurrency': 'USD'},
            ],
        }, {
            '@type': 'FAQPage', 'inLanguage': code,
            'mainEntity': [{'@type': 'Question', 'name': strip_tags(q),
                            'acceptedAnswer': {'@type': 'Answer', 'text': strip_tags(ans)}} for q, ans in faq],
        }],
    })

    # ----- SUPPORT PAGE -----
    w.vars.update({'pricing_url': '../duptaboff/#pricing', 'dt_url': '../duptaboff/'})
    note = f'<p class="fine lang-note">{w["s_lang_note"]}</p>' if w['s_lang_note'] else ''
    page(code, 'support/', w['s_title'], w['s_desc'], f'''
<section class="doc narrow">
  <h1>{w['s_h1']}</h1>
  <p class="lead">{w['s_lead']}</p>
  {note}
  <div class="contact-card">
    <h2 style="margin-top:0">{w['s_email_h']}</h2>
    <p><a href="mailto:{SUPPORT_EMAIL}?subject=DupTabOff%20help">{SUPPORT_EMAIL}</a></p>
    <p class="fine">{w['s_email_note']}</p>
  </div>
  <h2>{w['s_keys_h']}</h2>
  <p>{w['s_keys_p']}</p>
  <h2>{w['s_refund_h']}</h2>
  <p>{w['s_refund_p']}</p>
  <h2>{w['s_back_h']}</h2>
  <p>{w['s_back_p']}</p>
  <h2>{w['s_common_h']}</h2>
  <p>{w['s_common_p']}</p>
</section>
''', nav='support')


# ---------------------------------------------------------------------------
# PRIVACY POLICY AND TERMS (English only, from the text files in content/)
# ---------------------------------------------------------------------------
def md_page(src, rel, title, description):
    text = open(os.path.join(ROOT, 'content', src), encoding='utf-8').read()
    # The "Draft note" line is a reminder for the owner, not for visitors.
    text = '\n'.join(l for l in text.split('\n') if not l.startswith('> Draft note'))
    body = markdown.markdown(text, extensions=['extra'])
    body = re.sub(r'<p>(Last updated:[^<]*)</p>', r'<p class="updated">\1</p>', body, count=1)
    page('en', rel, title, description, f'<section class="doc narrow">\n{body}\n</section>', translated=False)


md_page('PRIVACY.md', 'privacy/', 'DupTabOff privacy policy',
        'What DupTabOff reads, stores and sends: your tabs stay in your browser.')
md_page('TERMS.md', 'terms/', 'DupTabOff terms and conditions',
        'The terms for using DupTabOff and buying Lifetime Pro.')

# ---------------------------------------------------------------------------
# "PAGE NOT FOUND", AND FILES FOR SEARCH ENGINES AND GITHUB PAGES
# ---------------------------------------------------------------------------
page('en', '404.html', 'Page not found: Purple Wonton', 'This page does not exist.',
     '''<section class="doc narrow"><h1>That page doesn't exist.</h1>
<p class="lead">The link may be old or mistyped.</p>
<p><a class="btn" href="/">Go to the home page</a></p></section>''', translated=False)

with open(os.path.join(ROOT, 'CNAME'), 'w') as f:
    f.write('www.purplewonton.com')  # (no line break, matching GitHub's own copy) tells GitHub Pages which domain this site lives on
with open(os.path.join(ROOT, 'robots.txt'), 'w') as f:
    f.write(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')

# SITEMAP for Google: every page in every language, with the date it last changed.
# .page-dates.json remembers a fingerprint of every page; when a page's content
# changes, its date becomes today. So the dates stay correct automatically.
state_file = os.path.join(ROOT, '.page-dates.json')
try:
    state = json.load(open(state_file))
except (OSError, ValueError):
    state = {}
today = datetime.date.today().isoformat()
pages = {}
for code, prefix in LANGUAGES:
    for rel in TRANSLATED_PAGES:
        pages[prefix + rel] = prefix + rel + 'index.html'
pages['privacy/'] = 'privacy/index.html'
pages['terms/'] = 'terms/index.html'
with open(os.path.join(ROOT, 'sitemap.xml'), 'w') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for u, file in pages.items():
        digest = hashlib.sha256(open(os.path.join(ROOT, file), 'rb').read()).hexdigest()
        if state.get(u, {}).get('hash') != digest:
            state[u] = {'hash': digest, 'date': today}
        f.write(f'  <url><loc>{SITE}/{u}</loc><lastmod>{state[u]["date"]}</lastmod></url>\n')
    f.write('</urlset>\n')
json.dump(state, open(state_file, 'w'), indent=1)
print('done')
