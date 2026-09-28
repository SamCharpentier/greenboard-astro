---
title: "AI in Securities Compliance: The Architecture Behind the Marketing Pitch"
summary: "Every securities compliance vendor claims to have AI. The architecture underneath tells a different story. Here's how to tell what they actually built."
date: "2026-05-11"
author: "dave-feldman"
featured: true
whitepaperForm: true
coverUrl: "https://cdn.prod.website-files.com/67d0a8a9156b7b7bd46ffe28/6a01e6ff143274ac2e148fd4_resource-database-RxyDNEtgkV0-unsplash.jpg"
status: "published"
seo:
  description: "Every securities compliance vendor says they have AI. Here's how to tell what they actually built — Modern Systems, Bolt-on AI, or DIY via MCP."
---

#### Every vendor says they have AI. Here’s how to tell what they actually built.

Open any securities compliance vendor’s website this quarter and you’ll find the same homepage. Sleek chat interface. A demo of an AI catching a flagged email. The phrase “AI-powered” somewhere above the fold. The press releases are interchangeable.

The architecture underneath is not.

Three patterns now define the market, and the choice between them determines whether AI makes your compliance program meaningfully faster and more defensible — or just adds a friendly chatbot to the workflows you’ve been running for fifteen years.

## Three Approaches

| Approach | What's underneath | What the AI can actually do | Who's here |
| --- | --- | --- | --- |
| Modern Systems | AI-native data layer with a single orchestration layer spanning every compliance domain. | Reason and act across the whole program; plan and modify multi-step workflows with full context. | Greenboard, Hadrius |
| Bolt-on AI | Pre-AI infrastructure with AI features added inside individual modules. | Help with discrete tasks in one use case; limited view of anything outside that module. | Smarsh, Global Relay, Red Oak, MCO, RegEd, MirrorWeb, StarCompliance, ACA, Skematic |
| DIY via MCP | Pre-AI infrastructure with a Model Context Protocol server exposed to your own AI agents. | Whatever you build — the vendor gives you a data pipe; you supply orchestration, maintenance, security. | Comply (ComplySci) |

## Modern Systems: AI Reasons Across the Whole Program

A Modern System is one where the data layer, the workflow layer, and the AI layer were designed together. The agent isn’t a feature on top of compliance software — it’s the way work gets done. The same orchestration layer sits across e-comms, employee compliance, marketing review, vendor diligence, books and records, and supervision. The firm’s actual procedures drive the AI’s behavior. Humans and agents drive the same workflows interchangeably.

Two vendors meaningfully fit the description: Greenboard and Hadrius. Both have rebuilt the stack. They’ve made different bets about where it matters most.

**Greenboard’s bet is the orchestration layer itself, and it has made its investment in** [**Greenboard Go**](/greenboardgo) **a priority.** Greenboard’s thesis: compliance is moving from a system *of record* to a system *of action*. The platform shouldn’t just hold the data and the audit trail — it should execute the work end to end. A flagged communication triggers a related employee disclosure check, surfaces the relevant marketing approval, and updates the supervisory log in one continuous flow. Nobody wrote an integration to make that happen. The agent is grounded in the firm’s actual written procedures, which is also what the firm hands to a regulator on day one of an exam. That’s what “defensible” looks like when it isn’t just a slide.

Hadrius is also AI-native but its center of gravity is different: more focus on per-domain coverage with AI baked into each function. This is strong, but the orchestration layer that flexibly drives work across all of those domains — and has dedicated support for AI-integrated workflows — is more of a Greenboard headline than a Hadrius one.

Greenboard’s thesis is that the value of AI scales with how connected the components of compliance actually are. An eComms flag becomes a trade review, which becomes a supervisory action, which then drives a procedural update. Those workflows require AI-native data and application layers underneath, but the orchestration layer is where they actually happen. That’s the part of the architecture that matters most, and it’s where Greenboard has made its deepest investment through [Greenboard Go](/blog/system-of-action).

| Capability | Greenboard | Hadrius |
| --- | --- | --- |
| Orchestration layer across the whole program | The product itself | Present, secondary to per-domain AI |
| Firm procedures as the AI's operating context | Yes — procedures drive agent behavior end to end | Yes — policy-as-code approach |
| Cross-domain agent actions without custom work | Native | Within product; not the architectural center |
| Dual traditional + agentic UX | Explicit design goal; HCI rebuilt for the agentic era | Not supported in many cases |
| Strategic posture | System of Action: the platform does the work | AI-native infrastructure with per-domain coverage |
|  |  |  |
| --- | --- | --- |
|  |  |  |

