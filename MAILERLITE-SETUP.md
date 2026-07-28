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
