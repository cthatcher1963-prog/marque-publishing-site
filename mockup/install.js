// mockup/install.js — promote the approved mockup into src/pages (source, with includes) and site/ (rendered).
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..');
const SRC = path.join(ROOT, 'src', 'pages'), SITE = path.join(ROOT, 'site'), PRE = path.join(ROOT, 'preview');
const ARCH = path.join(ROOT, '_archive', 'pre-redesign-2026-09-15');
fs.mkdirSync(ARCH, { recursive: true });
for (const f of ['index.html', 'labs.html']) {
  fs.copyFileSync(path.join(SRC, f), path.join(ARCH, 'src-' + f));
  fs.copyFileSync(path.join(SITE, f), path.join(ARCH, 'site-' + f));
}
// source (unrendered) versions
const idx = fs.readFileSync(path.join(SRC, 'index.html'), 'utf8');
const cut = idx.indexOf('<main id="main-content">');
fs.writeFileSync(path.join(SRC, 'index.html'), idx.slice(0, cut) + fs.readFileSync(path.join(__dirname, 'home-main.html'), 'utf8'));
let labs = fs.readFileSync(path.join(SRC, 'labs.html'), 'utf8');
const a = labs.indexOf('<!-- ─── Team callout ─── -->'), b = labs.indexOf('</main>');
const engineer = fs.readFileSync(path.join(__dirname, 'labs-engineer.html'), 'utf8');
const newsletter = `

<!-- ─── Newsletter ─── -->
<section class="newsletter section-pad">
  <div class="container">
    <div class="newsletter-inner fade-in">
      <h2>Stay in The Loop</h2>
      <p>Get notified when we launch &mdash; plus the free <em>Creating with Claude</em> toolkit.</p>
      <div class="ml-embedded" data-form="By4UIw"></div>
    </div>
  </div>
</section>
`;
fs.writeFileSync(path.join(SRC, 'labs.html'), labs.slice(0, a) + engineer + newsletter + labs.slice(b));
// rendered versions straight from the verified preview
fs.copyFileSync(path.join(PRE, 'index.html'), path.join(SITE, 'index.html'));
fs.copyFileSync(path.join(PRE, 'labs.html'), path.join(SITE, 'labs.html'));
// photo
fs.copyFileSync(path.join(__dirname, 'jayden.jpg'), path.join(SITE, 'jayden.jpg'));
fs.copyFileSync(path.join(__dirname, 'jayden.jpg'), path.join(ROOT, 'jayden.jpg'));
console.log('installed: src/pages + site/ index.html, labs.html, jayden.jpg; originals in', ARCH);
