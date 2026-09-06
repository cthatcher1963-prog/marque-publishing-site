# MailerLite — Two-List Setup

Updated July 5, 2026. Account: cthatcher1963@gmail.com (ID 2453958).

## Already done (via API, July 5)

- **Group: "Makers — Creating with Claude"** (ID 192195393391429213) — AI-builder audience.
- **Group: "Executives — Cyber Risk"** (ID 192195394516551407) — board/security-leadership audience.
- **Embedded form: "Creating with Claude — Makers Signup"** (ID 192195413134017938, embed slug `5UgLqq`) — feeds the Makers group. Double opt-in is ON.
- Existing setup untouched: "Newsletter — All" group + "Website Newsletter Signup" form (`NTW6JI`) still powers every form on the site today.

## What you do in the dashboard (~20 min)

1. **Style the new Makers form.** Dashboard → Forms → Embedded → "Creating with Claude — Makers Signup" → pick a template, match the brand (Ink `#1B2430` or Paper background, Brass `#B68A4E` button), set success message ("Check your inbox to confirm"), save/publish. The form exists but has no design yet — it won't render on the site until you do this.
2. **Decide double opt-in.** It's ON for the new form (better list quality, fewer fake addresses). Keep it. Just confirm the confirmation email doesn't look default-ugly: Forms → form → Double opt-in email → apply brand colors.
3. **Welcome automations, one per group.** Automations → Create → trigger "subscriber joins group":
   - Makers group → welcome email delivering the free tools (link the /downloads pages + calculator), warm intro, what to expect.
   - Executives group → welcome email delivering the *10 Cybersecurity Decisions* PDF.
   I can draft both emails — say the word.
4. **Move your existing subscriber(s).** Subscribers → select → Add to group → pick the right segment. (Only 1 sub today, 10 seconds.)

## What happens on the site (my side, per launch plan Jul 8)

- CwC hub + creative blog pages switch from `NTW6JI` to the Makers form (`5UgLqq`) once you've styled it.
- Homepage + cyber blog keep the board-guide form, pointed at the Executives group (I'll update the form's group assignment or create a parallel executive form — cleanest is repointing `NTW6JI` to Executives since all its context is the cyber guide).
- "Newsletter — All" stays as the catch-all; both audiences can get studio-wide news (launch announcements) by emailing all groups.

## Sending rules going forward

Cyber content → Executives only. Maker/tutorial content → Makers only. Book launches and big studio news → everyone. This is the whole point of the split: nobody unsubscribes because you sent them the wrong half of your brain.


---

## Status update — July 8, 2026 (completed this session)

**Account note:** The real account (all groups/forms/automations + the Claude connection) logs in as **cthatcher1963@gmail.com** (account ID 2453958). A second, EMPTY account exists under marquepublishing@gmail.com — do not build there. Chris now has access to the correct account.

**Done tonight:**
- **Two welcome automations built AND active** (via the connection, copy written by Claude, activated by Chris in the dashboard):
  - "Welcome — Makers (Creating with Claude)" → delivers the free tools. Automation ID 192477453485082211.
  - "Welcome — Executives (Cyber Risk)" → delivers the 10 Cybersecurity Decisions PDF. Automation ID 192477455759443836.
  - Sender: Marque Publishing, LLC / chris@marquepublishing.com.
- **Makers form designed + live.** "Creating with Claude — Creators Signup" (ID 192195413134017938, embed slug `5UgLqq`), double opt-in on, feeds the Makers group. (Shows active:false = "no signups yet", not a blocker — public share page renders.)
- **Site wired (LOCAL, not deployed):** all Creating with Claude pages (hub, blog index, 7 blog posts) now use the Makers form `5UgLqq`. Generator template (generate_creative_blog.py) updated too, so future posts inherit it. Everything else still uses `NTW6JI`.
- **CwC blog populated:** the 7 creative-blog posts flipped from draft → published and generated live.

**Still to do (next session):**
- **Executives-side segmentation.** No live site form feeds the Executives group yet. `NTW6JI` still feeds "Newsletter — All". Decide: repoint `NTW6JI` → Executives group (cleanest, since its context is the cyber board guide), OR build a separate styled Executives form. This affects homepage + cyber blog + the /cyber-risk/ page.
- **Deploy.** All of tonight's work (author note, /cyber-risk/ page, published blog, Makers-form wiring) is LOCAL only. Run `npm run build` then wrangler deploy to go live.
- Optional: delete the old empty "Simple welcome email" automation (June 18) to reduce clutter.


---

## Writing with Claude — Writers list + gated toolkit (planned 2026-09-05, site side built)

**Decision (Chris, 2026-09-05):** third group, not Makers. Gate = signup form → double opt-in → welcome automation delivers the links. Everything gated: reference guides PDF, production worksheets ZIP, editorial + cover brief templates.

