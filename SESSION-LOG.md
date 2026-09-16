# SESSION-LOG — Marque Publishing Website

Continuity log for the Marque Publishing author website (Cloudflare Pages,
git: cthatcher1963-prog/marque-publishing-site). Created 2026-08-06 by the
session-harvester -- no prior SESSION-LOG existed for this project despite
active engineering work; see the project description in projects_data.json
for earlier history (Amazon buy links, Shopify removal, cover updates).

---

## 2026-08-06 (harvested) — Cache-purge fix validated; false-alarm break diagnosed

Two sessions processed this harvest (exact dates not visible in the transcript
window; both predate this harvest date):

**Cache-purge deploy guard.** Created a scoped Cloudflare API token (Cache
Purge only, marquepublishing.com zone only), stored outside the deployable
project tree at `~/.marque/cache-purge-token`, wired into `scripts/deploy-guard.js`
so every successful deploy auto-purges the edge cache. Tested end-to-end.
Closes the 7/28 CSS-cache class of bug. This is the source session behind the
"self-healing deploy pipeline" already on record in projects_data.json.

**Follow-up false alarm.** A reported site rendering break (missing header/nav
styling) traced to the browser having cached a stale Cloudflare 503 response
for `/css/style.css` -- not a real break. Server-side edge cache had already
expired correctly; a hard refresh (Ctrl+Shift+R) resolved it in both Chrome
and Brave. Confirms the cache-purge fix above is working as designed; the
redeploy performed during triage was unnecessary.

Next action: none outstanding from these two sessions. Known open item
elsewhere on record: MailerLite Executives signup form still unstyled.


## 2026-08-06 — [scavenged from "Untitled task"] Site outage diagnosed as stale browser cache
A brief Cloudflare 503 on /css/style.css got cached by the browser and kept re-serving after Cloudflare recovered. Nothing was actually broken site-side. Fixed with a hard refresh (Ctrl+Shift+R) in both Chrome and Brave.
Next action: none — resolved, confirmed working by Chris.
Source session: local_674331a9-156a-4f9f-9ea9-3c77de74886f (originally ran outside the project folder)

## 2026-08-06 — [scavenged from "Book Amazon links strategy"] Amazon buy links and cover images deployed
Added Amazon buy links to both book pages, the books catalog, and "Available now" homepage badges. Removed leftover Shopify buy-button scripts from the CwC page (also fixed a truncated file issue found in passing). Replaced both cover images from Downloads (Cyber Risk cover resized 3600x5400 → 1024x1536 for web; CwC cover already correct size, copied over). All changes deployed.
Next action: none — deployed and complete.
Source session: local_850c923b-af3f-42af-8fbc-e72eb8b53a7b (originally ran outside the project folder)

