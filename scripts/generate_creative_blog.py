#!/usr/bin/env python3
"""Creative blog generator - Creating with Claude.

Markdown in content/creative-blog/*.md -> site/creating-with-claude/blog/<slug>.html
Draft posts (status: draft) render to _preview/creative-blog/ instead of the site.
Rebuilds the card grid in blog.html and the 3-post preview on the hub page.

Frontmatter keys: title, date (YYYY-MM-DD), category, excerpt,
  subtitle (optional), download_url (optional), download_label (optional),
  status (draft | published)

Usage: python scripts/generate_creative_blog.py
"""
import os, re, html
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, 'content', 'creative-blog')
OUTDIR = os.path.join(ROOT, 'site', 'creating-with-claude', 'blog')
PREVIEW = os.path.join(ROOT, '_preview', 'creative-blog')
INDEX = os.path.join(ROOT, 'site', 'creating-with-claude', 'blog.html')
HUB = os.path.join(ROOT, 'site', 'creating-with-claude', 'index.html')
SITE = 'https://www.marquepublishing.com'

def parse_post(fp):
    txt = open(fp, encoding='utf-8').read()
    m = re.match(r'---\s*\n(.*?)\n---\s*\n(.*)', txt, re.S)
    meta, body = {}, txt
    if m:
        for line in m.group(1).splitlines():
            if ':' in line:
                k, v = line.split(':', 1)
                meta[k.strip()] = v.strip()
        body = m.group(2).strip()
    return meta, body

def md_inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', s)
    return s

def md_to_html(md):
    out, in_list, first_p = [], None, True
    def close():
        nonlocal in_list
        if in_list:
            out.append('</%s>' % in_list)
            in_list = None
    for ln in md.split('\n'):
        s = ln.strip()
        if not s:
            close()
        elif s.startswith('### '):
            close(); out.append('<h3>%s</h3>' % md_inline(s[4:]))
        elif s.startswith('## '):
            close(); out.append('<h2>%s</h2>' % md_inline(s[3:]))
        elif s.startswith('> '):
            close(); out.append('<blockquote><p>%s</p></blockquote>' % md_inline(s[2:]))
        elif re.match(r'[-*] ', s):
            if in_list != 'ul': close(); out.append('<ul>'); in_list = 'ul'
            out.append('<li>%s</li>' % md_inline(s[2:]))
        elif re.match(r'\d+\. ', s):
            if in_list != 'ol': close(); out.append('<ol>'); in_list = 'ol'
            out.append('<li>%s</li>' % md_inline(re.sub(r'^\d+\. ', '', s)))
        else:
            close()
            cls = ' class="lead"' if first_p else ''
            out.append('<p%s>%s</p>' % (cls, md_inline(s)))
            first_p = False
    close()
    return '\n'.join(out)

NAV = '''<nav class="site-nav" aria-label="Main navigation">
  <div class="container nav-inner">
    <a href="/" class="wordmark">
      <svg class="wordmark-diamond" width="32" height="32" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <path d="M50 4 L92 50 L50 96 L8 50 Z" fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round"/>
        <path d="M50 16 L80 50 L50 84 L20 50 Z" fill="none" stroke="var(--accent)" stroke-width="1.5"/>
        <path d="M50 0 L53 4 L50 8 L47 4 Z" fill="var(--accent)"/>
        <text x="50" y="60" text-anchor="middle" font-family="'Cormorant', 'EB Garamond', Georgia, serif" font-weight="700" font-size="40" fill="currentColor">M</text>
      </svg>
      <span class="wordmark-text">
        <span class="wordmark-name">Marque</span>
        <span class="wordmark-sub">Publishing</span>
      </span>
    </a>
    <button class="nav-toggle" aria-label="Toggle navigation" aria-expanded="false" onclick="this.setAttribute('aria-expanded',this.getAttribute('aria-expanded')==='false'?'true':'false');document.querySelector('.nav-links').classList.toggle('open')">
      <span></span><span></span><span></span>
    </button>
    <ul class="nav-links">
      <li><a href="/">Home</a></li>
      <li><a href="/books">Books</a></li>
      <li><a href="/about">About</a></li>
      <li><a href="/blog">Blog</a></li>
      <li><a href="/labs">Labs</a></li>
    </ul>
  </div>
</nav>'''

