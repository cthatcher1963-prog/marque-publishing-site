# Your Developers Trusted a Plugin. Attackers Were Counting on That.

Last week, JetBrains confirmed that 15 malicious plugins had been operating inside its Marketplace — the official storefront for developer tools used by millions of software engineers worldwide — since October 2025. Eight months. These plugins quietly harvested AI service API keys from every developer who installed them. Nearly 70,000 installations. No alarms. No alerts. Just a slow, silent bleed of credentials straight out of your development environment.

If you're an executive reading this and thinking "that's a developer problem," I'd encourage you to reconsider. Those stolen API keys don't just represent a technical inconvenience — they represent unauthorized access to your AI infrastructure, your proprietary data pipelines, and potentially the intellectual property flowing through your AI-assisted development processes.

This is a supply chain attack. And it landed inside 70,000 development environments without tripping a single wire.

## What Actually Happened

The attack was elegant in its simplicity. A threat actor published plugins that did exactly what they advertised: code review, chat features, commit message generation. Developers installed them because they looked legitimate and solved real problems. But buried in the code was a second function. Every time a developer entered an API key for services like OpenAI, Anthropic, or other AI providers, the plugin silently forwarded that key to the attacker's server.

No popup. No consent screen. No indication anything was wrong.

Aikido, the security firm that discovered the scheme, found something even more brazen: the attackers appeared to be reselling the stolen keys to paid subscribers.

Let that sink in. They built a subscription business on top of your stolen credentials.

JetBrains responded by pulling the plugins, blocking the publisher accounts, and remotely disabling installed copies. But eight months of exposure doesn't get cleaned up with a takedown notice.

## Why This Matters to Your Business

In *Cyber Risk Is Business Risk*, I talk about the Three Questions framework — three things every executive should be able to answer about their organization's cyber posture. The first question is deceptively simple: *What do we have?*

Most organizations can tell you about their servers, their cloud instances, their SaaS subscriptions. Very few can tell you what plugins their developers have installed in their IDEs. Even fewer can tell you which of those plugins have access to API keys that connect to paid AI services processing company data.

That gap — between what you think you control and what you actually control — is where attackers live.

In my experience, this incident also illustrates something I keep coming back to: the difference between compliance and security. Your organization might be fully compliant with every applicable framework. You might have a software bill of materials. You might audit your production dependencies. But if nobody is looking at what your developers install on their local machines — the tools they use to build your products — you have a blind spot that compliance will never catch.

## The AI Dimension Makes It Worse

Those API keys connect to AI services that are increasingly embedded in core business processes. Stolen AI API keys can be used to access any data your AI pipelines process, including proprietary business logic and customer information. They can run up massive compute bills on your account — some organizations have reported charges of tens of thousands of dollars from stolen AI credentials. And they can potentially access conversation histories and context windows containing sensitive business data.

We are asking developers to integrate AI into everything. That's the right move. But every integration point is also an attack surface. When I talk to boards about AI governance — what I call the "sheriff" role — this is exactly the scenario I'm describing. Somebody needs to be asking: who has access to our AI infrastructure, and how are those credentials managed?

Nobody was asking at those 70,000 organizations. Not until Aikido asked for them.

## What to Ask Your CISO This Week

**"Do we have visibility into developer tool extensions and plugins?"** Most organizations don't. Developer machines are often treated as personal workspaces, not managed endpoints. That made sense when developers were writing code in text editors. It doesn't make sense when their tools have network access and handle authentication credentials.

**"How are we managing AI service API keys across the organization?"** If the answer involves developers copying keys into configuration files or pasting them into plugin settings, you have the same exposure that hit those 70,000 JetBrains users. Centralized key management and rotation policies aren't optional anymore.

**"What's our software supply chain security posture beyond production?"** Most supply chain security programs focus on what ships to customers. The JetBrains incident is a reminder that the development pipeline itself is a target. Your developers' tools are part of your attack surface whether you've inventoried them or not.

## Where This Is Headed

The ReversingLabs 2026 Software Supply Chain Security Report calls the software supply chain "the new ground zero for enterprise cyber risk." Malware on open-source platforms is up 73% this year. Attacks are targeting the tools developers trust most: security scanners, password managers, IDE plugins.

The JetBrains incident wasn't sophisticated. It didn't exploit a zero-day or require nation-state resources. It exploited trust — the reasonable assumption that a plugin in an official marketplace has been vetted.

That assumption is broken. And as AI tools multiply across development workflows, every plugin, extension, and integration becomes a potential entry point.

If your board isn't asking about software supply chain risk with the same rigor they apply to third-party vendor risk, this is the week to start. Developer environments are inside the security perimeter now — whether your security program has caught up to that fact or not.
