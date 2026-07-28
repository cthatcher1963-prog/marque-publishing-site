#!/usr/bin/env node
/**
 * MARQUE DEPLOY GUARD - the ONLY sanctioned way to deploy marquepublishing.com
 *
 * Usage:
 *   npm run deploy        -> run all checks, then deploy the site/ folder
 *   npm run deploy:check  -> run all checks only (no deploy)
 *
 * WHY THIS EXISTS (incident 2026-07-28): a scheduled task deployed the project
 * ROOT, resurrecting the retired /site/ redirect and exposing private business
 * docs. This guard makes that class of mistake impossible to repeat silently.
 *
 * HARD RULES enforced here:
 *   1. Deploys ONLY the site/ folder. Takes no target argument.
 *   2. HALTS (exit 1) if anything references the retired /site URL space,
 *      if private/internal files are inside site/, if the root redirect stub
 *      reappears, or if any scheduled task contains a non-site deploy command.
 *   3. On a block: writes MARQUE-DEPLOY-BLOCKED.txt to the project root AND
 *      Chris's Desktop, and raises a Windows popup alert.
 *
 * AI AGENTS: if this guard blocks you, STOP. Fix the root cause or ask Chris.
 * Never invoke wrangler directly and never deploy any other folder.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const { execSync, spawn } = require('child_process');

const PROJECT = path.resolve(__dirname, '..');
const SITE = path.join(PROJECT, 'site');
const SCHEDULED = 'C:\\Users\\rctha\\Documents\\cowork_projects\\Scheduled';
const DESKTOP = 'C:\\Users\\rctha\\Desktop';
const ALERT_NAME = 'MARQUE-DEPLOY-BLOCKED.txt';
const CHECK_ONLY = process.argv.includes('--check');

const TEXT_EXT = new Set(['.html', '.htm', '.css', '.js', '.mjs', '.xml', '.txt', '.md', '.svg', '.json', '.webmanifest']);
const FORBIDDEN_EXT = new Set(['.docx', '.log', '.py', '.toml']);
const FORBIDDEN_BASE = new Set(['launch-plan.md', 'marketing-plan.md', 'mailerlite-setup.md',
  'social-posts.md', 'site-structure-proposal.md', 'claude.md', 'package.json',
  'zone.json', 'purge.json', 'pr.json', 'rs.json']);

const RX_OLD_URL = /marquepublishing\.(com|net)\/site/i;
const RX_ATTR_SITE = /(href|src|content|action|url)\s*[=:(]\s*["']?\/site\//i;
const RX_META_STUB = /http-equiv\s*=\s*["']refresh["'][^>]*\/site/i;
const RX_BAD_DEPLOY = /pages\s+deploy(?!\s+site\b)/i;

const violations = [];
const bad = (msg) => violations.push(msg);

function walk(dir, fn) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, fn);
    else fn(p);
  }
}

// ---- Check 1: deploy target sanity -----------------------------------------
if (!fs.existsSync(path.join(SITE, 'index.html')))
  bad('site/index.html is missing - empty or wrong deploy folder.');
if (fs.existsSync(path.join(PROJECT, 'index.html')))
  bad('index.html exists at the PROJECT ROOT - the old /site redirect stub landmine is back. Delete it.');

// ---- Check 2: wrangler.toml still pins the site folder ---------------------
try {
  const toml = fs.readFileSync(path.join(PROJECT, 'wrangler.toml'), 'utf8');
  if (!/pages_build_output_dir\s*=\s*"site"/.test(toml))
    bad('wrangler.toml no longer pins pages_build_output_dir = "site".');
} catch (e) {
  bad('wrangler.toml is missing from the project root.');
}

// ---- Check 3: scan deployable content (site/) ------------------------------
walk(SITE, (p) => {
  const rel = path.relative(PROJECT, p);
  const base = path.basename(p).toLowerCase();
  const ext = path.extname(p).toLowerCase();
  if (base === '_redirects') return; // legit: the rules that redirect OFF /site
  if (FORBIDDEN_BASE.has(base)) return bad('Private/internal file inside site/: ' + rel);
  if (FORBIDDEN_EXT.has(ext)) return bad('Forbidden file type (' + ext + ') inside site/: ' + rel);
  if (!TEXT_EXT.has(ext)) return;
  let text; try { text = fs.readFileSync(p, 'utf8'); } catch (e) { return; }
  if (RX_OLD_URL.test(text)) bad('Retired /site URL referenced in ' + rel);
  if (RX_ATTR_SITE.test(text)) bad('Link/asset points into /site/ in ' + rel);
  if (RX_META_STUB.test(text)) bad('Meta-refresh redirect to /site in ' + rel);
});

// ---- Check 4: scheduled-task canary ----------------------------------------
try {
  walk(SCHEDULED, (p) => {
    if (!p.toLowerCase().endsWith('.md')) return;
    const rel = 'Scheduled\\' + path.relative(SCHEDULED, p);
    let text; try { text = fs.readFileSync(p, 'utf8'); } catch (e) { return; }
    if (RX_BAD_DEPLOY.test(text))
      bad('Scheduled task has a deploy command whose target is not "site": ' + rel);
    if (RX_OLD_URL.test(text))
      bad('Scheduled task references the retired /site URL space: ' + rel);
  });
} catch (e) {
  bad('Could not scan the Scheduled tasks folder: ' + e.message);
}

function writeAlerts() {
  const body = ['MARQUE DEPLOY GUARD - DEPLOY BLOCKED', 'Time: ' + new Date().toString(), '',
    'A deploy/check was HALTED. NOTHING WAS DEPLOYED.',
    'Something references the retired /site URL space or would expose private files.', '',
    'Violations:'].concat(violations.map((v) => '  - ' + v)).concat(['',
    'Fix the causes above, then rerun: npm run deploy',
    'AI agents: do NOT bypass this guard and do NOT call wrangler directly.']).join('\r\n');
  fs.writeFileSync(path.join(PROJECT, ALERT_NAME), body);
  try { if (fs.existsSync(DESKTOP)) fs.writeFileSync(path.join(DESKTOP, ALERT_NAME), body); } catch (e) {}
  try {
    const msg = 'Marque deploy BLOCKED - ' + violations.length + ' violation(s). Nothing was deployed. See ' + ALERT_NAME + ' on your Desktop.';
    spawn('powershell.exe', ['-NoProfile', '-WindowStyle', 'Hidden', '-Command',
      "(New-Object -ComObject WScript.Shell).Popup('" + msg + "',600,'MARQUE DEPLOY GUARD',4144)"],
      { detached: true, stdio: 'ignore' }).unref();
  } catch (e) {}
}

// ---- Verdict ---------------------------------------------------------------
if (violations.length) {
  writeAlerts();
  console.error('\n' + '='.repeat(72));
  console.error('GUARD ALERT - DEPLOY BLOCKED - ' + violations.length + ' violation(s). NOTHING WAS DEPLOYED.');
  console.error('='.repeat(72));
  violations.forEach((v) => console.error('  - ' + v));
  console.error('='.repeat(72));
  console.error('Alert file written to Desktop (' + ALERT_NAME + ') and popup raised.');
  console.error('AI agents: STOP HERE. Do not bypass. Do not call wrangler directly.');
  console.error('='.repeat(72) + '\n');
  process.exit(1);
}

for (const dir of [PROJECT, DESKTOP]) {
  try { fs.unlinkSync(path.join(dir, ALERT_NAME)); } catch (e) {}
}
console.log('DEPLOY GUARD: all checks passed (site/ clean, no /site refs, scheduled tasks clean).');

if (CHECK_ONLY) {
  console.log('Check-only mode: no deploy performed.');
  process.exit(0);
}

console.log('Deploying site/ ...');
execSync('npx wrangler pages deploy site --project-name=marque-publishing --commit-dirty=true',
  { cwd: PROJECT, stdio: 'inherit' });
console.log('DEPLOY GUARD: deploy complete.');
