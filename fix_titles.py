import re, os, sys

REVISED_DIR = r'C:\Users\rctha\AppData\Roaming\Claude\local-agent-mode-sessions\1d8055c6-7760-4d78-9d4a-314605eeca68\b85c7b8f-0ffe-443c-b9fa-e73078c253ab\local_546b18e4-e69a-4b30-b574-c9cc9e460eaa\outputs'
BLOG_DIR = r'C:\Users\rctha\Documents\cowork_projects\13_Marque_Publishing_Website\site\blog'
BLOG_HTML = r'C:\Users\rctha\Documents\cowork_projects\13_Marque_Publishing_Website\site\blog.html'

MAPPING = {
    'post01-squidbleed-revised.md': 'squidbleed.html',
    'post02-jetbrains-supply-chain-revised.md': 'jetbrains-supply-chain.html',
    'post03-fortibleed-revised.md': 'fortibleed.html',
    'post04-compliance-deadline-revised.md': 'compliance-deadline.html',
    'post05-boards-failing-cyber-revised.md': 'boards-failing-cyber.html',
    'post06-ciso-liability-revised.md': 'ciso-liability.html',
    'post07-lost-in-translation-revised.md': 'lost-in-translation.html',
    'post08-ai-executive-order-revised.md': 'ai-executive-order.html',
    'post09-wild-west-of-ai-revised.md': 'wild-west-of-ai.html',
    'post10-ai-risk-in-healthcare-revised.md': 'ai-risk-in-healthcare.html',
}

def extract_title(md_text):
    for line in md_text.strip().split('\n'):
        if line.startswith('# '):
            return line[2:].strip()
    return None

def extract_body(md_text):
    lines = md_text.strip().split('\n')
    found = False
    body = []
    for line in lines:
        if not found and line.startswith('# '):
            found = True
            continue
        if found:
            body.append(line)
    return '\n'.join(body).strip()

def convert_inline(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', text)
    return text

def md_to_html(body_md):
    lines = body_md.split('\n')
    parts = []
    first_para = True
    current_para = []
    def flush():
        nonlocal first_para, current_para
        if not current_para:
            return
        text = convert_inline(' '.join(current_para))
        if first_para:
            parts.append('      <p class="lead">' + text + '</p>')
            first_para = False
        else:
            parts.append('      <p>' + text + '</p>')
        current_para = []
    for line in lines:
        s = line.strip()
        if not s:
            flush()
            continue
        if s.startswith('## '):
            flush()
            parts.append('')
            parts.append('      <h2>' + convert_inline(s[3:]) + '</h2>')
            continue
        if s.startswith('### '):
            flush()
            parts.append('')
            parts.append('      <h3>' + convert_inline(s[4:]) + '</h3>')
            continue
        current_para.append(s)
    flush()
    return '\n'.join(parts)

# Process each blog post HTML file
for md_file, html_file in MAPPING.items():
    md_path = os.path.join(REVISED_DIR, md_file)
    html_path = os.path.join(BLOG_DIR, html_file)
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    new_title = extract_title(md_content)
    body_md = extract_body(md_content)
    body_html = md_to_html(body_md)
    # Replace article-prose content
    pattern = r'(<div class="article-prose fade-in">)\s*\n.*?(\s*</div>\s*\n+\s*\n*\s*<!--)'
    replacement = '\\1\n' + body_html + '\n    \n    \\2'
    new_html, cnt = re.subn(pattern, replacement, html_content, count=1, flags=re.DOTALL)
    if cnt == 0:
        print(f"WARN: article-prose not matched for {html_file}", flush=True)
    # Update h1, title, og:title
    if new_title:
        new_html = re.sub(r'<h1>.*?</h1>', '<h1>' + new_title + '</h1>', new_html, count=1)
        new_html = re.sub(r'<title>.*?</title>', '<title>' + new_title + ' \\u2014 Marque Publishing</title>', new_html, count=1)
        og_esc = new_title.replace('"', '&quot;')
        new_html = re.sub(r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="' + og_esc + '">', new_html, count=1)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    # Verify
    with open(html_path, 'r', encoding='utf-8') as f:
        verify = f.read()
    h1m = re.search(r'<h1>(.*?)</h1>', verify)
    actual = h1m.group(1) if h1m else 'NOT FOUND'
    status = 'OK' if actual == new_title else 'MISMATCH'
    print(f"{status} {html_file}: {actual[:70]}", flush=True)

# Update blog.html listing page
print("\nUpdating blog.html...", flush=True)
with open(BLOG_HTML, 'r', encoding='utf-8') as f:
    blog_content = f.read()

for md_file, html_file in MAPPING.items():
    md_path = os.path.join(REVISED_DIR, md_file)
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    new_title = extract_title(md_content)
    # Update blog card h3
    card_pat = r'(href="blog/' + re.escape(html_file) + r'".*?<h3>)(.*?)(</h3>)'
    blog_content = re.sub(card_pat, r'\g<1>' + new_title + r'\3', blog_content, flags=re.DOTALL)
    # Update structured data headline
    sd_pat = r'("headline": ")(.*?)("[\s\S]*?"url": "https://www\.marquepublishing\.com/site/blog/' + re.escape(html_file) + r'")'
    blog_content = re.sub(sd_pat, r'\g<1>' + new_title + r'\3', blog_content, flags=re.DOTALL)

with open(BLOG_HTML, 'w', encoding='utf-8') as f:
    f.write(blog_content)
print("blog.html updated.", flush=True)
print("\nAll done!", flush=True)
