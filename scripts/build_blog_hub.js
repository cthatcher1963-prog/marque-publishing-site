// scripts/build_blog_hub.js — regenerate the /blog hub from the two stream indexes.
//   Cybersecurity stream index : site/blog/cybersecurity/index.html   (cards inside .blog-grid)
//   Creating with AI index     : site/creating-with-claude/blog.html   (cards inside .blog-grid)
// Template: src/pages/blog.html (has <!-- HUB:START --> … <!-- HUB:END --> markers).
// Output  : site/blog.html (rendered) AND src/pages/blog.html (template with markers refilled),
//           so scripts/sync-src-from-site.js stays byte-exact.
// Run after ANY post is added to either stream:  node scripts/build_blog_hub.js
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..');
const SITE = path.join(ROOT, 'site'), SRC = path.join(ROOT, 'src', 'pages'), PART = path.join(ROOT, 'build', 'partials');

const p = n => fs.readFileSync(path.join(PART, n + '.html'), 'utf8');
const NAV = p('nav'), FOOTER = p('footer'), ML = p('mailerlite'), SCRIPTS = p('scripts');
const NAV_ITEMS = { home: ['/', 'Home'], books: ['/books', 'Books'], about: ['/about', 'About'], blog: ['/blog', 'Blog'], labs: ['/labs', 'Labs'] };
const navFor = a => { if (!a || !NAV_ITEMS[a]) return NAV; const [h, l] = NAV_ITEMS[a]; return NAV.replace(`<a href="${h}">${l}</a>`, `<a href="${h}" class="active">${l}</a>`); };
const render = h => h.replace(/<!--#include nav(?: active="([a-z]+)")?-->/g, (_, a) => navFor(a))
  .split('<!--#include footer-->').join(FOOTER).split('<!--#include mailerlite-->').join(ML).split('<!--#include scripts-->').join(SCRIPTS);

function cards(file) {
  const html = fs.readFileSync(file, 'utf8');
  const re = /<a href="([^"]+)" class="blog-card">\s*<div class="blog-card-body">\s*<p class="blog-card-meta">([\s\S]*?)<\/p>\s*<h3>([\s\S]*?)<\/h3>\s*<p>([\s\S]*?)<\/p>/g;
  const out = []; let m;
  while ((m = re.exec(html))) out.push({ href: m[1], meta: m[2].trim(), title: m[3].trim(), desc: m[4].trim() });
  if (!out.length) throw new Error('no cards parsed from ' + file);
  return out;
}
const cyber = cards(path.join(SITE, 'blog', 'cybersecurity', 'index.html'));
const ai = cards(path.join(SITE, 'creating-with-claude', 'blog.html'));

const card = (c, stream) => `      <a href="${c.href}" class="blog-card">
        <div class="blog-card-body">
          <p class="blog-card-meta">${c.meta.replace(/&middot;.*$/, '&middot; ' + stream)}</p>
          <h3>${c.title}</h3>
          <p>${c.desc}</p>
          <span class="blog-card-link">Read more &rarr;</span>
        </div>
      </a>`;

const streamCard = (name, kicker, desc, latest, href, count, soon) => `      <div class="stream-card fade-in">
        <p class="section-kicker">${kicker}</p>
        <h2>${name}</h2>
        <p class="stream-desc">${desc}</p>
${soon ? `        <p class="stream-soon">Coming soon</p>` : `        <a href="${latest.href}" class="stream-latest">
          <span class="stream-latest-label">Latest</span>
          <span class="stream-latest-title">${latest.title}</span>
          <span class="stream-latest-meta">${latest.meta.replace(/\s*&middot;.*$/, '')}</span>
        </a>
        <a href="${href}" class="btn-outline">All ${count} posts &rarr;</a>`}
      </div>`;

// Latest across both streams: alternate newest cyber / newest AI, six cards
const mixed = [];
for (let i = 0; i < 3; i++) { if (cyber[i]) mixed.push(card(cyber[i], 'Cybersecurity')); if (ai[i]) mixed.push(card(ai[i], 'Creating with AI')); }

const filled = `<!-- HUB:START -->
    <div class="stream-grid">
${streamCard('Cybersecurity', 'For boards and executives', 'Thirty years in the field, applied to this week\'s breach, patch, or regulation. What it means for the people who sign the risk acceptance form.', cyber[0], '/blog/cybersecurity/', cyber.length, false)}
${streamCard('Creating with AI', 'For makers', 'Essays, free tools, and lessons from building real things with Claude &mdash; books, software, and the occasional poker app.', ai[0], '/creating-with-claude/blog', ai.length, false)}
${streamCard('Writing with AI', 'For writers', 'Your voice on the page, with Claude as the assistant and never the author. Starts when <em>Writing with Claude</em> ships.', null, '/writing-with-claude/', 0, true)}
    </div>

    <div class="section-header fade-in" style="margin-top: 4rem;">
      <p class="section-kicker">Latest</p>
      <h2>New This Month</h2>
    </div>
    <div class="blog-grid fade-in">
${mixed.join('\n')}
    </div>
<!-- HUB:END -->`;

const tplPath = path.join(SRC, 'blog.html');
let tpl = fs.readFileSync(tplPath, 'utf8');
const a = tpl.indexOf('<!-- HUB:START -->'), b = tpl.indexOf('<!-- HUB:END -->');
if (a < 0 || b < 0) throw new Error('HUB markers missing in src/pages/blog.html');
tpl = tpl.slice(0, a) + filled + tpl.slice(b + '<!-- HUB:END -->'.length);
fs.writeFileSync(tplPath, tpl);
fs.writeFileSync(path.join(SITE, 'blog.html'), render(tpl));
console.log(`blog hub built: ${cyber.length} cyber posts, ${ai.length} AI posts, ${mixed.length} in the latest grid`);