## Bolt-on AI: Real Features, Module-Sized Vision

The legacy roster is genuinely working on this. Smarsh ships an AI Assistant, a Noise Reduction Agent it claims cuts false positives by ~60%, and a Misconduct Detection Agent in beta — all living inside the Professional Archive. Global Relay runs LLM-based surveillance with chain-of-thought explanations on alerts, hosts it in its own data centers, and lets customers train models in an AI Studio. Red Oak’s AI Review module catches misleading and promissory language in marketing submissions before the reviewer ever sees them. MCO has a Responsible AI framework and an AI Policy Assistant. ACA Compliance Alpha continues to add AI across its long-tenured suite. Skematic, newer to the market, brings firm and employee compliance into a unified workflow — a real improvement on disconnected modules, though the public AI story stays thinner than either Modern System’s.

None of this is fake. For the use case each tool was built to handle, the AI is often very good.

The catch is structural. When the AI lives inside a module, it sees what the module sees. The e-comms surveillance agent doesn’t natively know about employee trades, marketing approvals, vendor diligence answers, or the firm’s written policies — not without a custom integration for each connection. You get AI that’s locally helpful and globally fragmented. Skematic’s integration layer addresses part of this on the workflow side, but without AI-native orchestration above it, the AI is still an assistive feature rather than the way the work gets done.

The other constraint is harder to retrofit. Long-horizon agentic capabilities — background monitoring across domains, agentic configuration of rules and tests, agents that hold state across many steps — don’t bolt onto data layers that weren’t designed for them. Vendors in this tier can get there eventually, but “eventually” usually means rewriting significant pieces of the stack.

The right question for buyers in this tier isn’t “does it have AI?” Of course it does. The question is whether single-module AI is enough — or whether you want AI that can reason and act across the whole program.

## DIY via MCP: A Pipe, Not a System

Another approach is Comply’s. In April 2026 the company launched the ComplyAI MCP Server. MCP, the open standard Anthropic introduced in late 2024, is a way AI agents can discover and use external tools and data. Comply’s server exposes its compliance information over that standard. Plug it into Claude, Copilot, ChatGPT, or any MCP-compatible client and — in Comply’s pitch — build your own compliance agents “without developers, without IT projects.” It’s an architectural choice with upside. It’s also the choice that puts the most work on the customer.

**MCP gives you a pipe, not a system.** Your team owns the orchestration. When the AI pulls compliance data and reasons across it alongside your CRM and your market-data feed, you’re the one making sure schemas line up, that two systems using “account” to mean different things don’t produce a hallucination, and that the whole arrangement still works when models, the protocol, and the underlying data all keep changing. Building it once is doable. Maintaining it is a job, and saying that this can be accomplished without developers understates the operational work involved. That maintenance is exactly the work a Modern System does for you.

**MCP is young and poses security risks.** Security researchers have already documented prompt injection through tool descriptions, tool-combinations that enable data exfiltration, lookalike tools that silently swap in for trusted ones, and OAuth token exposure across servers. Anthropic-led safety audits and academic work have flagged MCP-based agentic deployments as carrying material risk that requires gateway-style controls. An MCP server, by design, makes data reachable by AI actors over a remote interface — a surface area that is not easy to lock down inside a regulated financial firm.

If you have a sophisticated AI and security team and want an open, vendor-agnostic substrate to build on, MCP is reasonable. If you want capability out of the box, defensible to a regulator, with the orchestration and security already handled — it isn’t.

## The Question That Matters

Each pattern has market presence but technology is moving quickly and not all will necessarily withstand the test of time.  Plug-and-play AI inside the modules you already use? The Bolt-on tier delivers. Maximum flexibility with a strong internal team behind it? MCP. AI as the way the work gets done, with the orchestration and security and exam-readiness handled for you? That’s a Modern System.

The marketing layer has converged on one sentence. The architecture hasn’t. The question worth asking isn’t whether a vendor has AI — they all do. It’s *how the platform was built, what the AI can actually see, and who owns the orchestration.*

That’s where defensibility, total cost, and day-to-day usefulness are going to diverge over the next several years — quietly, and decisively.
