# -*- coding: utf-8 -*-
"""One-off (2026-09-06): close the Creating with Claude gate.
Public tool download links -> signup anchor; ARC-preview 'sample' link removed and file pulled;
/downloads/* gets X-Robots-Tag noindex. Site-only pages (CwC hub + tool posts) — no src/ twin."""
import os, re, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

def rw(path, fn):
    t = open(path, encoding='utf-8').read()
    u = fn(t)
    if u != t:
        open(path, 'w', encoding='utf-8', newline='\n').write(u)
        print('changed', path)
    else:
        print('NO CHANGE', path)

# 1. CwC hub page
def hub(t):
    t = t.replace('          <a href="/downloads/creating-with-claude-sample.pdf" class="link-secondary" style="color: #9AA4AE;">Read a free sample &rarr;</a>\n', '')
    t = t.replace('<h2>Download &amp; Use</h2>\n      <p>Tools built during the writing of this book. Free for readers and anyone curious enough to try them.</p>',
                  '<h2>The Creating with Claude Toolkit</h2>\n      <p>Six tools built during the writing of this book. Free with your email &mdash; sign up below and the toolkit lands in your inbox.</p>')
    t = re.sub(r'<a href="/downloads/[a-z0-9-]+\.pdf" class="download-link">Download &rarr;</a>',
               '<a href="#signup" class="download-link">Get it free &darr;</a>', t)
    t = t.replace('<section class="newsletter section-pad">\n  <div class="container">\n    <div class="newsletter-inner fade-in">\n      <h2>Stay in the Loop</h2>\n      <p>Get notified when new tools drop, blog posts publish, and book updates land. No spam, ever.</p>',
                  '<section id="signup" class="newsletter section-pad">\n  <div class="container">\n    <div class="newsletter-inner fade-in">\n      <h2>Get the Toolkit</h2>\n      <p>Sign up and the six tools land in your inbox after you confirm &mdash; plus new tools, posts, and book updates. No spam, ever.</p>')
    t = t.replace('<p>New tools will be added here as they\'re built. Sign up below to get notified when something new drops.</p>',
                  '<p>New tools go to the list first. Sign up below and you\'ll have them the day they drop.</p>')
    return t
rw('site/creating-with-claude/index.html', hub)

# 2. The five tool posts
posts = ['ai-output-verification-checklist', 'ai-readiness-self-assessment', 'custom-instructions-builder',
         'prompt-library-starter-kit', 'what-should-i-build-idea-generator']
def post(t):
    t = t.replace('<p>Free, no strings attached. If it saves you an hour, tell a friend about the book.</p>',
                  '<p>Free with your email. Sign up and it lands in your inbox with the rest of the toolkit. If it saves you an hour, tell a friend about the book.</p>')
    t = re.sub(r'<a href="/downloads/[a-z0-9-]+\.pdf" class="btn-primary">Download it free</a>',
               '<a href="#signup" class="btn-primary">Get it free &darr;</a>', t)
    t = t.replace('<section class="newsletter section-pad">\n  <div class="container">\n    <div class="newsletter-inner fade-in">\n      <h2>Get the Next One</h2>',
                  '<section id="signup" class="newsletter section-pad">\n  <div class="container">\n    <div class="newsletter-inner fade-in">\n      <h2>Get the Toolkit</h2>')
    return t
for p in posts:
    rw(f'site/creating-with-claude/blog/{p}.html', post)

# 3. Generator template, if it carries the same CTA
gen = 'scripts/generate_creative_blog.py'
if os.path.exists(gen):
    def gfix(t):
        t = t.replace('Free, no strings attached. If it saves you an hour, tell a friend about the book.',
                      'Free with your email. Sign up and it lands in your inbox with the rest of the toolkit. If it saves you an hour, tell a friend about the book.')
        t = t.replace('class="btn-primary">Download it free</a>', 'class="btn-primary">Get it free &darr;</a>')
        t = t.replace('<section class="newsletter section-pad">', '<section id="signup" class="newsletter section-pad">')
        return t
    rw(gen, gfix)

# 4. Pull the ARC preview from the deploy folder
src = 'site/downloads/creating-with-claude-sample.pdf'
if os.path.exists(src):
    os.makedirs('downloads_originals_2026-09-06', exist_ok=True)
    shutil.move(src, 'downloads_originals_2026-09-06/creating-with-claude-sample-ARC-PREVIEW-pulled.pdf')
    print('pulled', src)

# 5. Headers: keep the PDFs reachable for the welcome email, but out of search
def hdr(t):
    if '/downloads/*\n' in t:
        return t
    return t.rstrip('\n') + '\n\n/downloads/*\n  X-Robots-Tag: noindex, nofollow\n'
rw('site/_headers', hdr)

# 6. Leftover check
left = []
for dp, dn, fns in os.walk('site'):
    for fn in fns:
        if fn.endswith('.html') and 'wwc-toolkit' not in dp:
            t = open(os.path.join(dp, fn), encoding='utf-8').read()
            for m in re.findall(r'href="/downloads/[^"]+"', t):
                left.append((os.path.join(dp, fn), m))
print('public /downloads/ links left:', left)
