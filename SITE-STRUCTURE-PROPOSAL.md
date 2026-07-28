# Site Structure Proposal — Audience Hubs

_Draft for Chris to review (morning of July 9). Written the night of July 8._

## The idea, in one line
Organize the site around your two **audiences**, not around individual books.

- **Marque AI** — a growing *collection*: Creating with Claude + future AI books, plus the free tools and the AI blog.
- **Cyber Risk** — a *one-off*: the book, its blog, and the board guide folded into one strong page.

## Why this is the clean version
One principle runs the whole way through:

> **audience → hub → signup form → welcome email**

That's the same split we built in MailerLite tonight (Makers vs. Executives). When the
*page structure* and the *email structure* agree, you never have to ask "which form goes
here?" again — the hub answers it. The site and the list reinforce each other.

## Proposed site map

```
/                     Home — studio front door          [General list]
/books                Full catalog (links into hubs)     [General list]
/about                The team                           [General list]
/labs                 Software + games (future)

/ai/                  ▶ MARQUE AI HUB (collection)       [Makers list]
   /creating-with-claude/     Flagship AI book (buy buttons, author note)
   /ai/blog  (or keep /creating-with-claude/blog)  The AI / maker blog — 7 posts
   /downloads/...             The 6 free tools, surfaced on the hub
   (future AI books slot in here)

/cyber-risk/          ▶ CYBER RISK (one-off page)        [Executives list]
   book + author note + endorsement
   the cyber blog (today's /blog, 22 posts) folded in / linked
   the "10 Cybersecurity Decisions" board guide
```

## Hub 1 — Marque AI  →  Makers form (`5UgLqq`, already live)
A landing page that says "this is where Marque does AI." It holds: the flagship book
(Creating with Claude), the free tools, and the AI blog. When book #2 arrives, it drops in
here with no restructuring. You're already 80% here — the Creating with Claude page is
effectively a proto-hub; "Marque AI" is that page grown into an umbrella.

## Hub 2 — Cyber Risk  →  Executives form (to be created)
Because it's a one-off, this stays **one strong page**, not a big section: the book, its
blog folded in, and the board guide. No over-building for a single title.

## Studio-general pages  →  General list (Newsletter — All)
Home, Books (catalog), About, Labs. Audience-agnostic front-of-house.

## Navigation change
- **Today:** Home · Books · About · Blog · Labs
- **Proposed:** Home · Books · AI · Cyber · About  _(Labs later)_

"Blog" leaves the top nav because there are now two blogs, each owned by its hub. "Books"
stays as the master catalog and routes into the hubs. (One edit now, thanks to the new
shared-nav build system.)

## Blogs & downloads placement
- **AI blog** (7 posts) → under the AI hub. Keep at `/creating-with-claude/blog` for now,
  or move to `/ai/blog` with redirects. (Open question below.)
- **Cyber blog** (22 posts) → under the Cyber hub. Stays at `/blog`, now clearly "the cyber blog."
- **Free tools** (6 downloads) → the AI hub's magnet. **Board guide** → the Cyber hub's magnet.

## This also fixes tonight's lead-magnet snag
The homepage currently hooks people with the *cyber* guide but should feed the *general*
list. The hub model resolves it: the cyber guide becomes the Cyber hub's magnet (→ Executives),
the free tools become the AI hub's magnet (→ Makers), and the homepage moves to an
audience-neutral hook (or offers both) feeding the general list. The gap closes on its own.

## What it takes / timing
Mostly **reframing existing pages, not a rebuild**:
1. Evolve the Creating with Claude page into the AI hub (or add an `/ai/` landing above it).
2. Fold a blog strip + the board guide into the Cyber Risk page.
3. Create + wire the Executives form (AI side already done).
4. One nav edit (shared partial).
5. Redirects for any moved URLs.

Feasible before **July 18** — it's reorganizing, not building new. Roughly one to two
focused sessions.

## Open decisions for you (morning)
1. **Umbrella now or later?** Build `/ai/` as a real hub now, or keep the Creating with
   Claude page as-is and add the umbrella when book #2 is real?
2. **AI blog URL** — move to `/ai/blog`, or leave at `/creating-with-claude/blog`?
3. **Nav** — drop "Blog" from the top nav in favor of AI / Cyber?
4. **Homepage hook** — go audience-neutral, or keep featuring the cyber guide (and accept
   home feeds Executives)?

_My lean: build the AI hub now (the tools + blog already justify it), keep the cyber side as
one lean page, update the nav, and make the homepage neutral. But it's your call in the morning._