FOOTER = '''<footer class="site-footer">
  <div class="container footer-inner">
    <div class="footer-left">
      <a href="/" class="wordmark">
        <svg class="wordmark-diamond" width="24" height="24" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <path d="M50 4 L92 50 L50 96 L8 50 Z" fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round"/>
          <path d="M50 16 L80 50 L50 84 L20 50 Z" fill="none" stroke="var(--accent)" stroke-width="1.5"/>
          <text x="50" y="60" text-anchor="middle" font-family="'Cormorant', 'EB Garamond', Georgia, serif" font-weight="700" font-size="40" fill="currentColor">M</text>
        </svg>
        <span class="wordmark-text">
          <span class="wordmark-name">Marque</span>
          <span class="wordmark-sub">Publishing</span>
        </span>
      </a>
      <span class="footer-year">&copy; 2026 Marque Publishing</span>
    </div>
    <ul class="footer-links">
      <li><a href="/books">Books</a></li>
      <li><a href="/about">About</a></li>
      <li><a href="/blog">Blog</a></li>
      <li><a href="/labs">Labs</a></li>
    </ul>
    <div class="footer-social">
      <a href="https://www.linkedin.com/in/christhatcher/" aria-label="LinkedIn" target="_blank" rel="noopener noreferrer">
        <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
      </a>
    </div>
  </div>
</footer>'''

POST_CSS = '''<style>
.post-header { max-width: 42rem; margin-inline: auto; margin-bottom: 2.5rem; }
.post-meta { display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
.post-category { font-size: 0.8rem; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; color: var(--accent); }
.post-date { font-size: 0.85rem; color: var(--text-subtle); }
.post-meta-divider { width: 4px; height: 4px; border-radius: 50%; background: var(--text-subtle); }
.post-header h1 { font-family: var(--serif); font-size: clamp(2rem, 4vw, 2.8rem); font-weight: 600; line-height: 1.2; letter-spacing: -0.01em; margin-bottom: 1rem; }
.post-subtitle { font-family: var(--serif); font-size: 1.2rem; font-style: italic; color: var(--text-muted); line-height: 1.5; }
.article-prose { max-width: 42rem; margin-inline: auto; }
.article-prose p { font-family: var(--serif); font-size: 1.15rem; color: var(--text); line-height: 1.8; margin-bottom: 1.5rem; }
.article-prose h2 { font-family: var(--serif); font-size: 1.6rem; font-weight: 600; margin-top: 3rem; margin-bottom: 1rem; line-height: 1.3; }
.article-prose h3 { font-family: var(--serif); font-size: 1.3rem; font-weight: 600; margin-top: 2rem; margin-bottom: 0.75rem; line-height: 1.35; }
.article-prose strong { font-weight: 600; color: var(--text); }
.article-prose ol, .article-prose ul { margin-bottom: 1.5rem; padding-left: 1.5rem; }
.article-prose ol li, .article-prose ul li { font-family: var(--serif); font-size: 1.15rem; color: var(--text); line-height: 1.8; margin-bottom: 1rem; }
.article-prose .lead { font-size: 1.25rem; color: var(--text); line-height: 1.7; }
.article-prose blockquote { border-left: 3px solid var(--accent); padding-left: 1.5rem; margin: 2rem 0; }
.article-prose blockquote p { font-family: var(--serif); font-style: italic; font-size: 1.25rem; color: var(--text-muted); }
.back-link { display: inline-flex; align-items: center; gap: 0.4rem; font-size: 0.9rem; font-weight: 500; color: var(--text-muted); margin-bottom: 2rem; transition: color 0.2s; }
.back-link:hover { color: var(--accent); }
.download-cta { max-width: 42rem; margin: 3rem auto 0; background: var(--card-bg); border: 1px solid var(--border); border-left: 3px solid var(--accent); border-radius: 10px; box-shadow: var(--card-shadow); padding: 1.75rem; }
.download-cta h3 { font-family: var(--serif); font-size: 1.25rem; font-weight: 600; margin-bottom: 0.5rem; }
.download-cta p { font-size: 0.95rem; color: var(--text-muted); line-height: 1.6; margin-bottom: 1.25rem; }
</style>'''