**Site side — DONE locally, not deployed:**
- `/writing-with-claude/` book page (src/pages + site rendered): hero, the book, who it's for, toolkit preview (locked cards), signup section with `data-form="WWC_FORM_SLUG"` placeholder.
- `/downloads/wwc-toolkit/` unlisted download page: `noindex,nofollow` meta, `site/_headers` X-Robots-Tag, `site/robots.txt` Disallow. Files: `writing-with-claude-reference-guides.pdf` (20 pp, the book's appendix), `writing-with-claude-production-worksheets.zip` (10 templates + README, Word + Markdown), `editorial-brief-template.pdf`, `cover-brief-template.pdf`. (No .docx loose in site/ — the deploy guard forbids it; Word versions ride in the ZIP.)
- Deploy guard `--check` passes on the new files.
- Only the two new pages were rendered (targeted render, not `npm run build`) so the nightly blog cards in `site/` were not touched.

**MailerLite side — DONE 2026-09-06 (group + form via dashboard/Chrome, rename + automation via connector):**
- **Group:** "Writers — Writing with Claude" — ID 197871099722073198.
- **Form:** "Writing with Claude — Writers Signup" — ID 197871181682968378, embed slug `0U4Pav`. Duplicated from the Creators form (styling carried over), repointed to the Writers group only, double opt-in ON. Success-message text not customized (inherits the Creators copy) — optional tweak in Edit design.
- **Automation:** "Welcome — Writers (Writing with Claude)" — ID 197871593993536612. Trigger: joins Writers group. One email, subject "Your Writing with Claude toolkit", HTML built from the copy below (Ink/Paper/Brass), sender Marque Publishing, LLC / chris@marquepublishing.com. Dry run clean; test sent to Chris. **Left INACTIVE — Chris activates in the dashboard after reviewing the test.**
- **Slug swapped** into src/pages + site copies of /writing-with-claude/index.html. Not deployed.

Original plan (kept for the record):
1. **Group:** "Writers — Writing with Claude".
2. **Embedded form:** "Writing with Claude — Writers Signup" → Writers group, double opt-in ON. Style it like the Makers form (Ink/Paper, Brass button). Success message: "Check your inbox to confirm — the toolkit is on its way."
3. **Swap the slug:** replace `WWC_FORM_SLUG` in BOTH `src/pages/writing-with-claude/index.html` and `site/writing-with-claude/index.html`.
4. **Welcome automation:** trigger "subscriber joins group: Writers". One email, copy below. Sender Marque Publishing, LLC / chris@marquepublishing.com.
5. **Sending rules:** writer/book-craft content → Writers only. Book launches + studio news → everyone.

### Welcome email — "Writing with Claude" toolkit (draft, Chris's teaching register)

**Subject:** Your Writing with Claude toolkit

**Preheader:** The guides, the worksheets, the two briefs. Plus one thing to do tonight.

Hi,

You're in. Here is everything the book tells you to download, in one place:

**Your toolkit → https://www.marquepublishing.com/downloads/wwc-toolkit/**

- **The Machine: Quick Reference Guides** (PDF). The book's appendix. Every file in your project and what goes in it, then a one-page guide for every chapter's build.
- **Production Worksheets** (ZIP, Word + Markdown). The run sheet with the owner column and every data sheet behind it. Give the run sheet to Claude and say "run my production."
- **Editorial Brief and Cover Brief** templates. Write them before you hire anyone. If Claude turns out to be the anyone, they are its instructions.

Save that link. It doesn't expire.

One thing to do tonight, if you haven't started: create a project folder, dump everything you have into it, and tell Claude to start a session log. That is Chapter 1, and it is the step that makes every other step possible. Ask me how I know.

I'll email when the book launches, and now and then when I have something worth a writer's time. That's it. No spam, ever.

Chris Thatcher
Marque Publishing

P.S. The files are free for readers. Please don't repost them — send a friend to marquepublishing.com/writing-with-claude instead.

## 2026-09-06 (evening) - All four forms on the light Writers style
- Makers form is now **By4UIw** (id 197878758427854030), Executives form is **xmtcNh** (id 197878777449023173), Newsletter form is **KBp3sy** (id 197879891714115182, 'Stay in the Loop', feeds Newsletter - All). All three are duplicates of the Writers form 0U4Pav, repointed to their groups, headings/text rewritten in the editor. Old 5UgLqq / HWaBaq / NTW6JI are no longer on the site; the blog generator templates were updated too.
- Writers form 0U4Pav heading fixed: 'Your Voice, Amplified' + free-briefs text (it had been carrying the Creators copy).
- Free WwC gate now delivers ONLY the two brief templates; reference guides + worksheets ship with the book (reader-only page later). Welcome email must be updated to match (blocked while the automation is active).
