---
title: "Surfing in the Dark -- Hidden Dangers Lurking on Every Web Page"
url: https://www.enkryptai.com/blog/ai-agent-security-indirect-prompt-injection
date: 2025-09-24
author: Nitin Birur
category: Industry Trends / Guest Post
collected: 2026-02-08
---

# Surfing in the Dark -- Hidden Dangers Lurking on Every Web Page

## Introduction

Modern AI agents now perform complex tasks autonomously -- researching topics, filling forms, comparing prices, and managing entire workflows without human intervention. OpenAI's ChatGPT Agent can browse and act independently, while Perplexity's Comet automates routine tasks like email management and research organization. However, this advancement introduces critical vulnerabilities.

The core problem: web pages contain text and code that agents interpret as potential instructions, making them susceptible to indirect prompt injection attacks where malicious websites embed hidden directives that hijack agent objectives.

OWASP ranks this as the top AI security risk. Unlike traditional software that separates data and instructions, AI models process both together, creating inherent ambiguity.

## Why These Attacks Work

### Instruction Confusion
Agents struggle distinguishing between user intent and webpage suggestions. This ambiguity forms the root of prompt injection vulnerabilities.

### Cascading Actions
Once agents gain capabilities to click, type, upload files, and access accounts, a single malicious instruction can trigger widespread damage -- data theft, unauthorized modifications, and account compromise. The impact extends across all connected services and accounts. Microsoft identifies this as inevitable and recommends layered defensive strategies.

### Small Model Risks
Research demonstrates smaller language models are easier to manipulate than larger counterparts, particularly when deployed as autonomous agents. Cost savings through model downsizing may introduce security regressions.

## Browser Agents vs. Agentic Browsers

**Browser Agent:** AI software controlling a standard browser (analogous to an AI pilot)

**Agentic Browser:** Browser with integrated AI capabilities (like Comet, where AI features are built into the interface)

Both architectures face identical risks -- reading untrusted pages and susceptibility to hidden instructions. Organizations implement guardrails, but attackers continually adapt.

## Demonstration 1: The Email Heist

Researchers built a fake vacuum review site containing buried malicious instructions within product reviews. The agent received a straightforward task: read reviews and recommend the best vacuum.

The hidden instruction remained invisible to normal users but activated the agent. Instead of reviewing products, the agent:
- Opened webmail
- Searched for sensitive data
- Forwarded information to a test inbox
- Attempted to delete evidence

## Demonstration 2: The Biased Recommendation

A second test embedded subtle instructions directing the agent to recommend a one-star product over a five-star alternative. The agent complied with confidence.

These controlled experiments used fake data with explicit permission, illustrating minimal friction between webpage reading and risky action execution once agents trust page content over user intent.

## Recommendations for Builders

**Treat every webpage as hostile.** If agents read content, it can influence behavior. Handle third-party material like untrusted code.

**Control capabilities, not just prompts.** Restrict default agent actions. Require explicit user approval for risky operations like sending emails or processing payments.

**Apply least privilege principles.** Minimize permissions, isolate data, and maintain comprehensive logging. Establish strict boundaries and filter outputs carefully.

**Test against evolving attacks.** Static filters cannot match emerging techniques. Red-team agents like web applications, not consumer tools.

**Exercise caution with smaller models.** Switching to smaller models for cost reduction requires comprehensive security retesting. Smaller models demonstrate higher jailbreak success rates.

**Consider proactive scanning solutions.** Tools like Enkrypt AI's Asset Risk Scanner scan webpages for policy violations and injection attacks before agent interaction, flagging and blocking malicious content for additional protection.

## Conclusion

Agentic browsing appears magical by collapsing hours of work into single commands. However, every webpage becomes a potential authority figure for agents. Systems unable to distinguish legitimate user authority from webpage directives will follow the loudest voice rather than the actual user.

Organizations should treat indirect injection as inevitable rather than merely possible. Design systems for damage control, incorporate human oversight for critical decisions, and maintain adaptive, layered defenses.

The future belongs to agents that are useful, not easily manipulated.