PAGE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} &mdash; Creating with Claude &mdash; Marque Publishing</title>
<meta name="description" content="{excerpt}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.png" type="image/png" sizes="32x32">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{excerpt}">
<meta property="og:url" content="{site}/creating-with-claude/blog/{slug}">
<link rel="canonical" href="{site}/creating-with-claude/blog/{slug}">
<meta property="og:type" content="article">
<meta property="og:image" content="{site}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/css/style.css">
<script type="application/ld+json">
{{"@context": "https://schema.org", "@type": "BlogPosting",
  "headline": "{title}", "datePublished": "{date}",
  "author": {{"@type": "Person", "name": "Chris Thatcher"}},
  "publisher": {{"@type": "Organization", "name": "Marque Publishing", "url": "{site}"}},
  "description": "{excerpt}"}}
</script>
<!-- MailerLite Universal -->
<script>
(function(w,d,e,u,f,l,n){{w[f]=w[f]||function(){{(w[f].q=w[f].q||[])
.push(arguments);}},l=d.createElement(e),l.async=1,l.src=u,
n=d.getElementsByTagName(e)[0],n.parentNode.insertBefore(l,n);}})
(window,document,'script','https://assets.mailerlite.com/js/universal.js','ml');
ml('account', '2453958');
</script>
<!-- End MailerLite Universal -->
{css}
</head>
<body>
<a href="#main-content" class="skip-link">Skip to content</a>
{nav}

<article class="section-pad" id="main-content">
  <div class="container">
    <div style="max-width: 42rem; margin-inline: auto;">
      <a href="/creating-with-claude/blog" class="back-link">&larr; All posts</a>
    </div>
    <header class="post-header fade-in">
      <div class="post-meta">
        <span class="post-category">{category}</span>
        <span class="post-meta-divider"></span>
        <time class="post-date">{date_disp}</time>
      </div>
      <h1>{title}</h1>
      {subtitle_html}
    </header>
    <div class="article-prose fade-in">
{body}
    </div>
    {cta}
  </div>
</article>

<section class="newsletter section-pad">
  <div class="container">
    <div class="newsletter-inner fade-in">
      <h2>Get the Next One</h2>
      <p>New tools, tutorials, and book updates from Creating with Claude. No spam, ever.</p>
      <div class="ml-embedded" data-form="NTW6JI"></div>
    </div>
  </div>
</section>

{footer}

