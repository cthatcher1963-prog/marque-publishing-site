const fs = require('fs'), path = require('path');
const f = path.resolve(__dirname, '..', 'src', 'pages', 'blog.html');
let t = fs.readFileSync(f, 'utf8');
if (t.includes('.stream-grid {')) { console.log('already present'); process.exit(0); }
const css = `
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
`;
const i = t.indexOf('</style>');
t = t.slice(0, i) + css + t.slice(i);
fs.writeFileSync(f, t);
console.log('hub css inserted');
