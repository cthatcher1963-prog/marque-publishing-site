# fix_urls.py - restructure URLs: /site/*.html -> root-level clean URLs
import os, re, sys, posixpath

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, 'site')
APPLY = len(sys.argv) > 1 and sys.argv[1] == 'apply'
DOMAIN = 'https://www.marquepublishing.com'

mappings = {}
missing = set()

def transform_path(p):
    if p.startswith('site/'):
        p = p[len('site/'):]
    elif p == 'site':
        p = ''
    if p.endswith('index.html'):
        p = p[:-len('index.html')]
    elif p.endswith('.html'):
        p = p[:-len('.html')]
    return '/' + p

def split_extra(u):
    frag = ''
    q = ''
    if '#' in u:
        u, f = u.split('#', 1)
        frag = '#' + f
    if '?' in u:
        u, qq = u.split('?', 1)
        q = '?' + qq
    return u, q, frag

def check_exists(webpath):
    p = webpath.lstrip('/')
    if p == '':
        return True
    full = os.path.join(ROOT, *p.split('/'))
    if os.path.isfile(full):
        return True
    if os.path.isfile(full + '.html'):
        return True
    if os.path.isdir(full) and os.path.isfile(os.path.join(full, 'index.html')):
        return True
    return False

ABS_RE = re.compile(r'https://www\.marquepublishing\.com/[^"\'\s<>)]*')
REL_RE = re.compile(r'\b(href|src)=(["\'])([^"\']*)\2')
SKIP = ('http://', 'https://', '//', '#', 'mailto:', 'tel:', 'javascript:', 'data:')

def fix_abs(m):
    url = m.group(0)
    path, q, frag = split_extra(url[len(DOMAIN) + 1:])
    newp = transform_path(path)
    new = DOMAIN + newp + q + frag
    if new != url:
        mappings[url] = new
    if not check_exists(newp):
        missing.add(new)
    return new

def make_fix_rel(fdir):
    def fix_rel(m):
        attr, quote, url = m.group(1), m.group(2), m.group(3)
        if url == '' or url.startswith(SKIP) or url.startswith('/'):
            return m.group(0)
        path, q, frag = split_extra(url)
        if path == '':
            return m.group(0)
        r = posixpath.normpath(posixpath.join(fdir, path))
        while r.startswith('../'):
            r = r[3:]
        if r in ('..', '.'):
            r = ''
        if path.endswith('/') and r != '':
            webpath = '/' + r + '/'
        elif r.endswith('.html'):
            webpath = transform_path(r)
        else:
            webpath = '/' + r
        if not check_exists(webpath) and r.endswith('.html'):
            alt = transform_path(posixpath.basename(r))
            if check_exists(alt):
                webpath = alt
        new = attr + '=' + quote + webpath + q + frag + quote
        if new != m.group(0):
            mappings[url + '  [in ' + (fdir or 'root') + ']'] = webpath + q + frag
        if not check_exists(webpath):
            missing.add(webpath)
        return new
    return fix_rel

count_files = 0
for dirpath, dirs, files in os.walk(ROOT):
    for fn in files:
        if not fn.endswith('.html'):
            continue
        fp = os.path.join(dirpath, fn)
        rel = os.path.relpath(fp, ROOT).replace(os.sep, '/')
        fdir = posixpath.dirname(rel)
        with open(fp, 'r', encoding='utf-8') as f:
            orig = f.read()
        txt = ABS_RE.sub(fix_abs, orig)
        txt = REL_RE.sub(make_fix_rel(fdir), txt)
        if txt != orig:
            count_files += 1
            print(('WOULD CHANGE: ' if not APPLY else 'CHANGED: ') + rel)
            if APPLY:
                with open(fp, 'w', encoding='utf-8', newline='') as f:
                    f.write(txt)

print()
print(('APPLIED' if APPLY else 'DRY RUN') + ': %d files changed' % count_files)
print()
print('Unique URL transformations (%d):' % len(mappings))
for k in sorted(mappings):
    print('  %s  ->  %s' % (k, mappings[k]))
print()
if missing:
    print('MISSING TARGETS:')
    for t in sorted(missing):
        print('  ' + t)
else:
    print('All rewritten link targets exist locally. OK')