<script>
const observer = new IntersectionObserver((entries) => {{
  entries.forEach(entry => {{
    if (entry.isIntersecting) {{ entry.target.classList.add('visible'); observer.unobserve(entry.target); }}
  }});
}}, {{ threshold: 0.15, rootMargin: '0px 0px -40px 0px' }});
document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
document.querySelectorAll('.nav-links a').forEach(link => {{
  link.addEventListener('click', () => {{ document.querySelector('.nav-links').classList.remove('open'); }});
}});
</script>
</body>
</html>'''

CTA_TMPL = '''<div class="download-cta fade-in">
      <h3>{label}</h3>
      <p>Free, no strings attached. If it saves you an hour, tell a friend about the book.</p>
      <a href="{url}" class="btn-primary">{button}</a>
    </div>'''

CARD_TMPL = '''      <a href="/creating-with-claude/blog/{slug}" class="blog-card">
        <div class="blog-card-body">
          <p class="blog-card-meta">{date_disp} &middot; {category}</p>
          <h3>{title}</h3>
          <p>{excerpt}</p>
          <span class="blog-card-link">Read more &rarr;</span>
        </div>
      </a>'''

EMPTY_HTML = '''    <div class="blog-empty fade-in">
      <h3>First posts are on the way</h3>
      <p>I'm writing the first tutorials and project walkthroughs now. Sign up below and I'll let you know when they're ready.</p>
    </div>'''

HUB_PLACEHOLDER = '''      <div class="blog-card">
        <div class="blog-card-body">
          <p class="blog-card-meta">Coming soon &middot; Tutorial</p>
          <h3>First posts are on the way</h3>
          <p>Hands-on guides, project walkthroughs, and the real story behind building this book with AI.</p>
        </div>
      </div>'''

def replace_between(text, start, end, replacement):
    pattern = re.compile(re.escape(start) + r'.*?' + re.escape(end), re.S)
    if not pattern.search(text):
        raise SystemExit('MARKER MISSING: %s ... %s' % (start, end))
    return pattern.sub(start + '\n' + replacement + '\n' + end, text)

def main():
    os.makedirs(OUTDIR, exist_ok=True)
    os.makedirs(PREVIEW, exist_ok=True)
    posts = []
    for fn in sorted(os.listdir(CONTENT)):
        if not fn.endswith('.md'):
            continue
        meta, body = parse_post(os.path.join(CONTENT, fn))
        slug = meta.get('slug', os.path.splitext(fn)[0])
        date = meta.get('date', '2026-01-01')
        try:
            date_disp = datetime.strptime(date, '%Y-%m-%d').strftime('%B %Y')
        except ValueError:
            date_disp = date
        sub = meta.get('subtitle', '')
        cta = ''
        if meta.get('download_url'):
            cta = CTA_TMPL.format(
                label=meta.get('download_label', 'Get the free tool'),
                url=meta['download_url'],
                button=meta.get('download_button', 'Download it free'))
        page = PAGE.format(
            title=meta.get('title', slug), excerpt=meta.get('excerpt', ''),
            slug=slug, site=SITE, date=date, date_disp=date_disp,
            category=meta.get('category', 'Tutorial'),
            subtitle_html=('<p class="post-subtitle">%s</p>' % sub) if sub else '',
            body=md_to_html(body), cta=cta, css=POST_CSS, nav=NAV, footer=FOOTER)
        status = meta.get('status', 'draft').lower()
        outdir = OUTDIR if status == 'published' else PREVIEW
        with open(os.path.join(outdir, slug + '.html'), 'w', encoding='utf-8') as f:
            f.write(page)
        print('%-9s %s' % (status.upper(), slug))
        if status == 'published':
            posts.append(dict(meta, slug=slug, date=date, date_disp=date_disp))

    posts.sort(key=lambda p: p['date'], reverse=True)
    cards = '\n'.join(CARD_TMPL.format(
        slug=p['slug'], date_disp=p['date_disp'],
        category=p.get('category', 'Tutorial'),
        title=p.get('title', ''), excerpt=p.get('excerpt', '')) for p in posts)

    idx = open(INDEX, encoding='utf-8').read()
    idx = replace_between(idx, '<!-- POSTS:START -->', '<!-- POSTS:END -->', cards)
    idx = replace_between(idx, '<!-- EMPTY:START -->', '<!-- EMPTY:END -->',
                          '' if posts else EMPTY_HTML)
    open(INDEX, 'w', encoding='utf-8').write(idx)

    hub_cards = '\n'.join(CARD_TMPL.format(
        slug=p['slug'], date_disp=p['date_disp'],
        category=p.get('category', 'Tutorial'),
        title=p.get('title', ''), excerpt=p.get('excerpt', '')) for p in posts[:3])
    hub = open(HUB, encoding='utf-8').read()
    hub = replace_between(hub, '<!-- HUBPOSTS:START -->', '<!-- HUBPOSTS:END -->',
                          hub_cards if posts else HUB_PLACEHOLDER)
    open(HUB, 'w', encoding='utf-8').write(hub)

    print('\n%d published post(s) on the index; drafts in _preview/creative-blog/' % len(posts))
    print('Deploy with: npx wrangler pages deploy site --project-name=marque-publishing --commit-dirty=true')

if __name__ == '__main__':
    main()
