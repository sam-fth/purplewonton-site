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
import html
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


def page(path, title, description, body, nav=''):
    """Wrap a page's own content in the shared header and footer, then save it.

    path:        where the page goes, e.g. 'duptaboff/index.html'
    title:       the text in the browser tab and in search results
    description: the short summary search engines and link previews show
    body:        the page's own content
    nav:         which menu item to show as "you are here"
    """
    depth = path.count('/')
    up = '../' * depth  # how to get back to the site's top folder from this page
    url = SITE + '/' + (path[:-len('index.html')] if path.endswith('index.html') else path)

    def cur(name):
        return ' aria-current="page"' if nav == name else ''

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
<meta property="og:image" content="{SITE}/assets/og-duptaboff.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="{up}assets/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap">
    <a class="brand" href="{up}"><img src="{up}assets/mark.png" width="36" height="36" alt=""><span>Purple Wonton</span></a>
    <nav class="nav" aria-label="Main">
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
page('index.html',
     'Purple Wonton: small, careful tools for your browser',
     'Purple Wonton is an independent software studio in Bengaluru. Our first product, DupTabOff, removes duplicate tabs in one click.',
     f'''
<section class="hero wrap">
  <h1>Small, careful tools that tidy up your browser.</h1>
  <p class="lead">Purple Wonton is an independent software studio in Bengaluru. We make simple tools that do one job well, keep your data on your own computer, and charge a fair price, once.</p>

  <article class="product-card">
    <div>
      <img class="icon" src="assets/duptaboff-icon.png" width="56" height="56" alt="">
      <h2>DupTabOff</h2>
      <p class="lead">Too many tabs, and three of them are the same page? DupTabOff finds every page you have open more than once and removes the extra copies in one click.</p>
      <div class="actions">
        <a class="btn" href="duptaboff/">See how it works</a>
        <span class="fine">Free, with Lifetime Pro for {PRICE} once</span>
      </div>
    </div>
    <img class="shot" src="assets/shots/light.webp" width="720" height="1150" alt="The DupTabOff popup listing duplicate tabs and which copy of each page stays open">
  </article>

  <section class="studio">
    <div>
      <img class="logo-light" src="assets/logo.png" width="200" height="271" alt="Purple Wonton: software, AI, automation">
      <img class="logo-dark" src="assets/logo-dark.png" width="200" height="271" alt="Purple Wonton: software, AI, automation">
    </div>
    <div>
      <h2>About Purple Wonton</h2>
      <p>We're a one-person studio building software, AI and automation tools that save people small amounts of time every day. Every product is private by design: no ads, no tracking, and nothing about you is sold.</p>
      <p>Questions or ideas? Write to <a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a>. We read every message.</p>
    </div>
  </section>
</section>
''')

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
          <li>Remove duplicates in the window you're in: your first 200 with no limit, then up to 10 per click</li>
          <li>Duplicate count on the icon, and right-click removal</li>
          <li>Search every open tab, copy all tab links</li>
          <li>Light and dark theme, larger text, keyboard use</li>
        </ul>
      </div>
      <div class="plan pro">
        <h3>Lifetime Pro</h3>
        <p class="price">{PRICE} <small>paid once, no subscription</small></p>
        {('<p class="fine">' + INDIA_PRICE + ' in India</p>') if INDIA_PRICE else ''}
        <ul class="points">
          <li>Remove every duplicate across all windows at once</li>
          <li>Stop duplicates before they open</li>
          <li>Undo, colour marks and sleep duplicates</li>
          <li>Snooze, saved sessions with folders, notes and sharing</li>
          <li>Automatic backups and tab clean-up tools</li>
          <li>One key works on up to 5 browsers</li>
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
''', nav='duptaboff')

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
    f.write('www.purplewonton.com\n')  # tells GitHub Pages which domain this site lives on
with open(os.path.join(ROOT, 'robots.txt'), 'w') as f:
    f.write(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
with open(os.path.join(ROOT, 'sitemap.xml'), 'w') as f:
    urls = ['', 'duptaboff/', 'support/', 'privacy/', 'terms/']
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for u in urls:
        f.write(f'  <url><loc>{SITE}/{u}</loc></url>\n')
    f.write('</urlset>\n')
print('done')
