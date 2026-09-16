// One-off (2026-09-15): split /blog into a hub + /blog/cybersecurity/ stream index.
// 1. src/pages/blog/cybersecurity/index.html  <- today's src/pages/blog.html with the AI banner removed,
//    hero retitled, newsletter = Executives guide form.  Rendered to site/blog/cybersecurity/index.html.
// 2. src/pages/blog.html  <- hub template (page hero + HUB markers + newsletter). build_blog_hub.js fills it.
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..');
const SITE = path.join(ROOT, 'site'), SRC = path.join(ROOT, 'src', 'pages'), PART = path.join(ROOT, 'build', 'partials');
const p = n => fs.readFileSync(path.join(PART, n + '.html'), 'utf8');
const NAV = p('nav'), FOOTER = p('footer'), ML = p('mailerlite'), SCRIPTS = p('scripts');
const NAV_ITEMS = { home: ['/', 'Home'], books: ['/books', 'Books'], about: ['/about', 'About'], blog: ['/blog', 'Blog'], labs: ['/labs', 'Labs'] };
const navFor = a => { if (!a || !NAV_ITEMS[a]) return NAV; const [h, l] = NAV_ITEMS[a]; return NAV.replace(`<a href="${h}">${l}</a>`, `<a href="${h}" class="active">${l}</a>`); };
const render = h => h.replace(/<!--#include nav(?: active="([a-z]+)")?-->/g, (_, a) => navFor(a))
  .split('<!--#include footer-->').join(FOOTER).split('<!--#include mailerlite-->').join(ML).split('<!--#include scripts-->').join(SCRIPTS);

const ARCH = path.join(ROOT, '_archive', 'pre-redesign-2026-09-15');
fs.mkdirSync(ARCH, { recursive: true });
fs.copyFileSync(path.join(SRC, 'blog.html'), path.join(ARCH, 'src-blog.html'));
fs.copyFileSync(path.join(SITE, 'blog.html'), path.join(ARCH, 'site-blog.html'));

const src = fs.readFileSync(path.join(SRC, 'blog.html'), 'utf8');
const must = (s, label) => { if (src.indexOf(s) < 0) throw new Error('missing: ' + label); };

// ---------- 1. Cybersecurity stream index ----------
let cyber = src;
// head: title / description / canonical / og
cyber = cyber.replace(/<title>[^<]*<\/title>/, '<title>Cybersecurity Blog — Marque Publishing</title>');
cyber = cyber.replace(/<meta name="description" content="[^"]*">/, '<meta name="description" content="Cybersecurity for boards and executives: thirty years in the field applied to this week\'s breach, patch, or regulation. From Chris Thatcher, author of Cyber Risk is Business Risk.">');
cyber = cyber.replace(/https:\/\/www\.marquepublishing\.com\/blog"/g, 'https://www.marquepublishing.com/blog/cybersecurity/"');
cyber = cyber.replace(/<meta property="og:title" content="[^"]*">/, '<meta property="og:title" content="Cybersecurity Blog — Marque Publishing">');
cyber = cyber.replace(/<meta name="twitter:title" content="[^"]*">/, '<meta name="twitter:title" content="Cybersecurity Blog — Marque Publishing">');
// hero
must('<p class="section-kicker">From the desk</p>\n  <h1>Blog</h1>', 'hero');
cyber = cyber.replace('<p class="section-kicker">From the desk</p>\n  <h1>Blog</h1>\n  <p>Cybersecurity insights from 30 years in the field, the publishing journey, and whatever else won\'t leave us alone.</p>',
  '<p class="section-kicker"><a href="/blog" style="color: inherit;">Thinking out loud</a> &middot; Cybersecurity</p>\n  <h1>Cybersecurity</h1>\n  <p>Thirty years in the field, applied to this week\'s breach, patch, or regulation &mdash; and what it means for the people who sign the risk acceptance form.</p>');
// remove the AI cross-link banner
const bA = cyber.indexOf('    <!-- ─── AI Blog Cross-Link ─── -->'), bB = cyber.indexOf('    <!-- ─── Posts ─── -->');
if (bA < 0 || bB < 0) throw new Error('banner markers');
cyber = cyber.slice(0, bA) + cyber.slice(bB);
// newsletter -> the guide (Executives)
must('<h2>Start Creating With Claude</h2>', 'newsletter');
cyber = cyber.replace('<h2>Start Creating With Claude</h2>\n      <p>Sign up and get the free <em>Creating with Claude</em> toolkit &mdash; plus new posts delivered to your inbox.</p>\n      <div class="ml-embedded" data-form="By4UIw"></div>',
  '<h2>Get The Free Guide</h2>\n      <p>Sign up and get <em>10 Cybersecurity Decisions Every Board Gets Wrong</em> &mdash; plus new posts delivered to your inbox.</p>\n      <div class="ml-embedded" data-form="xmtcNh"></div>');
fs.mkdirSync(path.join(SRC, 'blog', 'cybersecurity'), { recursive: true });
fs.mkdirSync(path.join(SITE, 'blog', 'cybersecurity'), { recursive: true });
fs.writeFileSync(path.join(SRC, 'blog', 'cybersecurity', 'index.html'), cyber);
fs.writeFileSync(path.join(SITE, 'blog', 'cybersecurity', 'index.html'), render(cyber));

// ---------- 2. Hub template ----------
let hub = src;
hub = hub.replace(/<meta name="description" content="[^"]*">/, '<meta name="description" content="The Marque Publishing blog: cybersecurity for boards and executives, creating real things with AI, and writing with AI. Two streams today, a third on the way.">');
hub = hub.replace('<p class="section-kicker">From the desk</p>\n  <h1>Blog</h1>\n  <p>Cybersecurity insights from 30 years in the field, the publishing journey, and whatever else won\'t leave us alone.</p>',
  '<p class="section-kicker">Thinking out loud</p>\n  <h1>Blog</h1>\n  <p>Two blogs, one desk. Cybersecurity for the people who carry the risk, and building real things with AI for the people who want to. A third, for writers, is on the way.</p>');
// replace everything from the AI banner through the end of the posts grid with the HUB markers
const hA = hub.indexOf('    <!-- ─── AI Blog Cross-Link ─── -->');
const hB = hub.indexOf('    <!-- ─── Empty state for additional posts ─── -->');
if (hA < 0 || hB < 0) throw new Error('hub markers');
hub = hub.slice(0, hA) + '<!-- HUB:START -->\n<!-- HUB:END -->\n' + hub.slice(hB);
// hub styles
hub = hub.replace('</style>\n</head>', `
/* ─── Blog hub (2026-09-15) ─── */
.stream-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.75rem; max-width: 66rem; margin-inline: auto; }
.stream-card { background: var(--card-bg); border-radius: 12px; box-shadow: var(--card-shadow); padding: 2rem 1.75rem; display: flex; flex-direction: column; }
.stream-card h2 { font-family: var(--serif); font-size: 1.6rem; font-weight: 600; margin: 0.25rem 0 0.5rem; }
.stream-card .stream-desc { color: var(--text-muted); line-height: 1.6; margin-bottom: 1.25rem; }
.stream-latest { display: block; background: var(--bg-alt); border-radius: 8px; padding: 0.9rem 1rem; margin-bottom: 1.25rem; text-decoration: none; flex: 1; }
.stream-latest:hover .stream-latest-title { color: var(--accent); }
.stream-latest-label { display: block; font-family: var(--sans); font-size: 0.7rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: var(--accent); margin-bottom: 0.3rem; }
.stream-latest-title { display: block; font-family: var(--serif); font-size: 1.1rem; font-weight: 600; color: var(--text); line-height: 1.3; transition: color 0.2s; }
.stream-latest-meta { display: block; font-size: 0.8rem; color: var(--text-subtle); margin-top: 0.3rem; }
.stream-soon { font-family: var(--sans); font-size: 0.85rem; font-weight: 600; color: var(--text-subtle); margin-top: auto; }
.stream-card .btn-outline { align-self: flex-start; }
@media (max-width: 860px) { .stream-grid { grid-template-columns: 1fr; max-width: 28rem; } }
</style>
</head>`);
fs.writeFileSync(path.join(SRC, 'blog.html'), hub);
console.log('restructured: cyber index + hub template written. Now run build_blog_hub.js');
