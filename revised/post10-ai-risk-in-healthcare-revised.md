# AI Risk in Healthcare: What Clinicians and Executives Are Getting Wrong

I spent most of last year working with three healthcare systems — two regional hospital networks and a large specialty practice group — on their AI security posture. Every single one had the same blind spot. They treated AI tools like they treated any other software purchase: run it through IT procurement, check the compliance box, deploy.

That approach is going to hurt people.

AI in healthcare is not another IT system. It's a fundamentally different category of risk, and the frameworks most health systems use to evaluate technology were never designed for it. I'm writing this because the gap between where healthcare AI adoption is right now and where healthcare AI governance is right now could get a patient killed — and I don't think enough clinical or business leaders understand how.

## These Systems Can Be Attacked in Ways Most Leaders Haven't Considered

Traditional healthcare IT security focuses on keeping attackers out and keeping data in. Access controls, encryption, network segmentation — the standard playbook. AI systems introduce attack surfaces that don't fit that model.

Adversarial attacks manipulate the inputs an AI model receives — subtly altered imaging data, for example — to produce incorrect outputs. In a clinical context, that could mean a diagnostic model misreading a scan. Not because the model is broken, but because someone deliberately fed it data designed to fool it. Researchers at Harvard and MIT demonstrated this with dermatology classification models back in 2019, and the techniques have only gotten more sophisticated since then.

Data poisoning is the slower-burn version. An attacker — or even a well-meaning insider making bad data hygiene decisions — corrupts the training data that a model learns from. The model still runs. It still produces outputs. But those outputs are quietly biased in ways that may not surface for months. In healthcare, that could mean a clinical decision support tool systematically under-flagging a specific patient population.

And then there's data extraction. AI models can sometimes be reverse-engineered to reveal the training data they were built on. In healthcare, that training data is patient records. I worked one assessment where a vendor's model had been fine-tuned on a client's PHI — and the vendor's security architecture would have allowed a determined attacker to extract fragments of that data through repeated queries. The client had no idea.

## The Complexity Problem

Here's what I keep running into: the people making purchasing and deployment decisions for AI tools in healthcare often don't have the technical depth to evaluate what they're buying.

That's not a criticism. A chief medical officer shouldn't need to understand transformer architectures. But right now, there's a dangerous gap between the complexity of these systems and the ability of decision-makers to assess their risk. A CMO or a VP of Operations evaluates a clinical AI tool based on the vendor's accuracy claims, maybe a pilot study, maybe a peer review. What they're not evaluating — because they can't — is the model's attack surface, its failure modes under distribution shift, or what happens to its performance when the patient population changes.

This is why I argue in *Cyber Risk Is Business Risk* that AI governance can't live solely inside IT or solely inside clinical leadership. It requires a cross-functional team that includes security, clinical informatics, legal, and operations — people who can collectively see the whole picture.

## Validation Has to Be Continuous, Not One-and-Done

Most healthcare organizations validate an AI tool at deployment and then treat it like furniture. It sits there. It runs. Nobody checks whether it's still performing the way it did during evaluation.

That's a mistake. AI models drift. The data they encounter in production diverges from the data they were trained on — patient demographics shift, documentation practices change, new disease variants emerge. A model that performed at 94% accuracy during validation might be operating at 81% eighteen months later, and nobody notices because nobody is looking.

Every AI system touching clinical decisions needs continuous output monitoring — automated checks that flag when performance metrics degrade, when outputs start clustering differently, or when the model's confidence scores shift in patterns that suggest drift. And critically, clinicians need a clear mechanism to challenge an AI recommendation. Not just override it — challenge it, with a documented escalation path that feeds back into model governance.

If a clinician can't explain to a patient why an AI-assisted decision was made, and can't show an auditor the evidence trail behind it, the system isn't ready for clinical use. Full stop.

## The Attacker Is Using AI Too

This is the part of the conversation that keeps me up at night.

While healthcare organizations are carefully piloting AI tools and running twelve-month evaluation cycles, threat actors are deploying AI offensively with no such constraints. AI-generated phishing campaigns targeting healthcare workers are already measurably harder to detect than their manually crafted predecessors — a 2024 study from Abnormal Security found that AI-generated phishing emails had a 60% higher click-through rate in healthcare settings.

Attackers are using AI to scan for vulnerabilities faster than defenders can patch them. They're using it to adapt attack patterns in real time, pivoting when they hit a control. And they're using it to craft social engineering attacks that are personalized to individual employees based on publicly available data.

The implication is stark: healthcare organizations need AI-powered defenses, not just AI-powered clinical tools. Your SOC needs machine learning models that can detect anomalous patterns across your network. Your email security needs AI that can identify AI-generated phishing. Your vulnerability management program needs AI-assisted prioritization. Defending a modern healthcare environment without AI in your security stack is like bringing a clipboard to a gunfight.

## The Regulatory Pressure Is Real and Accelerating

HHS released updated guidance on AI in healthcare in late 2024. The EU AI Act classifies most clinical AI as high-risk, with mandatory conformity assessments. State-level legislation — Colorado's AI Act, California's proposed SB 1047 framework — is creating a patchwork of requirements that multi-state health systems are already struggling to track.

This is not a technical compliance exercise. When regulators come asking about your AI governance — and they will — they're going to want to see board-level accountability, documented risk assessments, continuous monitoring evidence, and incident response plans specific to AI failures. If your answer is "we rely on our vendors to handle that," you're going to have a very bad day.

Compliance in this space requires clinical, operational, legal, security, and technology leaders working together. Not in a quarterly meeting. Continuously.

## Humans Stay in the Loop. Period.

I've heard executives talk about AI "replacing" clinical judgment. That framing is dangerous and wrong — at least for the foreseeable future.

AI in healthcare should augment clinical decision-making, not supplant it. Every AI-generated recommendation in a clinical setting needs a qualified human reviewing it before it reaches a patient. Not because the AI is always wrong — often it's quite good. But because when it is wrong, the consequences land on a person lying in a hospital bed, and that person deserves a clinician who looked at the evidence, not just a confidence score.

In my work, I push healthcare clients toward what I call a "trust but verify" model — use AI to surface insights, flag anomalies, accelerate workflows, but keep a clinician's judgment as the final gate on anything that touches patient care. The organizations getting this right are building that human checkpoint into their clinical workflows from day one, not bolting it on after a near-miss.

The technology is powerful. The risks are specific and serious. And the gap between adoption speed and governance maturity in healthcare is wider than in any other sector I work in. Close it — before a patient pays the price.
