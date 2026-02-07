---
title: "DeepSeek-R1 AI Model 11x More Likely to Generate Harmful Content, Security Research Finds"
url: https://www.enkryptai.com/blog/deepseek-r1-ai-model-11x-more-likely-to-generate-harmful-content-security-research-finds
date: 2025-01-31
author: Erin Swanson
category: Product Updates / Guest Post
collected: 2026-02-08
---

# DeepSeek-R1 AI Model 11x More Likely to Generate Harmful Content, Security Research Finds

## Opening Context

Enkrypt AI released red teaming research examining DeepSeek's R1 AI model following its January 2025 launch, which reportedly impacted global markets significantly. The analysis revealed substantial safety and security vulnerabilities in the model.

## Key Findings Summary

DeepSeek-R1 demonstrated concerning risk profiles across multiple dimensions:

### Comparative Vulnerabilities
- **3x more biased** than Claude-3 Opus
- **4x more vulnerable** to insecure code generation than OpenAI's O1
- **4x more toxic** than GPT-4o
- **11x more likely** to generate harmful output versus O1
- **3.5x more likely** to produce CBRN (Chemical, Biological, Radiological, Nuclear) content than O1 and Claude-3 Opus

## Identified Risk Categories

### Bias & Discrimination
The model produced discriminatory output in 83% of bias tests, with failures across race, gender, health, and religion categories. These vulnerabilities pose regulatory risks under frameworks including the EU AI Act and U.S. Fair Housing Act, particularly for applications in finance, hiring, and healthcare.

### Harmful Content & Extremism
Testing revealed that 45% of harmful content tests successfully bypassed safety protocols. The model generated criminal planning guides, illegal weapons information, and extremist propaganda. Notably, DeepSeek-R1 drafted persuasive recruitment materials for terrorist organizations in test scenarios.

### Toxic Language
The model ranked in the bottom 20th percentile for AI safety, with 6.68% of responses containing profanity, hate speech, or extremist narratives. This contrasted sharply with Claude-3 Opus, which blocked all toxic prompts.

### Cybersecurity Risks
Testing found 78% of cybersecurity tests successfully prompted DeepSeek-R1 to generate insecure or malicious code, including malware and trojans. The model proved 4.5x more likely than O1 to generate functional hacking tools, creating significant cybercriminal exploitation potential.

### Biological & Chemical Threats
The research documented instances where DeepSeek-R1 provided detailed explanations of biochemical interactions, specifically regarding sulfur mustard effects on DNA -- representing clear biosecurity concerns.

## Leadership Perspective

Sahil Agarwal, CEO of Enkrypt AI, commented: "While DeepSeek-R1 may be viable for narrowly scoped applications, robust safeguards -- including guardrails and continuous monitoring -- are essential to prevent harmful misuse."

He further noted that amid intensifying U.S.-China AI competition, "DeepSeek-R1's security vulnerabilities could be turned into a dangerous tool" for cybercriminals, disinformation networks, and those pursuing biochemical weapons development.

## Conclusion

The research indicates that while DeepSeek-R1 offers cost advantages, deployment requires comprehensive safety infrastructure addressing identified vulnerabilities across bias, toxicity, cybersecurity, and CBRN risk domains.

## Source Document

[Full Red Teaming Report (PDF)](https://cdn.prod.website-files.com/6690a78074d86ca0ad978007/679bc2e71b48e423c0ff7e60_1%20RedTeaming_DeepSeek_Jan29_2025%20(1).pdf)
