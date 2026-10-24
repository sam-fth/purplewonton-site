"""
build.py: MAKES EVERY PAGE OF PURPLEWONTON.COM

In plain words:
  Every page shares the same header (logo and menu) and footer (links).
  Instead of copying them into each page by hand, this script writes all the
  pages from the templates below, so a change to the menu or footer happens
  everywhere at once. The privacy policy and terms come from the text files
  in content/ (the same text as inside the extension).

How to use it:
  1. Change the text below (or content/PRIVACY.md, content/TERMS.md).
  2. Run:  python3 build.py
  3. Commit and push. GitHub Pages publishes the new pages within a minute.

Things you will want to change later are in the SETTINGS section just below.
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

# PRODUCTS shown on the home page, newest first. To add a product, copy the
# DupTabOff entry, change the details, and add its own page (like duptaboff/).
PRODUCTS = [
    {
        'name': 'DupTabOff',
        'page': 'duptaboff/',
        'icon': 'assets/duptaboff-icon.png',
        'kind': 'Chrome extension',
        'pitch': 'Too many tabs, and three of them are the same page? DupTabOff finds every page you have open more than once and removes the extra copies in one click, and with Pro stops duplicates before they open.',
        'price': 'Free, with Lifetime Pro for ' + PRICE + ' once',
        'shot': 'assets/shots/light.webp',
        'shot_size': (720, 1150),
        'shot_alt': 'The DupTabOff popup listing duplicate tabs and which copy of each page stays open',
    },
]



def page(path, title, description, body, nav='', jsonld=None, og_image='assets/og-duptaboff.jpg'):
    """Wrap a page's own content in the shared header and footer, then save it.

    path:        where the page goes, e.g. 'duptaboff/index.html'
    title:       the text in the browser tab and in search results
    description: the short summary search engines and link previews show
    body:        the page's own content
    nav:         which menu item to show as "you are here"
    jsonld:      optional facts for Google ("structured data"): who we are, what a product costs...
    og_image:    the picture shown when the page is shared in chat apps or social media
    """
    depth = path.count('/')
    up = '../' * depth  # how to get back to the site's top folder from this page
    url = SITE + '/' + (path[:-len('index.html')] if path.endswith('index.html') else path)

    def cur(name):
        return ' aria-current="page"' if nav == name else ''

    # Structured data: a small block of facts Google reads to understand the page
    # (and may show as richer search results). It is invisible to visitors.
    ld = ''
    if jsonld:
        ld = '<script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False) + '</script>'

    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{url}">
<link rel="icon" href="{up}assets/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="{up}assets/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/{og_image}">
<meta property="og:site_name" content="Purple Wonton">
<meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="#7140e0">
{ld}
<link rel="stylesheet" href="{up}assets/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap">
    <a class="brand" href="{up}"><img src="{up}assets/mark.png" width="36" height="36" alt=""><span>Purple Wonton</span></a>
    <nav class="nav" aria-label="Main">
      <a href="{up}#products"{cur('products')}>Products</a>
      <a href="{up}duptaboff/"{cur('duptaboff')}>DupTabOff</a>
      <a href="{up}support/"{cur('support')}>Support</a>
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-foot">
  <div class="wrap">
    <span>© {YEAR} Purple Wonton, Bengaluru, India</span>
    <nav aria-label="Footer">
      <a href="{up}duptaboff/">DupTabOff</a>
      <a href="{up}support/">Support</a>
      <a href="{up}privacy/">Privacy policy</a>
      <a href="{up}terms/">Terms</a>
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


def store_button(up=''):
    """The "Add to Chrome" button. Before the store link exists it says "coming soon"."""
    if CHROME_STORE_URL:
        return f'<a class="btn" href="{CHROME_STORE_URL}" rel="noopener">Add to Chrome, it\'s free</a>'
    return '<span class="btn" aria-disabled="true">Coming soon to the Chrome Web Store</span>'


ORG = {
    '@type': 'Organization',
    '@id': SITE + '/#org',
    'name': 'Purple Wonton',
    'url': SITE + '/',
    'logo': SITE + '/assets/mark.png',
    'email': SUPPORT_EMAIL,
    'description': 'Purple Wonton is a technology studio in Bengaluru, India, building software, AI and automation products.',
    'address': {'@type': 'PostalAddress', 'addressLocality': 'Bengaluru', 'addressRegion': 'Karnataka', 'addressCountry': 'IN'},
}


def tab_strip():
    """The animated row of browser tabs (the site's signature picture).

    Three copies of "Flight options to Goa" glow red, then fold into the green
    copy that stays. The animation itself lives in assets/site.css.
    """
    return '''<div class="strip-demo" aria-label="Three copies of the same page fold into one">
  <div class="strip" aria-hidden="true">
    <div class="tab"><i></i><span>Inbox (12)</span></div>
    <div class="tab kept"><i></i><span>Flight options to Goa</span></div>
    <div class="tab hide-sm"><i></i><span>Q3 report draft</span></div>
    <div class="tab dup"><i></i><span>Flight options to Goa</span></div>
    <div class="tab dup hide-sm"><i></i><span>Flight options to Goa</span></div>
    <div class="tab hide-sm"><i></i><span>Bengaluru weather</span></div>
  </div>
  <div class="strip-body">
    <div class="addr"><i></i><span>flights.farefinder.in/blr-goi</span></div>
    <div class="page-lines"><b></b><b></b><b></b></div>
  </div>
  <p class="strip-caption">Same page, open three times. DupTabOff closes the extra copies and <b>keeps the one you need</b>, without moving any other tab.</p>
</div>'''


# ---------------------------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------------------------
def product_card(p):
    """One product on the home page, built from an entry in PRODUCTS."""
    w, h = p['shot_size']
    return f'''
  <article class="product-card">
    <div>
      <img class="icon" src="{p['icon']}" width="56" height="56" alt="">
      <p class="kind">{html.escape(p['kind'])}</p>
      <h3 class="product-name">{html.escape(p['name'])}</h3>
      <p class="lead">{html.escape(p['pitch'])}</p>
      <div class="actions">
        <a class="btn" href="{p['page']}">Explore {html.escape(p['name'])}</a>
        <span class="fine">{html.escape(p['price'])}</span>
      </div>
    </div>
    <img class="shot" src="{p['shot']}" width="{w}" height="{h}" loading="lazy" alt="{html.escape(p['shot_alt'])}">
  </article>'''


page('index.html',
     'Purple Wonton: software, AI and automation, made in Bengaluru',
     'Purple Wonton is a technology studio in Bengaluru, India, building fast, private software, AI and automation products. Our first product: DupTabOff for Chrome.',
     f'''
<section class="home-hero wrap">
  <div>
    <h1>Software, AI and automation, engineered with care.</h1>
    <p class="lead">Purple Wonton is a technology studio in Bengaluru. We design and build modern software products that take repetitive work off your hands: fast, private by design, and tested in real browsers before they reach you.</p>
    <div class="actions">
      <a class="btn" href="#products">See our products</a>
      <a class="btn ghost" href="mailto:{SUPPORT_EMAIL}">Talk to us</a>
    </div>
  </div>
  <div class="hero-logo">
    <img class="logo-light" src="assets/logo.png" width="240" height="325" alt="Purple Wonton: software, AI, automation">
    <img class="logo-dark" src="assets/logo-dark.png" width="240" height="325" alt="Purple Wonton: software, AI, automation">
  </div>
</section>

<section class="wrap capabilities" aria-labelledby="what-we-build">
  <h2 id="what-we-build">What we build</h2>
  <div class="cap-grid">
    <div class="cap">
      <h3>Software</h3>
      <p>Browser extensions and apps that feel instant and stay out of your way, built on current web standards and kept working on older devices too.</p>
    </div>
    <div class="cap">
      <h3>AI</h3>
      <p>Practical intelligence inside everyday tools: features that understand what you're doing and save real minutes, not demos.</p>
    </div>
    <div class="cap">
      <h3>Automation</h3>
      <p>Repetitive clicks turned into one action, or none at all, so the computer does the chores and you do the thinking.</p>
    </div>
  </div>
</section>

<section class="wrap products" id="products" aria-labelledby="products-title">
  <h2 id="products-title">Products</h2>
  <p class="lead">Each Purple Wonton product does one job very well, keeps your data on your own device, and is priced fairly, with no subscriptions you didn't ask for.</p>
  {"".join(product_card(p) for p in PRODUCTS)}
  <p class="more">More products are in the works. Ideas for what we should build next are welcome at <a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a>.</p>
</section>

<section class="wrap how" aria-labelledby="how-title">
  <h2 id="how-title">How we work</h2>
  <dl class="how-list">
    <div><dt>Private by design</dt><dd>Our products work on your device. No ads, no tracking, and nothing about you is sold or shared.</dd></div>
    <div><dt>Tested like it matters</dt><dd>Every release runs hundreds of automated checks, including tests that click through the product in a real browser.</dd></div>
    <div><dt>Fair, clear pricing</dt><dd>A useful free version, and one-time Lifetime upgrades. You always know what you pay and what you get.</dd></div>
    <div><dt>Built to last</dt><dd>Clean, well-documented code that supports older computers and browsers, so tools keep working for years.</dd></div>
  </dl>
</section>

<section class="wrap contact-band">
  <h2>Have a question or an idea?</h2>
  <p>Write to <a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a>. We read every message.</p>
</section>
''', nav='products', jsonld={
    '@context': 'https://schema.org',
    '@graph': [ORG, {'@type': 'WebSite', '@id': SITE + '/#site', 'url': SITE + '/', 'name': 'Purple Wonton', 'publisher': {'@id': SITE + '/#org'}, 'inLanguage': 'en'}],
})

# ---------------------------------------------------------------------------
# DUPTABOFF PRODUCT PAGE
# ---------------------------------------------------------------------------
faq = [
    ('Will it close my Gmail, Google Docs or other web apps?',
     'Only real duplicates close. Apps like Gmail use the part of the address after # for different screens, so your inbox and an open email are not treated as copies. Pinned tabs and tabs playing sound are never closed.'),
    ('Will it mix up the order of my tabs?',
     'No. DupTabOff never moves a tab when removing duplicates; it only closes the extra copies. The copy you\'re looking at, a pinned copy, or a copy inside one of your tab groups is the one that stays.'),
    ('What is the difference between Free and Lifetime Pro?',
     f'The free version removes duplicates in the window you\'re in: your first 200 with no limit, then up to 10 per click. Lifetime Pro checks every window at once, stops duplicates before they open, and adds Undo, colour marks, snooze, saved sessions and clean-up tools.'),
    ('Is Lifetime Pro a subscription?',
     f'No. Lifetime Pro is {PRICE}, paid once, with no renewals. One license key works on up to 5 browsers. You can try every Pro feature free for 7 days first, with nothing to cancel.'),
    ('Does DupTabOff collect my browsing data?',
     'No. Your tabs are read only inside your browser and nothing about them is sent anywhere. There are no ads, no analytics and no account. The only time DupTabOff goes online is to check a Pro license key with Gumroad, the store that sells Pro.'),
    ('Which browsers does it work in?',
     'Chrome 88 or newer on Windows, Mac, Linux and ChromeOS, and Chromium browsers such as Edge, Brave, Opera and Vivaldi. Chrome on phones doesn\'t support extensions.'),
    ('Can I get a refund?',
     f'Yes. If Pro doesn\'t work for you, email {SUPPORT_EMAIL} within 14 days of buying and we\'ll refund you.'),
]
faq_html = '\n'.join(
    f'    <details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in faq)

page('duptaboff/index.html',
     'DupTabOff: remove duplicate tabs in one click',
     f'DupTabOff finds every page you have open more than once and removes the extra copies in one click. Free, with Lifetime Pro for {PRICE} once.',
     f'''
<section class="p-hero wrap">
  <div>
    <p class="title"><img src="../assets/duptaboff-icon.png" width="44" height="44" alt="">DupTabOff for Chrome</p>
    <h1>Same page open three times? Keep one.</h1>
    <p class="lead">DupTabOff finds every page you have open more than once, shows which copy stays, and removes the rest in one click. Pinned tabs, music and the tab you're reading are never touched.</p>
    <div class="actions">
      {store_button()}
      <a class="btn ghost" href="#pricing">Free vs Lifetime Pro</a>
    </div>
  </div>
  {tab_strip()}
</section>

<div class="wrap">
  <section class="feature">
    <div>
      <h2>See which copy stays before anything closes</h2>
      <p>The number on the DupTabOff icon tells you how many duplicates are open. Open the popup and each duplicated page is listed, with the copy that stays and the copies that close.</p>
      <ul class="points">
        <li>Treats http and https, www, trailing slashes and tracking codes as the same page</li>
        <li>Right-click any page and choose "Remove duplicates of this page"</li>
        <li>Undo brings back the tabs you just removed <span class="pro-tag">Pro</span></li>
      </ul>
    </div>
    <div class="shot-wrap"><img src="../assets/shots/light.webp" width="720" height="1150" loading="lazy" alt="DupTabOff popup showing 10 duplicate tabs, with Q3 report draft open four times: one copy stays, three close"></div>
  </section>

  <section class="feature flip">
    <div>
      <h2>Stop duplicates before they open <span class="pro-tag">Pro</span></h2>
      <p>Click a link or bookmark to a page you already have open, and DupTabOff takes you to that tab instead of opening another copy. Links you open in the background close quietly, so you're never pulled away from what you're reading.</p>
      <ul class="points">
        <li>Never touches sign-in windows, form results or tabs you duplicated on purpose</li>
        <li>Recently stopped pages are listed with a Reopen button</li>
      </ul>
    </div>
    <div class="shot-wrap"><img src="../assets/shots/guard.webp" width="720" height="1200" loading="lazy" alt="Prevention mode switched on, with a list of recently stopped duplicate pages and Reopen buttons"></div>
  </section>

  <section class="feature">
    <div>
      <h2>Find any tab in a second</h2>
      <p>Press / in the popup and start typing. Matching tabs from every window appear as you type, and Enter takes you straight there. Free for everyone.</p>
    </div>
    <div class="shot-wrap"><img src="../assets/shots/search.webp" width="720" height="820" loading="lazy" alt="Searching for bengaluru lists five matching tabs across windows"></div>
  </section>

  <section class="feature flip">
    <div>
      <h2>Snooze a tab until you need it <span class="pro-tag">Pro</span></h2>
      <p>Close a tab now and have it come back by itself later today, this evening, tomorrow morning, next Monday or any time you pick. If Chrome is closed then, it comes back the next time you open it.</p>
    </div>
    <div class="shot-wrap"><img src="../assets/shots/snooze.webp" width="720" height="1256" loading="lazy" alt="Snooze screen with later today, this evening, tomorrow morning and next Monday, and two snoozed tabs"></div>
  </section>

  <section class="feature">
    <div>
      <h2>Never lose a set of tabs again <span class="pro-tag">Pro</span></h2>
      <p>Save your open tabs as a named session, file it in a folder, add a note, and reopen it in one click with pinned tabs and tab groups back in place. Automatic backups every 30 minutes protect you from crashes.</p>
      <ul class="points">
        <li>Share a session as a simple page of links you can send to anyone</li>
        <li>Clean-up tools: close unused tabs, close a whole site, merge windows, sort by site</li>
      </ul>
    </div>
    <div class="shot-wrap"><img src="../assets/shots/restore.webp" width="720" height="1250" loading="lazy" alt="Saved sessions grouped into Personal and Work folders, with Restore and Share buttons"></div>
  </section>

  <section class="promise">
    <h2>Private by design</h2>
    <p>DupTabOff reads your open tabs only inside your browser. It has no ads, no analytics and no account, and your tabs and sessions never leave your computer. Read the <a href="../privacy/">privacy policy</a>.</p>
  </section>

  <section class="pricing" id="pricing">
    <h2>Free to use. Lifetime Pro when you want more.</h2>
    <p class="lead">Try every Pro feature free for 7 days, with nothing to pay or cancel.</p>
    <div class="plans">
      <div class="plan">
        <h3>Free</h3>
        <p class="price">$0</p>
        <ul class="points">
          <li>Remove duplicates in <strong class="limit">the current window only</strong></li>
          <li>Your first <strong class="limit">200</strong> removals with no limit, then <strong class="limit">10 per click</strong></li>
          <li>Duplicate count on the icon, and right-click removal</li>
          <li>Search every open tab, copy all tab links</li>
          <li>Light and dark theme, larger text, keyboard use</li>
        </ul>
        <ul class="points missing" aria-label="Not included in the free version">
          <li>No Undo</li>
          <li>No prevention mode</li>
          <li>No snooze, saved sessions or backups</li>
        </ul>
      </div>
      <div class="plan pro">
        <h3>Lifetime Pro</h3>
        <p class="price">{PRICE} <small>paid once, no subscription</small></p>
        {('<p class="fine">' + INDIA_PRICE + ' in India</p>') if INDIA_PRICE else ''}
        <ul class="points headline">
          <li><strong>Remove every duplicate in one click</strong>: no 200 limit, no 10-per-click cap</li>
          <li><strong>Check all windows at once</strong>, plus private windows if you allow it</li>
          <li><strong>Stop duplicates before they open</strong>, including addresses you type</li>
          <li><strong>Undo</strong> a removal, with tabs put back exactly where they were</li>
          <li><strong>Colour marks</strong>: each set of duplicates in its own colour</li>
        </ul>
        <p class="also">Also included</p>
        <ul class="points">
          <li>Sleep duplicates to free memory without closing them</li>
          <li>Snooze tabs until later today, tonight, tomorrow, next Monday or a time you pick</li>
          <li>Saved sessions with folders and notes, restored with pinned tabs and groups</li>
          <li>Share a session as a page of links, or copy it as text</li>
          <li>Automatic backups every 30 minutes, keeping the last 24</li>
          <li>Clean-up tools: close unused tabs, close a whole site, merge windows, sort by site</li>
          <li>Sites to leave alone, for pages you keep open twice on purpose</li>
          <li>Keyboard shortcut to remove duplicates from anywhere</li>
          <li>One key works on up to 5 browsers, with all future Pro updates included</li>
        </ul>
      </div>
    </div>
    <div class="actions">{store_button()}</div>
  </section>

  <section class="faq narrow" style="margin-left:0">
    <h2>Questions</h2>
{faq_html}
    <p class="fine" style="margin-top:20px">More answers on the <a href="../support/">support page</a>.</p>
  </section>
</div>
''', nav='duptaboff', jsonld={
    '@context': 'https://schema.org',
    '@graph': [ORG, {
        '@type': 'SoftwareApplication',
        'name': 'DupTabOff: Duplicate Tab Remover',
        'url': SITE + '/duptaboff/',
        'applicationCategory': 'BrowserApplication',
        'operatingSystem': 'Chrome 88 or newer on Windows, macOS, Linux and ChromeOS',
        'description': 'Removes duplicate tabs in one click. Pro stops duplicates before they open, checks every window, and adds undo, snooze, saved sessions and clean-up tools.',
        'image': SITE + '/assets/og-duptaboff.jpg',
        'screenshot': SITE + '/assets/shots/light.webp',
        'publisher': {'@id': SITE + '/#org'},
        'offers': [
            {'@type': 'Offer', 'name': 'Free', 'price': '0', 'priceCurrency': 'USD'},
            {'@type': 'Offer', 'name': 'Lifetime Pro', 'price': PRICE.lstrip('$'), 'priceCurrency': 'USD'},
        ],
    }, {
        '@type': 'FAQPage',
        'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq],
    }],
})

# ---------------------------------------------------------------------------
# SUPPORT PAGE
# ---------------------------------------------------------------------------
page('support/index.html',
     'Support: Purple Wonton',
     'Get help with DupTabOff: contact Purple Wonton, refunds, license keys and common questions.',
     f'''
<section class="doc narrow">
  <h1>Support</h1>
  <p class="lead">Something not working, or an idea for DupTabOff? Write to us and include which version of Chrome you use. We read every message.</p>
  <div class="contact-card">
    <h2 style="margin-top:0">Email</h2>
    <p><a href="mailto:{SUPPORT_EMAIL}?subject=DupTabOff%20help">{SUPPORT_EMAIL}</a></p>
    <p class="fine">Inside DupTabOff, the "?" button opens the help page, and its Contact button fills in your version numbers for you.</p>
  </div>

  <h2>License keys</h2>
  <p>After buying Lifetime Pro, copy the license key from your Gumroad receipt, open DupTabOff's settings, click "Enter key" and paste it. One key works on up to 5 browsers. If a key says it's used on too many browsers, reply to your receipt email and we'll reset it.</p>

  <h2>Refunds</h2>
  <p>If Pro doesn't work for you, email us within 14 days of buying and we'll refund you. After 14 days, refunds are at our discretion, and your rights under your country's consumer law always apply.</p>

  <h2>Getting tabs back</h2>
  <p>Chrome itself can reopen recently closed tabs: press Ctrl+Shift+T (Cmd+Shift+T on Mac). With Pro, DupTabOff's Undo button brings back a whole batch in the windows they came from.</p>

  <h2>Common questions</h2>
  <p>See the <a href="../duptaboff/#pricing">Free vs Lifetime Pro</a> comparison and the questions at the bottom of the <a href="../duptaboff/">DupTabOff page</a>.</p>
</section>
''', nav='support')

# ---------------------------------------------------------------------------
# PRIVACY POLICY AND TERMS (from the text files in content/)
# ---------------------------------------------------------------------------
def md_page(src, path, title, description):
    text = open(os.path.join(ROOT, 'content', src), encoding='utf-8').read()
    # The "Draft note" line is a reminder for the owner, not for visitors.
    text = '\n'.join(l for l in text.split('\n') if not l.startswith('> Draft note'))
    body = markdown.markdown(text, extensions=['extra'])
    # Show the "Last updated" line in grey.
    body = re.sub(r'<p>(Last updated:[^<]*)</p>', r'<p class="updated">\1</p>', body, count=1)
    page(path, title, description, f'<section class="doc narrow">\n{body}\n</section>')

md_page('PRIVACY.md', 'privacy/index.html', 'DupTabOff privacy policy',
        'What DupTabOff reads, stores and sends: your tabs stay in your browser.')
md_page('TERMS.md', 'terms/index.html', 'DupTabOff terms and conditions',
        'The terms for using DupTabOff and buying Lifetime Pro.')

# ---------------------------------------------------------------------------
# "PAGE NOT FOUND", AND FILES FOR SEARCH ENGINES AND GITHUB PAGES
# ---------------------------------------------------------------------------
page('404.html', 'Page not found: Purple Wonton', 'This page does not exist.',
     '''<section class="doc narrow"><h1>That page doesn't exist.</h1>
<p class="lead">The link may be old or mistyped.</p>
<p><a class="btn" href="/">Go to the home page</a></p></section>''')

with open(os.path.join(ROOT, 'CNAME'), 'w') as f:
    f.write('www.purplewonton.com')  # (no line break, matching GitHub's own copy) tells GitHub Pages which domain this site lives on
with open(os.path.join(ROOT, 'robots.txt'), 'w') as f:
    f.write(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
# SITEMAP for Google, with the date each page last changed.
# .page-dates.json remembers a fingerprint of every page; when a page's content
# changes, its date becomes today. So the dates stay correct automatically.
state_file = os.path.join(ROOT, '.page-dates.json')
try:
    state = json.load(open(state_file))
except (OSError, ValueError):
    state = {}
today = datetime.date.today().isoformat()
pages = {'': 'index.html', 'duptaboff/': 'duptaboff/index.html', 'support/': 'support/index.html',
         'privacy/': 'privacy/index.html', 'terms/': 'terms/index.html'}
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
