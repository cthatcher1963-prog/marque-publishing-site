#!/usr/bin/env node
// scripts/sync-src-from-site.js -- keep src/pages in lockstep with site/
//
// WHY: the daily blog publisher edits site/ pages directly (blog.html,
// index.html). src/pages drifts behind, and the next `npm run build` would
// overwrite site/ with stale src -- wiping live blog posts off the index
// (near-miss discovered 2026-08-10: src was ~3 weeks / 40+ posts behind).
//
// WHAT: for every .html in src/pages, render it with the partials exactly
// like build.js does and compare to the site/ counterpart. If site/ is
// different, back-port the site copy into src (collapsing nav/footer/
// mailerlite/scripts back into <!--#include --> directives). src is only
// overwritten when re-rendering the new src reproduces the live file
// byte-for-byte; anything that can't round-trip is flagged for manual review.
//
// RUN: node scripts/sync-src-from-site.js   (safe to run any time;
// the daily publish task runs it after editing site/ pages)
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SRC = path.join(ROOT, 'src', 'pages');
const SITE = path.join(ROOT, 'site');
const PARTIALS = path.join(ROOT, 'build', 'partials');

const partial = (n) => fs.readFileSync(path.join(PARTIALS, n + '.html'), 'utf8');
const NAV = partial('nav');
const FOOTER = partial('footer');
const MAILERLITE = partial('mailerlite');
const SCRIPTS = partial('scripts');

const NAV_ITEMS = {
  home:  ['/', 'Home'],
  books: ['/books', 'Books'],
  about: ['/about', 'About'],
  blog:  ['/blog', 'Blog'],
  labs:  ['/labs', 'Labs'],
};

function navFor(active) {
  if (!active || !NAV_ITEMS[active]) return NAV;
  const [href, label] = NAV_ITEMS[active];
  return NAV.replace(`<a href="${href}">${label}</a>`,
                     `<a href="${href}" class="active">${label}</a>`);
}

// identical to build/build.js render()
function render(html) {
  html = html.replace(/<!--#include nav(?: active="([a-z]+)")?-->/g, (_, a) => navFor(a));
  html = html.split('<!--#include footer-->').join(FOOTER);
  html = html.split('<!--#include mailerlite-->').join(MAILERLITE);
  html = html.split('<!--#include scripts-->').join(SCRIPTS);
  return html;
}

// reverse of render(): collapse expanded partials back into include tags
function unrender(html) {
  let out = html;
  let navDone = false;
  for (const k of Object.keys(NAV_ITEMS)) {
    const v = navFor(k);
    if (v !== NAV && out.includes(v)) {
      out = out.split(v).join(`<!--#include nav active="${k}"-->`);
      navDone = true;
      break;
    }
  }
  if (!navDone && out.includes(NAV)) {
    out = out.split(NAV).join('<!--#include nav-->');
    navDone = true;
  }
  out = out.split(FOOTER).join('<!--#include footer-->');
  out = out.split(MAILERLITE).join('<!--#include mailerlite-->');
  out = out.split(SCRIPTS).join('<!--#include scripts-->');
  return { out, navDone };
}

function* walk(dir, rel = '') {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const abs = path.join(dir, e.name), r = path.join(rel, e.name);
    if (e.isDirectory()) yield* walk(abs, r);
    else if (e.name.endsWith('.html')) yield r;
  }
}

let clean = 0, synced = 0;
const manual = [];

for (const rel of walk(SRC)) {
  const srcP = path.join(SRC, rel), siteP = path.join(SITE, rel);
  if (!fs.existsSync(siteP)) { manual.push(rel + '  (no site/ counterpart)'); continue; }
  const rendered = render(fs.readFileSync(srcP, 'utf8'));
  const live = fs.readFileSync(siteP, 'utf8');
  if (rendered === live) { clean++; continue; }
  const { out, navDone } = unrender(live);
  if (!navDone) { manual.push(rel + '  (nav partial not found in site copy)'); continue; }
  if (render(out) !== live) { manual.push(rel + '  (round-trip mismatch)'); continue; }
  fs.writeFileSync(srcP, out);
  synced++;
  console.log('SYNCED  src/pages/' + rel.replace(/\\/g, '/') + '  (site copy was newer)');
}

console.log('');
console.log('Done. ' + clean + ' in sync, ' + synced + ' back-ported from site/.');
if (manual.length) {
  console.log('NEEDS MANUAL REVIEW (src NOT touched):');
  manual.forEach((m) => console.log('  - ' + m));
  process.exitCode = 1;
}
