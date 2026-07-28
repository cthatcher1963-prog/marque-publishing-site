# Marque Publishing Website — operating guide (for Claude)

This project **owns marquepublishing.com and marquepublishing.net**. I (Claude) own all tech
decisions, publishing, and maintenance for the site. Chris is the author/owner; I drive the build.

## What this is
A static, hand-crafted site deployed on **Cloudflare Pages** (serves the `site/` folder directly;
`wrangler.toml` sets `pages_build_output_dir = "site"`). Fonts: Cormorant / EB Garamond / Inter.
Design tokens + shared classes live in `site/css/style.css`. MailerLite (account 2453958,
form `NTW6JI`) handles the newsletter + the "10 Cybersecurity Decisions" lead magnet.

## Build system (added 2026-07-08) — READ THIS BEFORE EDITING
Light include-based build to kill nav/footer/tracking duplication.
- `build/partials/` — single source for shared blocks: `nav.html`, `footer.html`,
  `mailerlite.html`, `scripts.html`.
- `build/build.js` — walks `src/pages/`, expands `<!--#include nav active="x"-->`,
  `<!--#include footer-->`, `<!--#include mailerlite-->`, `<!--#include scripts-->`,
  writes finished HTML to `site/`.
- `build/refactor.js` — one-time codemod that generated the partials + src pages. Do NOT re-run.
- `package.json`: `npm run build` (regenerate), `npm run deploy` (build + `wrangler pages deploy`).

**CRITICAL — which file to edit:**
- Pages in `src/pages/` (index, books, about, blog, labs, 404, cyber-risk/) → edit the
  `src/pages/` copy. `npm run build` OVERWRITES the matching `site/` file.
- Pages NOT yet converted (blog posts under `site/blog/`, `site/creating-with-claude/`,
  `site/calculator/`) → still edited directly in `site/`.
- Nav active state: pass `active="home|books|about|blog|labs"` in the include; `nav.html` is stored
  without any active class.

## Deploy
`npm run build` then deploy the `site/` folder via wrangler on Chris's machine (Desktop Commander).
Local preview: `cd site && python -m http.server 8123` → http://localhost:8123/ (absolute asset
paths need a server; file:// won't work).

## Book roster
- **Creating with Claude** — releases 2026-07-18. Full page `site/creating-with-claude/index.html`
  (NOT yet in the build system). Shopify buy buttons live ($24.99 + $34.99 products).
- **Cyber Risk is Business Risk** — releases 2026-07-18. Page `src/pages/cyber-risk/index.html`.
  Buy buttons are a "Notify me" capture until Nam's cover wrap → Lulu/KDP upload → Shopify product,
  then swap in Buy Buttons (mirror the CWC page).
- **The Treasure Hunter's Legacy** — in progress. Catalog card only.
- **Deal Me In** — on the way. Catalog card only.

## Open work (see the task list / MEMORY)
1. Centralize book blurbs into one data source (still duplicated across home/books/detail/JSON-LD).
2. Roll the include system out to blog posts, creating-with-claude/, calculator/.
3. Wire Cyber Risk buy buttons once the product is live.

## House rules
- Never deploy the project root — it holds private business docs. Only `site/` ships.
- Chris does not use OneDrive; never reference it.
- Check CSS (object-fit, scaling) before blaming image resolution.