## 2026-08-06 — [scavenged from "Remind style executives form"] MailerLite Executives form still blocking full site deploy
Same content as logged in 04_Book_Cybersecurity_Executives/SESSION-LOG.md: the Executives signup form (id 192571086895843038) is unstyled (has_content:false), rendering blank on Cyber Risk pages and blocking the full site deploy for the July 18 launch window. ~5-minute fix, same as the completed Makers form.
Next action: style the Executives MailerLite form (template + brass #B68A4E button + heading) to unblock deploy.
Source session: local_8084d118-3953-4445-b3c9-59312353b493 (originally ran outside the project folder)


## 2026-08-06/07 — [scavenged from "Chrome redirect issue marquepublishing.com"] /site retirement guard, CRBR download button wired, cache-purge auto-wired (also harvested — cache-purge portion overlaps 2026-08-06 harvested entry above)
Built `scripts/deploy-guard.js` as the only deploy path (`npm run deploy` now replaces every direct wrangler command in the scheduled task, CLAUDE.md, and notes). Guard halts before shipping on: any /site URL-space reference in deployable content, private business docs (launch plan, marketing plan, .docx, logs) inside the deploy folder, the old redirect stub reappearing at project root, or any scheduled task whose deploy command targets something other than `site`. On violation it writes `MARQUE-DEPLOY-BLOCKED.txt` to the Desktop and raises a Windows popup (fixed to always-on-top after Chris missed the first test). Full audit came back clean — no /site references anywhere in the 15 scheduled tasks, build scripts, source pages, project instructions, or installed skills.
Separately fixed the CRBR (Cyber Risk) page's broken "free guide" offer: the section relied on an inactive MailerLite embed (form HWaBaq, Executives-side, never activated) that rendered as nothing. Added a direct "Download the free guide (PDF)" button linking to `site/10-cybersecurity-decisions.pdf` (verified complete/polished), deployed on both source and built copies. The Executives MailerLite form itself is still not activated — noted as still pending, see 04_Book_Cybersecurity_Executives log.
Also found and fixed: marquepublishing.com/cyber-risk was serving a stale Cloudflare edge-cache page ("Get notified" instead of live Amazon buy buttons), likely cached since the 7/18 launch. Chris manually purged via dashboard, then asked for the auto-purge token — created a scoped Cloudflare API token (Cache Purge only, marquepublishing.com zone) via browser automation, stored at `C:\Users\rctha\.marque\cache-purge-token` (outside the deployable tree), and wired it into deploy-guard.js so every successful deploy auto-purges the edge cache going forward.
Next action: activate/style the Executives MailerLite form (id 192571086895843038) to also capture emails on the CRBR download, per the still-open item in 04_Book_Cybersecurity_Executives.
Source session: local_f52eb644-18cd-4ed0-90e1-6507150d76b6 (originally ran outside the project folder)

## 2026-08-08 -- Site "broken" report was a stale browser cache (harvested)

A report that the site looked broken traced to a stale browser-cached 503 from a
brief Cloudflare edge hiccup roughly 10 hours earlier -- the edge had already
recovered (fresh curl returned 200) but the browser kept re-serving its cached
error. Hard refresh (Ctrl+Shift+R) fixed it in both Chrome and Brave. No redeploy
was actually necessary; site files were fine the whole time. No action needed
going forward -- noted for the record in case the pattern recurs.


## 2026-08-10 -- Blog visibility broken; fix session interrupted at the usage ceiling (harvester entry)

Chris reports (in a parallel session) that the LIVE site is missing ALL blog content -- none of
the security posts, none of the AI posts -- and that /site was retired. A late-evening session
("Website updates and book launches") worked heavily in this repo: edit_blocks, a new directory,
multiple writes into site\ and site\blog\ (mtimes to 01:35 UTC 8/11) -- then died at the usage
ceiling mid-write. NO git commit resulted (HEAD still 3a5c720, 7/28): the work is uncommitted and
undeployed, and blog.html / index.html are untouched since 8/9.
Open items: (1) reconcile repo site\blog (57 posts) against what marquepublishing.com actually
serves; (2) inspect the uncommitted changes -- finish or roll back; (3) deploy only via
npm run deploy (guard + auto cache-purge). Carries: MailerLite Executives form still unstyled.


## 2026-08-10/11 — THL preorder live, Marque AI Collection launched, blog consolidated, src-drift landmine defused

**"Where's the blog content?" diagnosed.** The cyber posts were deployed the whole time — /blog was serving a mid-July edge-cached index (third cache incident; browser cache likely worse on Chris's machine). Redeploy + purge fixed it. The AI posts were ALSO live the whole time, but only at the Creating with Claude hub blog (/creating-with-claude/blog, 19 posts) — never surfaced on the main blog, so they were invisible unless you found the hub.

**src-drift landmine (root cause work).** src/pages had drifted ~3 weeks behind site/ (the daily publisher edits site/ directly) — any `npm run build` would have wiped 40+ posts off the live blog index. Built `scripts/sync-src-from-site.js` (back-ports site/ into src/pages with a byte-exact round-trip check), synced blog.html + index.html, and added it as mandatory Step 4b in Scheduled/publish-blog-content/SKILL.md.

**Blog consolidation.** Main /blog now aggregates both streams: filter tabs (All / Cybersecurity / Creating with AI), cards for all 19 hub posts linking to their canonical /creating-with-claude/blog/ URLs, stale "More Posts on The Way" block removed, subheads updated. Homepage blog trio = 2 newest cyber + 1 AI. Seven accidental duplicates briefly created in site/blog were archived to _archive/blog-dupes-2026-08-10. Fixed stale pre-launch copy in the hub ai-readiness post ("book launches July 18" → available now).

**THL Sept 1 launch.** Preorder flipped on everywhere: homepage card ("Preorder now · Out September 1"), books page (Amazon Kindle preorder B0HCMCJ7R7 + "paperback & hardcover at launch"), and a new dedicated /treasure-hunter/ page (dark hero, story section, audience cards, trilogy note, Makers-form launch list).

**Marque AI Collection.** Books page gained a collection header; Creating with Claude labeled Book One (books page genre line + CwC page hero kicker); Writing With Claude added as Book Two with Chris's concept cover (writing-with-claude-cover.png, resized 2048x3072 → 1024x1536): homepage card, books page #writing-with-claude entry ("Your voice, amplified — not replaced," copy from the Series Bible), and a "Next in the collection" section on the CwC page. Homepage now "Five Books, Five Obsessions" / "5 books in the works."

**Publish task upgraded.** Step 3b added: content/creative-blog drafts now publish to the hub AND get a card on the main blog index automatically — the AI stream can't strand again.

Deployed (7 files changed) + cache purged; verified live: /blog (tabs + both streams), /books, /treasure-hunter/, homepage.
Next action: swap in the final WWC cover when ready (replace writing-with-claude-cover.png in project root + site/, redeploy). Still open elsewhere: Executives MailerLite form styling.


## 2026-08-11 -- harvester note: blog fix finished and LIVE; repo needs one commit

The interrupted 8/10 session resumed this morning and completed: /blog is cyber-only with a
"Creating with AI" cross-link banner, /creating-with-claude/blog unchanged, homepage preview
three cyber cards, OG tags verified on the deployed files. Deployed via the guarded wrangler
path -- live without a commit. OPEN: repo is uncommitted (HEAD 3a5c720, 7/28) -- 8 modified
files plus untracked site\treasure-hunter\, writing-with-claude-cover.png,
scripts\sync-src-from-site.js, _archive\, and this SESSION-LOG. Next action: review + one
commit/push so the deployed state is recorded. Carry: MailerLite Executives form styling.


## 2026-08-11 -- [scavenged from "Website updates and book launches"] file verification only (also harvested)

Scavenger verified nothing is stranded: writing-with-claude-cover.png present in repo root AND
site\, site\treasure-hunter\index.html present. Session outputs hold only a staging intermediate
(staging\th-part3.html, superseded by the live treasure-hunter page) -- left in place. Context
fully captured by the harvester entries above. Open item unchanged: repo needs one commit/push.

## 2026-08-20 — [scavenged from "Website updates and book launches"] Blog page restructure

**What changed:**
- `/blog` is now cybersecurity-only — all 56 cyber posts, no AI cards, no filter tabs. Dark cross-link banner at top says "Creating with AI" with button pointing to `/creating-with-claude/blog`.
- `/creating-with-claude/blog` continues as standalone AI hub with 19 posts — no changes needed.
- Homepage blog preview now shows three cyber cards instead of two cyber + one AI. CwC hub already promoted through books section and the Marque AI Collection.



## 2026-08-21 — Automated deploy (harvester entry, evening)

The 9:31 publish-blog-content run deployed one post to Cloudflare Pages. Sweep evidence:
`src\pages\index.html` 13:36Z, `src\pages\blog.html` 13:36Z, `site\index.html` 13:36Z,
`.wrangler\cache\pages.json` 13:37Z.

**Published:** "Eight Hours. Six Days. 3.7 Million People." —
https://www.marquepublishing.com/blog/eight-hours-six-days-3-7-million-people

- AI fingerprint fixes: 0 — the draft was clean.
- Blog index: new card added as the newest post on blog.html.
- Homepage: rotated into the three-card preview, replacing "AI Assistant Insider Threat"; the
  Creating with AI card was kept.
- src/pages sync clean, 2 files back-ported. Deploy guard passed, 3 files uploaded, edge cache
  purged. Source draft archived into `12_Thought_Leadership\blog\`.

**Open item, unchanged and widening:** this repo is still UNCOMMITTED at HEAD 3a5c720 (7/28).
Roughly four weeks of live deployed state exists nowhere in git history, and every automated deploy
adds more. One review plus commit/push records it all; the diff gets harder to read every day.

**Carries:** the MailerLite Executives signup form is still unstyled — a five-minute job that blocks
newsletter integration.

**Next action:** review and commit the working tree, then style the Executives form.


## 2026-09-06 -- (harvester) WwC page + gated toolkit built 9/5 night; deploy guard blocked it

- Source: session "Chapters 1-9 edits review" (82afaeeb), files 23:25-23:26 EDT 9/5. Chris:
  "we need to build the mailing list in mailer lite and gate the content before we post it."
- Built: site\writing-with-claude\index.html (book page, #signup anchor), site\downloads\
  wwc-toolkit\index.html (noindex/nofollow, MailerLite Universal script account 2453958; cards
  for reference guides PDF, production worksheets ZIP, editorial + cover brief templates),
  src\pages twins, robots.txt and _headers touched.
- MARQUE-DEPLOY-BLOCKED.txt (23:26 EDT): forbidden .docx inside site\ (the two brief
  templates) + EACCES scanning the Scheduled folder. NOTHING DEPLOYED. Last transcript step was
  a file-delete permission request; no file changes after 23:26.
- Open: remove/convert the two .docx (PDF or into the ZIP), rerun npm run deploy (never
  wrangler directly); confirm the MailerLite form -> group -> welcome email with the download
  link actually exists; author/services page still unbuilt; git HEAD 7/28 with 60 uncommitted
  paths.
- Blog (auto): 9/5 9:31 PM publish pass could not see 12_Thought_Leadership (mount) -- IDScan
  not shipped; MAG breach draft added 9/6 06:11 EDT.

## 2026-09-05 (late) — Writing with Claude: book page + gated toolkit built (from the WwC book session)

Chris decided: MailerLite third group "Writers — Writing with Claude"; gate = form → double opt-in →
welcome email delivers links; everything gated (guides PDF, worksheets ZIP, both briefs).

**Built (LOCAL, not deployed):**
- `src/pages/writing-with-claude/index.html` → `site/writing-with-claude/index.html` — book page
  modeled on treasure-hunter: hero (concept cover, "in production"), the book, who it's for, locked
  toolkit cards, signup section with `data-form="WWC_FORM_SLUG"` placeholder.
- `src/pages/downloads/wwc-toolkit/index.html` → `site/downloads/wwc-toolkit/index.html` — unlisted
  download page (noindex/nofollow; `site/_headers` X-Robots-Tag; new `site/robots.txt` Disallow).
- Files in `site/downloads/wwc-toolkit/`: reference-guides PDF (20 pp, built from WwC appendix v6),
  production-worksheets ZIP (10 templates + README, .md + .docx), editorial + cover brief PDFs.
  Loose .docx removed after the deploy guard flagged them (guard rule: no .docx in site/).
- Targeted render of the two new pages only — `npm run build` NOT run, so nightly blog cards intact.
- `deploy-guard --check` passes (the Scheduled-folder EACCES line is the sandbox, not a real block).
  NOTE: the guard wrote MARQUE-DEPLOY-BLOCKED.txt to Chris's Desktop and raised a popup during the
  docx check — that alert is stale; safe to delete.
- MailerLite plan + welcome email copy appended to MAILERLITE-SETUP.md. Connector was not connected
  this session, so group/form/automation are still to create.

**Chris's hand-off:** (1) connect the MailerLite connector or do steps 1–2 in the dashboard;
(2) paste the new form slug over `WWC_FORM_SLUG` in src + site copies; (3) build the welcome
automation from the copy; (4) `npm run deploy`. Also: the Executives form styling carry is
still open.

**Repo note, unchanged:** working tree still uncommitted at HEAD 3a5c720. Commit before more drift.

## 2026-09-06 — Toolkit PDFs fixed after Chris's check

- Chris opened the reference-guides PDF: every table carried a junk "———" row. Cause: my em-dash
  conversion for the download copy also hit the Markdown table-separator lines, and the generator
  rendered them as data rows. Fixed (separator rows exempt); regenerated. Brief PDFs had borderless,
  half-empty tables from the pandoc path — rebuilt all 11 worksheet .docx with the project's
  generator (bordered tables), horizontal rules dropped, dashes normalized; ZIP + both brief PDFs
  replaced in site/downloads/wwc-toolkit/. Deploy guard --check still clean.
- Chris's read on "site in the URL" checked: no /site URL anywhere (pages, PDF, email copy, guard
  pass). What he saw was the on-disk folder `site\` — the Cloudflare output root, not a URL.
- Chris opened site/writing-with-claude/index.html straight from the folder — renders unstyled
  because asset paths are absolute (documented in CLAUDE.md). Needs the local server or deploy.
- Lesson logged: open and look at every served file before presenting it. I rasterized page 1 of
  the guides PDF and stopped; the damage was on page 6 onward.

## 2026-09-06 (later) — Toolkit PDFs rebuilt in the house style

- Chris: "did you even look at how this rendered?" He was right twice over. The first fix removed the
  junk table rows but left a raw Word export — plain headings, no header band, no footer — next to
  the designed companion resources already on the site (custom-instructions-builder.pdf etc.).
- New generator: `scripts/build_wwc_toolkit_pdfs.py` (ReportLab, Markdown in). Matches the
  existing downloads: Helvetica, rust #C4623A accent, "WRITING WITH CLAUDE | Companion Resource"
  header band, "Marque Publishing | marquepublishing.com | Page N" footer, rust H2s, olive H3s,
  bordered tables with tinted header row, rust-bar block quotes, headings kept with their content.
  Rebuilt: reference guides (24 pp), editorial brief (3 pp), cover brief (3 pp). Every page
  rasterized and checked, including the task tables (Owner column width fixed).
- Rebuild command: `python scripts/build_wwc_toolkit_pdfs.py <appendix.md> <08_brief.md>
  <09_brief.md> site/downloads/wwc-toolkit` (strip the H1 from the two brief .md first; the script
  supplies titles). Re-run whenever the WwC appendix or templates change.
- Download page badge updated to 24 pages. Guard --check clean.

## 2026-09-06 (cont.) — Toolkit PDFs: brand mark, copyright, one-page cards

- Chris asked (1) copyright + Marque logo on everything, (2) single-page QRGs for Ch 1–10 with
  no widows/orphans and no tables split across pages.
- Finding on (1): none of the EXISTING site downloads carry a copyright line or the mark either
  (only the text footer). The three WwC PDFs now do: lozenge mark (brand_assets/web/
  2A_Marque_Loz_Mark.png) + "© 2026 Chris Thatcher · Marque Publishing, LLC · marquepublishing.com"
  in every footer, plus a copyright/not-for-redistribution line on page 1. The older downloads
  should get the same treatment when they are next rebuilt — flagged, not done.
- (2) Generator rewritten: every "##" section is a card on its own page; each card is auto-fitted
  to one page by stepping type size down (100% → 78%); if it still won't fit it runs on but breaks
  only between "###" blocks. Tables never split; paragraphs allowWidows/Orphans=0; headings keep
  with their content. Result: all 10 artifact cards and Ch 1–10 + Ch 13 = one page each (Ch 3 and
  Ch 10 at 90%, Ch 6/7 at 95%, Ch 13 at 86%); Ch 11 and Ch 12 run 3 pages each, breaking at Build /
  Phase headings. 28 pages total. Briefs: 2 + 3 pages, no orphaned headings.
- Every page rasterized and checked. Download page badge → 28 pages. Guard --check clean.

## 2026-09-06 (cont.) — All site downloads stamped: mark, copyright, "Not for redistribution"

- Chris: update the existing downloads too, and put "Not for redistribution" in header/footer.
- WwC toolkit generator: header right now "Companion Resource · Not for redistribution"; footer
  copyright line ends "· Not for redistribution". Rebuilt (28 / 3 / 2 pp).
- New `scripts/stamp_downloads.py` (pypdf overlay): the five Creating with Claude companion PDFs get
  their header-right label and footer repainted in place (mark + © line + page); the board guide
  gets a footer line right of its centered folio (cover page untouched); both book samples get a
  tiny centered line under the folio. Originals in `downloads_originals_2026-09-06/` (project root).
- Every footer of every page (62 pages across 8 files) rasterized and checked; first pass had the
  white-out rectangles a few points short, fixed and re-run from the originals.
- CLAUDE.md house rule added. Guard --check clean. Nothing deployed.

## 2026-09-06 (afternoon) — Writers list set up in MailerLite

- Group "Writers — Writing with Claude" created (ID 197871099722073198).
- Form: duplicated the Creators form so the brand styling carried over, repointed to Writers only,
  renamed "Writing with Claude — Writers Signup" (ID 197871181682968378, slug `0U4Pav`), double
  opt-in on. Dashboard driving via Chrome was flaky (Vue inputs ignored typed text; a form submit
  logged the session out) — Chris fixed the MailerLite connector mid-session and the rest went
  through the API.
- Automation "Welcome — Writers (Writing with Claude)" (ID 197871593993536612): trigger joins
  Writers group → one branded HTML email from the approved copy. Dry run clean, test sent to
  Chris. INACTIVE until Chris activates it.
- `0U4Pav` swapped over `WWC_FORM_SLUG` in src/pages + site. MAILERLITE-SETUP.md updated.
- Guard --check: only the sandbox Scheduled-folder ENOENT line (not a real block). Nothing deployed.
- Open: Chris reviews the test email → activates the automation → `npm run deploy`. Optional:
  customize the form's success message ("Check your inbox to confirm — the toolkit is on its way.").


## 2026-09-06 (evening) — Staged work DEPLOYED; THL flipped to available; repo committed + pushed

- Deployed via `npm run deploy` (guard clean, cache purged), two passes. Live and verified:
  /writing-with-claude/ (book page + Writers form 0U4Pav), /downloads/wwc-toolkit/ (noindex),
  stamped download PDFs, robots.txt, _headers.
- THL: "Preorder now · out September 1" was still live five days after launch. Fixed on homepage,
  /books, /treasure-hunter/ (hero, meta/OG, signup section now "Be First to Hear About Book Two").
  Print ASINs from the live Amazon page: paperback B0HDMY2J3Y (primary Buy button), hardcover
  B0HDK7GQ1S, Kindle B0HCMCJ7R7.
- WwC links repointed from /books#writing-with-claude to /writing-with-claude/ on homepage card,
  /books entry (new "Visit the book page & get the free toolkit" button), and the CwC page's
  "Next in the collection" block. Status copy "In the works" -> "In production".
- Repo: committed 6be3a47 (first commit since 7/28; adds .gitignore for node_modules/.wrangler/
  guard file) and pushed to origin main. Deployed state is now recorded.
- OPEN (Chris): MailerLite automation "Welcome — Writers (Writing with Claude)" (197871593993536612)
  is still DISABLED. Form is live; signups before it is enabled will not get the toolkit email.
  Subscriber baseline today: 4 total.
- Decision from Chris (CMO discussion): Marque AI hub page and per-book intro videos are NOT this
  month — off THE-RAILS. Teaser recorded session = the workshop's selling mechanism (already in
  Workshop-Offer.md), gated behind the list. Next: the Track 2 inventory doc, then gate the CwC toolkit.
- Carry: Executives MailerLite form styling; deploy guard EACCES/ENOENT on Scheduled folder is
  cosmetic (guard passes).

## 2026-09-06 (late) - Toolkit split, forms unified, list routing fixed
- WwC free gate now delivers ONLY the two brief templates; reference guides PDF + worksheets ZIP moved out of site/ to wwc-toolkit-reader-only/ (ship with the book; reader-only page later). WwC page + download page copy updated. Writers welcome email rewritten (subject 'Your Writing with Claude briefs'); automation re-enabled by Chris.
- All four MailerLite forms now use the light Writers style: Makers By4UIw, Executives xmtcNh, Writers 0U4Pav (heading fixed), Newsletter KBp3sy (built, currently unused).
- Routing fix: every page that promises '10 Cybersecurity Decisions' (homepage, books, about, labs, all 70 cyber posts) now uses the Executives form xmtcNh so the Executives automation actually delivers the guide. Previously they fed Newsletter - All, which has no automation. Net: xmtcNh 103 embeds, By4UIw 23, 0U4Pav 2. Generator templates updated.
- Open (copy decision, not urgent): homepage/about/labs promise the cyber guide sitewide; if the general newsletter should be its own thing, swap those four back to KBp3sy and build a Newsletter welcome.


## 2026-09-06 — Harvester (evening): shipping day, all live and committed

Recorded by session-harvester from session 0ed7096e "Marque AI website structure strategy" and
file mtimes (deploys through 17:33Z).

- Deploy unblocked; site live with THL fix, WwC page, full appendix pulled.
- Four MailerLite forms unified in light Marque style: Makers "Create Something Real",
  Executives "Get the Free Guide", Writers "Your Voice, Amplified", Newsletter "Stay in the Loop"
  (NTW6JI -> KBp3sy).
- List routing fixed: cyber-guide pages (homepage, books, about, labs, all 70 cyber posts) ->
  Executives; CwC pages -> Makers; WwC page -> Writers.
- Decision (Chris): Creating with Claude is the LEAD offer everywhere general (hero, popup,
  signup sections). Cyber guide only on the Cyber Risk page and cyber posts.
- Cover frames 3:4 -> 2:3 (side bands gone); v8 CwC and WwC covers live; old ones archived.
- CwC toolkit gate CLOSED: every tool link and the five tool blog posts route to signup; welcome
  email is the only delivery; calculator stays public; "free sample" link removed (file was a
  5-page NOT FOR DISTRIBUTION preview). Tool PDFs unlisted + noindex.
- Open: THL page signup feeds the Makers list (Chris decides fiction group vs newsletter).
- NEXT (agreed for Monday 9/7): blog restructure. /blog becomes a hub with one card per stream
  (Cybersecurity, Creating with AI, Writing with AI "coming soon"); each stream gets its own
  index (/blog/cybersecurity/ new; post URLs do not move); homepage bottom = one latest-post
  card per stream. Update the nightly publisher script FIRST or its next run undoes the change.
  Two-hour job with a test run.


## 2026-09-06 -- [scavenged] source attribution for today's out-of-folder sessions (also harvested)

- Today's website work came from four sessions whose cwd was a session outputs folder, not this project: 82afaeeb "Chapters 1-9 edits review" (PDF stamping, downloads_originals_2026-09-06), f390c2a5 "Writing with Claude list" (MailerLite Writers list + 0U4Pav slug), 0ed7096e "Marque AI website structure strategy" (deploy, CwC gate closed, forms unified, routing fix, commit 6be3a47), 360aa14c "WWC and CWC cover comparison" (v8 covers). All were folder-connected; files and log entries above landed here directly. No copies needed.
- Proof renders of the toolkit PDFs (~45 PNGs) sit in the 82afaeeb outputs folder; derivative, not copied.


## 2026-09-07 -- (auto) Overnight publish: 2 new blog posts live

Nightly publisher run (05:34-05:37Z):
- scanner-at-the-counter.html deployed
- hack-not-a-lapse.html deployed
- blog.html + index.html regenerated
- Cloudflare Pages deploy confirmed (.wrangler cache updated 05:37Z)

Blog restructure still agreed for Monday (today). Must update the nightly publisher script first or its 9:31 PM run undoes the change.


## 2026-09-07 (evening) — First Hour live; ladder pages built (LOCAL, not deployed)

- KDP: "Your First Hour with Claude" live, ASIN B0HJ3XW5MM, $0.99, KDP Select (90-day term from
  9/7 — the ebook must NOT be given away on the site until ~Dec 6). CwC republished with the
  9/4 categories/keywords and the "Marque AI Collection" cover line on all three formats.
- New pages (src/pages + targeted render to site/, NOT `npm run build`): /toolkit/ (starter-kit
  landing, Makers form By4UIw), /reader/ (noindex; readers from the book's cards/back matter;
  Makers form), /workshop/ (holding page, "first to know", Makers form), /downloads/cwc-reader/
  (noindex; 14 PDFs: ten chapter quick-reference cards re-footered to /reader + ethics guide,
  before-you-hit-send, deep research template, win tracker; stamped via new
  scripts/stamp_cwc_reader.py; originals in downloads_originals_2026-09-07/cwc-reader/).
  _headers + robots.txt updated for /downloads/cwc-reader/ and /reader/.
- site/creating-with-claude/index.html (direct edit): hero "Start here for a dollar" tile ->
  Amazon B0HJ3XW5MM; toolkit/signup copy now matches the drip (starter kit on signup, rest over the
  week) instead of "six tools in your inbox". New asset site/your-first-hour-cover.jpg.
- src/pages/books.html: Your First Hour entry added above CwC (rendered).
- MailerLite: new automation "Welcome — Makers (Creating with Claude) — 5 emails"
  (197980985088803893): days 0/1/3/5/7, all five bodies loaded via connector, dry run clean.
  E1 delivers the two starter PDFs + the reader-resources URL; E2 prompt library + First Hour
  Kindle link; E3 custom instructions + CwC; E4 verification checklist + CwC; E5 meeting prep +
  workshop interest (reply) + review ask. Old 1-email Makers welcome PAUSED. Old dark form
  "Creators Signup" (5UgLqq) DELETED — zero site references. Default sender name still
  "Marque Publishing, LLC" -> Chris to change to "Chris Thatcher" and ACTIVATE the new automation
  (dashboard only; connector/browser could not).
- Guard --check: only the cosmetic Scheduled-folder ENOENT in the sandbox. Deploy: Chris runs
  `npm run deploy` (no build step). Then commit.
- Open: Facebook launch post waits for WWC; A+ content for First Hour + CwC (copy/images in
  16_With_Claude_Series/0-Your-First-Hour-with-Claude/aplus/); Amazon series page; blog
  restructure (agreed for today, not started — nightly publisher script first).


## 2026-09-07 -- Site pages built, deploy waiting; books page QA pass

**Session: 0be110f4 "Claude books marketing strategy" (continuation) + 2c2e7b06 "Website content deployment"**

### What was done
- Built and rendered into site/: /toolkit, /reader (unlisted), /workshop, reader-resources download page with 14 PDFs stamped to house rule
- "Start here for a dollar" CWC tile added to CWC page
- First Hour with Claude added to Books page
- CWC signup copy corrected to match what the welcome emails actually send
- Deploy guard integrated into the build
- QA pass: all five book covers confirmed rendering correctly on Books page (CwC, First Hour, WwC, CRBR, THL, Deal Me In)
- downloads_originals_2026-09-07/ created with CWC reader resources

### Decisions
- Pages built but NOT deployed yet -- three-step deploy process required

### Open items
- DEPLOY (three steps in order): (1) MailerLite sender name -> "Chris Thatcher" + activate "Welcome -- Makers (Creating with Claude) -- 5 emails" automation, (2) `npm run deploy`, (3) test signup at /toolkit
- Blog restructure (agreed for Mon 9/7) still pending -- do AFTER this deploy lands
- THL page signup still routes to Makers list (Chris decides fiction group vs newsletter)

### Next action
Deploy the site, then blog restructure.


## 2026-09-07 — [scavenged from "Claude books marketing strategy" (0be110f4, fifth reuse)] Site build: toolkit + reader + workshop + stamped PDFs

- Out-of-folder session, folder-connected to website project. Pages built and rendered to site/: /toolkit (CWC signup with MailerLite form), /reader (unlisted reader-resources landing), /workshop, reader-resources download page with all 14 PDFs stamped (mark + copyright + "Not for redistribution"), "Start here for a dollar" tile on CWC page, First Hour entry on Books page, CWC signup copy corrected. MailerLite 5-email automation content updated via API.
- Deploy waiting: (1) MailerLite sender name → "Chris Thatcher" + activate "Welcome — Makers — 5 emails", (2) npm run deploy, (3) test at /toolkit. downloads_originals_2026-09-07/ and scripts/__pycache__/ untracked.
- Blog restructure (/blog → hub with stream cards) agreed for after deploy lands. Update nightly publisher script first or its 9:31 PM run undoes the change.
- Source: transcript of 0be110f4, also logged in 16_With_Claude_Series\SESSION-LOG.md.

## 2026-09-07 — [scavenged from "Website content deployment" (2c2e7b06)] Post-deploy site QA — all covers confirmed

- Out-of-folder session. Chris asked to verify current book covers. Full visual QA via Chrome confirmed all six covers rendering crisp on the Books page: Creating with Claude, Your First Hour with Claude ($0.99 Kindle button), Writing with Claude (concept, "In production"), Cyber Risk is Business Risk, The Treasure Hunter's Legacy (buy buttons live), Deal Me In ("On the way"). Homepage, blog page, and all layouts clean. No files created.
- Source: transcript of 2c2e7b06.


## 2026-09-08 -- Site deployed (untracked activity)

Chris ran `npm run deploy` at approximately 05:35 EDT. Files updated: site/index.html, site/blog.html, site/blog/astra-cra-collision.html, .wrangler/cache/pages.json. This means /toolkit, /reader, /workshop, reader-resources, the "Start here for a dollar" CWC tile, First Hour on the Books page, and the corrected CWC signup copy are now LIVE on marquepublishing.com. The astra-cra-collision blog post also deployed with this push.

**Open items:**
- Verify MailerLite sender name changed to "Chris Thatcher" and the 5-email welcome automation is activated
- Test: sign up at /toolkit with a fresh address, confirm email 1 arrives with PDF buttons
- Blog restructure (agreed Mon 9/7): /blog becomes a hub with stream cards -- do this next
- Monday shelf check: CwC under Generative AI, Amazon.ca paperback stock, Kindle pricing, Author Central bio, Bowker LCCN

## 2026-09-15 -- Homepage redesign agreed; CwC gate live; WWC MailerLite list created

**What was done:**
- CwC content gate finalized: all tool links/blog posts now route to signup; welcome email is the only path to tools; calculator stays public; mislabeled "free sample" link removed
- Homepage redesign agreed in principle: hero (lozenge + "Stories. Software. Games." + new invitation copy) -> "Meet the Publisher" (photo/bio/credentials) -> "What We Do" three-track (Publishing, Labs, Thinking Out Loud) -> single signup at bottom
- Books page becoming a catalog grid (not full repeated text)
- Dedicated Marque AI Collection page planned under Publishing
- WWC MailerLite list created: group "Writers -- Writing with Claude," form slug 0U4Pav, double opt-in, automation OFF pending activation
- Soft gate design confirmed (noindex + robots Disallow + X-Robots-Tag; honor-system P.S. in email)
- Site QA: all 6 book covers confirmed rendering on books page
- Automated blog deploy: index.html + blog.html updated 9/15 12:55 PM

**Decisions:**
- Homepage structure locked (pending scope decisions below)
- Workshops live on Marque AI Collection page, not a new nav item
- Soft gate is sufficient for now; hard gate is future scope

**Open items:**
- Chris decides: services page scope (full page now or homepage sentence + contact page)
- Chris decides: Labs page (own page or homepage card)
- Chris decides: THL signup routing (fiction group vs. general newsletter; magnet choice)
- Verify contact page works
- Chris must activate MailerLite automation and run npm run deploy for WWC pages

**Next action:** Build homepage mockup after Chris settles scope decisions; test before pushing live.

## 2026-09-15 - Homepage + Labs redesign LIVE
- Homepage cut from 9 sections to 4: hero (lozenge, 'Stories. Software. Games.', original paragraph + Chris's two new paragraphs, ONE 'Email us' button, no hero signup, no links), 'Meet the publisher' (photo, creds line '30 years in cybersecurity - Writer - Advisor - AI coach', books-page bio), 'What we do / Three Tracks, One Standard' (Publishing: books + services mailto; Labs: Meet the engineer + software/games coming soon; Thinking Out Loud: cyber blog + Creating with AI blog), one bottom signup (Makers By4UIw). Removed: authority strip, division cards, featured-books grid, about preview, blog preview trio.
- Labs: 'Meet the Engineer' section with Jayden's desk photo (site/jayden.jpg, 1400x1050; original in brand_assets/photos/) and his bio as Chris wrote it (Scratch at 7, Code Ninjas Black Belt at 15, Lua/Java/JavaScript/C#/Python, Unity + Godot, One Piece with Dad, Pokemon tournaments).
- Process: mockup built in mockup/ -> rendered to preview/ (gitignored, outside site/) -> served on http://127.0.0.1:8787 -> Chris reviewed two rounds -> mockup/install.js promoted to src/pages + site/ -> sync check clean -> deploy + purge. Originals in _archive/pre-redesign-2026-09-15/.
- Scheduled task publish-blog-content/SKILL.md updated: homepage has no blog preview, do not touch site/index.html; Makers form slug By4UIw; tool posts link to #signup.
- Decisions (Chris): services = homepage sentence + contact email for now; Labs card links to the Labs page; no Marque AI hub this month.
- Next: books catalog cleanup (grid, one line each, link to book pages); blog restructure (/blog hub + per-stream indexes + homepage latest-per-stream, nightly task rewritten); THL signup group decision.

## 2026-09-15 (later) - Blog restructure LIVE
- /blog is now a GENERATED hub: three stream cards (Cybersecurity -> /blog/cybersecurity/, Creating with AI -> /creating-with-claude/blog, Writing with AI -> coming soon) each showing its latest post + 'All N posts', then a six-card 'New This Month' grid alternating streams. Generator: scripts/build_blog_hub.js (reads both stream indexes, fills HUB:START/END markers in src/pages/blog.html, writes site/blog.html). NEVER hand-edit site/blog.html.
- New cyber stream index /blog/cybersecurity/ (96 posts, Executives guide form). Post URLs unchanged (/blog/<slug>). AI banner removed.
- Homepage 'Thinking Out Loud' card: Cybersecurity link -> /blog/cybersecurity/.
- Nightly task Scheduled/publish-blog-content/SKILL.md rewritten: cyber cards go to site/blog/cybersecurity/index.html, AI cards to the AI index only, then run build_blog_hub.js, then sync. Homepage untouched.
- One-off: scripts/restructure_blog_20260915.js (+ fix_hub_css.js). Originals in _archive/pre-redesign-2026-09-15/.
- Verified live: hub 3 stream cards + 6 latest; cyber index 96 cards; old post URLs 200.
- Still open: books catalog cleanup; THL signup group; services page (later).
