# The 29-Year-Old Bug Leaking Your Credentials Right Now

A security researcher in California just found a bug that has been silently leaking usernames, passwords, and session tokens from corporate networks since January 1997.

Not 2017. 1997 — the year Deep Blue beat Kasparov and most of us were still on dial-up.

The vulnerability is called Squidbleed (CVE-2026-47729), and it lives in Squid Proxy, a piece of open-source software that sits between your employees and the internet across millions of installations worldwide — universities, government agencies, Fortune 500 companies, hospitals. Squid is the invisible plumbing that routes and caches web traffic. If your organization has a web proxy, there is a reasonable chance it runs Squid, and until a patch ships in version 7.7, every default installation is vulnerable.

## What Happened

Researchers at Calif.io discovered that Squid's FTP gateway — a feature almost nobody uses anymore — contains a heap buffer overread. In plain English: when the proxy processes certain requests, it accidentally reads past the boundary of its own memory and spills whatever was sitting there into the response. That "whatever" can include the HTTP requests of other users on the same network, complete with their login credentials, API keys, cookies, and session tokens.

The researchers named it Squidbleed as a nod to Heartbleed, the 2014 OpenSSL vulnerability that shook the internet. The comparison holds up. Both are memory leak bugs in foundational infrastructure. Both sat undetected for years. Both expose credentials at scale.

And both remind us that the most dangerous risks hide in the components we never think about.

## Why Executives Should Care

Here is the question I would ask if I were sitting in a board meeting right now: *Do we even know what proxy software we run?*

Most boards can tell you their endpoint detection vendor and their SIEM platform. Maybe their firewall brand. But the proxy server? The load balancer? The DNS resolver? These are the unglamorous pipes that keep everything flowing, and they rarely appear on a risk register — until they fail catastrophically.

Squidbleed is a case study in what I call infrastructure blind spots. In *Cyber Risk Is Business Risk*, I argue that the Three Questions framework — *What can go wrong? How likely is it? What would it cost us?* — has to extend beyond the obvious attack surfaces. It has to reach into the boring, invisible layers that nobody puts on a slide deck.

The proxy server is exactly that kind of layer.

The exposure here is real but bounded. Most modern web traffic is encrypted via HTTPS, which Squid relays as an opaque tunnel — it cannot read what is inside. But cleartext HTTP traffic still exists in plenty of enterprise environments, especially for legacy internal applications, and any deployment where Squid terminates TLS is also at risk. An attacker who has access to the network — an insider, a compromised endpoint, a contractor on the guest Wi-Fi — can silently harvest credentials from other users sharing the same proxy.

## Tech Debt Compounds Like Interest

Twenty-nine years. That is how long this bug survived in production code, through three decades of releases, code reviews, and independent security audits. The fix is a single check — verify a null terminator before calling a string function. One line of code that was missed since the Clinton administration.

I want to be clear: this is not a story about Squid's maintainers being negligent. Open-source maintainers are chronically underfunded and overworked, and Squid has served the internet reliably for decades. This is a story about what happens when organizations build critical infrastructure on components they never inventory, never audit, and never budget to maintain.

The mitigation is almost comically simple: disable FTP support in your Squid configuration. Every major browser dropped native FTP support years ago. The feature is a vestige of a different era, still enabled by default because nobody turned it off.

That pattern — legacy features left running because "it's always been that way" — is how technical debt compounds into business risk.

## What to Ask Your CISO This Week

If Squidbleed is not already on your security team's radar, it should be.

**"Do we run Squid Proxy, and if so, has the FTP gateway been disabled?"** This is the immediate tactical question. If the answer is yes to Squid and no to disabling FTP, your team should remediate today — not next sprint, today.

**"Do we have a complete inventory of our infrastructure software, including open-source components?"** Squidbleed is this month's example, but the pattern repeats constantly. Log4Shell in 2021. Heartbleed in 2014. The XZ Utils backdoor in 2024. Every one of these was a critical vulnerability in software that most organizations did not even know they were running. A software bill of materials is not a compliance checkbox — it is a survival tool.

**"How are we funding the maintenance of our foundational infrastructure?"** This is the harder conversation. Security budgets tend to flow toward visible, exciting capabilities — AI-powered threat detection, zero-trust architecture, shiny dashboards. Meanwhile, the proxy server that has been running since 2009 gets no love until it bleeds credentials onto the network. Ask where the budget goes, and whether the unsexy but critical components are getting their share.

## One More Thing

Squidbleed will not dominate the news cycle the way a massive data breach does. No congressional hearing, no breathless cable news segment. But that is precisely what makes it worth paying attention to. The threats that keep experienced CISOs up at night are not the dramatic ones — they are the quiet, structural failures in infrastructure nobody remembers deploying.

Your next board conversation about cybersecurity should include the word "inventory" at least as often as it includes the word "AI."
