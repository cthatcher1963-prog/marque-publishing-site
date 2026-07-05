# 86,000 Firewalls, 194 Countries, and One Uncomfortable Question For Your Board

On June 16, a security researcher named Volodymyr Diachenko found an open directory sitting on the public internet. Inside it: verified administrator credentials — in cleartext — for more than 73,000 Fortinet firewalls spread across 194 countries. The affected organizations read like a who's who of the Fortune Global 500. Chevron. Samsung. AT&T. Mercedes-Benz. PwC. Oracle. Government agencies in dozens of countries.

They're calling it FortiBleed.

The name undersells it.

The attack itself wasn't sophisticated. Threat actors scanned the internet for Fortinet devices, tried passwords harvested from earlier breaches against each one, and logged every successful hit. No zero-day. No nation-state toolkit. Just credential stuffing at industrial scale against devices that were supposed to be the front door lock.

That's the part that should bother executives.

## The Question Nobody Wants to Ask

In my experience, boards handle novel threats reasonably well. A new vulnerability with a catchy name gets briefed, money gets allocated, people feel like they're responding.

What boards handle poorly is the realization that the basics weren't covered.

FortiBleed isn't a story about a clever attacker. It's a story about 73,000 organizations that left default or reused credentials on their perimeter firewalls — the single device most responsible for keeping unauthorized traffic out of their networks. When half the publicly exposed Fortigate devices on the internet turn out to be compromised, that's not a vulnerability. That's a hygiene failure at civilizational scale.

The uncomfortable question for your board: Are we one of the 73,000?

And if your CISO can't answer that in under five minutes, you have a different problem.

## This is a Three Questions Moment

I talk about the Three Questions framework in *Cyber Risk Is Business Risk* because they cut through the noise in exactly this kind of situation:

*What do we have?* Does your organization run Fortinet devices on its perimeter? How many? Are they internet-facing? Your asset inventory either answers this instantly or it doesn't — and the speed of that answer tells you more about your security posture than any maturity score.

*What are we doing to protect it?* Were those devices patched? Were default credentials changed? Is there multi-factor authentication on administrative access? These aren't advanced questions. They're the equivalent of asking whether the office doors are locked at night.

*What happens if we fail?* With verified admin credentials in the wild, an attacker doesn't need to break in. They walk in. They have the keys. From there it's lateral movement, data exfiltration, ransomware — pick your nightmare. The exposed data included Kerberos hashes, which means domain-level compromise is on the table.

## Compliance Checked the Box. Security Didn't.

Here's what I'd bet happened at a lot of those 73,000 organizations. Somebody bought the Fortinet devices. Somebody configured them. An auditor checked a box that said "perimeter firewall deployed."

And then nobody circled back to ask whether the credentials were rotated, whether the firmware was current, whether the device was actually doing what it was supposed to do.

This is the gap between compliance and security that I keep hammering on. Compliance asks "do you have a firewall?" Security asks "is your firewall actually protecting you right now?" Those are fundamentally different questions, and FortiBleed just demonstrated the cost of confusing them — across 194 countries, on a stage nobody wanted.

## What Executives Should Do This Week

If you're a CEO, CFO, or board member reading this, here's what I'd want to know before Friday.

**Ask your CISO: "Are we running Fortinet devices, and have we checked against the FortiBleed indicators of compromise?"** That's a yes-or-no question. If the answer takes more than a day, your asset management needs work.

**Then ask the harder one: "What's our process for ensuring that security devices themselves stay secure?"** Firewalls, VPN concentrators, identity providers — these are the infrastructure that everything else depends on. If they're not getting priority attention, your security program has a foundation problem.

**And the one that matters most: "How would we know if someone had already used compromised credentials to get inside?"** The FortiBleed data has been circulating since at least early June. The window for exploitation is already open.

## The Board Conversation

FortiBleed is going to come up in board meetings this quarter. When it does, resist the temptation to make it a Fortinet problem. Fortinet makes the devices; your team is responsible for configuring and maintaining them. Every vendor product in your environment carries this same risk if the basics aren't maintained.

The real board conversation isn't "should we replace Fortinet?"

It's "do we have visibility into the security posture of our own infrastructure, and are we investing enough in the boring work of credential management, patching, and asset inventory?"

Not a sexy budget line item. But 73,000 organizations just learned what happens when you skip it.
