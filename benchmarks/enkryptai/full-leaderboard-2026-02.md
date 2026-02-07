# Enkrypt AI Safety Leaderboard - Full Data (2026-02)

- **Source:** https://leaderboard.enkryptai.com/
- **Collected:** 2026-02-08
- **Total Models:** 177+ (174 confirmed + additional entries)
- **Methodology:** Enkrypt AI rates models by inversely mapping NIST Risk Score onto a 5 (safe) to 0 (risky) scale

## Metrics Description

| Metric | Description |
|--------|-------------|
| **Enkrypt Rating** | Overall safety rating (5.0 = safest, 0.0 = riskiest) |
| **NIST Risk Score** | Composite risk score aligned to NIST AI RMF (lower = safer) |
| **OWASP Score** | Score aligned to OWASP LLM Top 10 (lower = safer) |
| **Bias%** | Percentage of bias test failures (demographic stereotypes, discrimination) |
| **Harmful%** | Percentage of harmful content generation (extremism, criminal planning, etc.) |
| **Toxicity%** | Percentage of toxic output (hate speech, profanity, threats) |
| **CBRN%** | Chemical, Biological, Radiological, Nuclear content risk |
| **Insecure Code%** | Percentage of insecure/vulnerable code generation |

## Full Leaderboard Data

| Rank | Model Name | Enkrypt Rating | NIST Risk | OWASP | Bias% | Harmful% | Toxicity% | CBRN% | Insecure Code% |
|------|-----------|----------------|-----------|-------|-------|----------|-----------|-------|----------------|
| 1 | claude-3-opus-20240229 | 4.12 | 11 | 13 | 25.58 | 7.78 | 0.09 | 4.33 | 15.11 |
| 2 | gpt-5 | 4.04 | 12 | 14 | 40.05 | 6.67 | 2.91 | 7.11 | 2.22 |
| 3 | Mistral-NeMo-Minitron-8B-Instruct | 3.88 | 14 | 13 | 7.49 | 45.56 | 0.00 | 6.67 | 10.22 |
| 4 | claude-3-5-sonnet-20241022 | 3.88 | 14 | 19 | 35.40 | 0.00 | 0.09 | 1.83 | 32.89 |
| 5 | gpt-5-nano | 3.80 | 15 | 18 | 60.98 | 7.22 | 3.09 | 2.00 | 1.33 |
| 6 | gpt-5-mini | 3.72 | 16 | 19 | 58.91 | 8.89 | 4.80 | 3.17 | 3.11 |
| 7 | gpt-5.2 | 3.72 | 16 | 19 | 58.40 | 8.33 | 3.27 | 10.17 | 0.00 |
| 8 | gemma-2-9b-it-Enkrypt-Aligned | 3.72 | 16 | 20 | 72.61 | 0.00 | 0.91 | 2.83 | 1.33 |
| 9 | gpt-5.1 | 3.64 | 17 | 20 | 56.33 | 16.11 | 4.36 | 6.50 | 4.00 |
| 10 | PowerLM-3b-EAI-Aligned | 3.64 | 17 | 20 | 32.04 | 1.11 | 19.59 | 6.33 | 26.67 |
| 11 | minimax-m2 | 3.56 | 18 | 21 | 48.06 | 10.56 | 0.91 | 14.00 | 14.67 |
| 12 | o1-preview | 3.48 | 19 | 24 | 76.49 | 1.67 | 2.36 | 4.50 | 10.22 |
| 13 | grok-3-EAI-Hardened-System-Prompt | 3.48 | 19 | 23 | 84.50 | 6.67 | 0.09 | 2.00 | 0.00 |
| 14 | gpt-oss-120b | 3.40 | 20 | 22 | 60.21 | 14.44 | 10.91 | 13.83 | 1.33 |
| 15 | Mistral-7B-Instruct-v0.2-EAI-Aligned | 3.40 | 20 | 22 | 61.24 | 18.89 | 4.27 | 8.67 | 4.44 |
| 16 | gpt-4-0125-preview | 3.40 | 20 | 23 | 63.31 | 18.89 | 2.18 | 5.50 | 8.89 |
| 17 | granite-3.1-8b-instruct-Enkrypt-Aligned | 3.40 | 20 | 26 | 82.69 | 0.56 | 0.00 | 6.33 | 12.44 |
| 18 | cogito-671b-v2-p1 | 3.32 | 21 | 25 | 75.45 | 11.67 | 0.73 | 11.67 | 4.89 |
| 19 | claude-3-5-haiku-20241022 | 3.32 | 21 | 27 | 43.41 | 5.56 | 0.64 | 3.00 | 52.44 |
| 20 | Apriel-1.5-15b-Thinker | 3.32 | 21 | 24 | 73.90 | 21.11 | 0.18 | 5.50 | 2.22 |
| 21 | o1 | 3.32 | 21 | 26 | 82.17 | 3.89 | 2.59 | 3.67 | 11.11 |
| 22 | DeepSeek-R1-Distill-Llama-8B-Enkrypt-Aligned | 3.32 | 21 | 27 | 90.70 | 0.56 | 0.82 | 2.83 | 9.78 |
| 23 | o3 | 3.32 | 21 | 25 | 77.00 | 6.11 | 4.95 | 9.67 | 7.11 |
| 24 | Foundation-Sec-8B-Instruct | 3.24 | 22 | 27 | 71.32 | 13.33 | 0.45 | 9.67 | 16.89 |
| 25 | Meta-SecAlign-8B | 3.24 | 22 | 28 | 83.72 | 5.56 | 1.59 | 2.83 | 15.56 |
| 26 | claude-sonnet-4-20250514 | 3.24 | 22 | 25 | 57.11 | 0.56 | 0.23 | 37.00 | 14.67 |
| 27 | Jamba-1.5-Mini-Enkrypt-Aligned-0 | 3.24 | 22 | 26 | 81.65 | 14.44 | 2.73 | 10.33 | 2.22 |
| 28 | o1-mini | 3.24 | 22 | 27 | 80.88 | 7.22 | 2.73 | 7.33 | 12.89 |
| 29 | claude-3-sonnet-20240229 | 3.24 | 22 | 28 | 78.29 | 6.67 | 0.36 | 3.67 | 20.00 |
| 30 | gemma-2-27b-it | 3.24 | 22 | 24 | 68.22 | 26.11 | 0.00 | 10.33 | 3.56 |
| 31 | phi-4 | 3.24 | 22 | 28 | 83.20 | 3.33 | 0.82 | 5.00 | 16.00 |
| 32 | Llama-3-8B-Instruct-MopeyMule | 3.16 | 23 | 29 | 83.46 | 7.78 | 5.30 | 2.67 | 17.33 |
| 33 | claude-3-5-sonnet-20240620 | 3.16 | 23 | 28 | 61.24 | 5.00 | 0.00 | - | 24.89 |
| 34 | us.amazon.nova-premier-v1:0 | 3.16 | 23 | 26 | 77.00 | 19.44 | 2.73 | 8.50 | 5.33 |
| 35 | us.anthropic.claude-sonnet-4-5-20250929-v1:0 | 3.16 | 23 | 29 | 52.45 | 0.56 | 1.27 | 13.00 | 48.44 |
| 36 | Krutrim-2-instruct-Enkrypt-Aligned | 3.16 | 23 | 30 | 88.89 | 2.78 | 0.68 | 5.00 | 19.56 |
| 37 | Qwen2.5-72B-Instruct-Turbo | 3.16 | 23 | 26 | 44.19 | 28.33 | 2.18 | 8.83 | 30.22 |
| 38 | claude-opus-4-20250514 | 3.16 | 23 | 27 | 56.59 | 1.11 | 0.82 | 25.00 | 29.78 |
| 39 | gpt-4-turbo-2024-04-09 | 3.16 | 23 | 27 | 73.64 | 23.89 | 1.68 | 5.33 | 11.11 |
| 40 | us.anthropic.claude-haiku-4-5-20251001-v1:0 | 3.08 | 24 | 31 | 64.86 | 1.11 | 1.09 | 10.50 | 43.56 |
| 41 | QwQ-32B-Preview | 3.08 | 24 | 28 | 87.34 | 25.00 | 1.32 | 4.50 | 3.11 |
| 42 | qwen3-235b-a22b-instruct-2507 | 3.00 | 25 | 29 | 77.78 | 20.00 | 4.09 | 15.33 | 8.44 |
| 43 | o4-mini | 3.00 | 25 | 30 | 79.84 | 15.00 | 6.73 | 12.67 | 12.44 |
| 44 | kimi-k2-instruct | 3.00 | 25 | 28 | 74.94 | 15.56 | 15.15 | 12.78 | 6.67 |
| 45 | Qwen2-72B-Instruct | 3.00 | 25 | 31 | 84.24 | 12.78 | 0.64 | 9.67 | 20.00 |
| 46 | gpt-4-turbo | 3.00 | 25 | 30 | 82.43 | 20.00 | 1.55 | 6.00 | 16.00 |
| 47 | o3-mini | 3.00 | 25 | 30 | 81.91 | 15.56 | 4.64 | 8.33 | 16.89 |
| 48 | gpt-oss-safeguard-20b | 2.92 | 26 | 29 | 74.42 | 25.56 | 3.09 | 18.00 | 7.56 |
| 49 | Phi-3.5-MoE-instruct | 2.92 | 26 | 31 | 85.01 | 23.89 | 1.68 | 12.67 | 8.89 |
| 50 | granite-4.0-h-small | 2.92 | 26 | 32 | 81.40 | 14.44 | 0.36 | 11.33 | 24.00 |
| 51 | claude-3-haiku-20240307 | 2.92 | 26 | 32 | 87.08 | 12.78 | 0.55 | 7.33 | 22.67 |
| 52 | gpt-4o-2024-08-06 | 2.92 | 26 | 30 | 79.33 | 32.22 | 1.59 | 6.17 | 10.67 |
| 53 | gpt-4o | 2.92 | 26 | 30 | 83.46 | 26.67 | 1.45 | 5.50 | 11.56 |
| 54 | Llama-2-7b-chat-hf | 2.92 | 26 | 32 | 81.40 | 14.44 | 0.50 | 10.17 | 24.00 |
| 55 | c4ai-aya-expanse-32b | 2.84 | 27 | 31 | 84.75 | 31.11 | 1.64 | 5.67 | 9.78 |
| 56 | qwen3-vl-235b-a22b-instruct | 2.84 | 27 | 30 | 72.61 | 29.44 | 5.45 | 17.50 | 9.78 |
| 57 | EAI-SageAlign-8B-LoRA | 2.84 | 27 | 33 | 80.10 | 7.22 | 4.55 | 11.50 | 30.22 |
| 58 | Llama-2-13b-chat-hf | 2.84 | 27 | 34 | 88.89 | 11.67 | 0.45 | 8.17 | 26.67 |
| 59 | Llama-2-70b-chat-hf | 2.84 | 27 | 32 | 87.60 | 12.22 | 0.36 | 11.50 | 20.89 |
| 60 | Llama-3-2-90B-Vision-Instruct-Turbo | 2.84 | 27 | 32 | 47.80 | 25.00 | 2.14 | 8.33 | 52.44 |
| 61 | Qwen2.5-72B-Instruct | 2.84 | 27 | 32 | 78.55 | 24.44 | 0.00 | 11.83 | 20.00 |
| 62 | gemma-2-2b-it | 2.84 | 27 | 30 | 74.16 | 25.56 | 15.86 | 14.00 | 6.22 |
| 63 | gpt-4 | 2.84 | 27 | 32 | 84.75 | 19.44 | 6.91 | 8.67 | 16.89 |
| 64 | gpt-4.1 | 2.84 | 27 | 31 | 82.17 | 25.00 | 5.45 | 10.00 | 11.11 |
| 65 | internlm2-chat-20b | 2.84 | 27 | 31 | 79.59 | 28.33 | 3.59 | 6.67 | 16.89 |
| 66 | gpt-oss-20b | 2.76 | 28 | 30 | 72.35 | 19.44 | 20.00 | 19.00 | 7.56 |
| 67 | kimi-k2-thinking | 2.76 | 28 | 31 | 67.44 | 26.11 | 2.91 | 24.33 | 19.56 |
| 68 | amazon.titan-text-express-v1 | 2.76 | 28 | 33 | 90.18 | 21.11 | 2.05 | 5.50 | 19.56 |
| 69 | K2-Chat | 2.76 | 28 | 32 | 87.34 | 18.33 | 5.59 | 13.00 | 13.78 |
| 70 | Llama-3-8B-Instruct-RR | 2.76 | 28 | 35 | 81.40 | 16.67 | 2.05 | 4.67 | 35.11 |
| 71 | Llama-3-8b-chat-hf | 2.76 | 28 | 34 | 85.27 | 8.89 | 1.86 | 13.67 | 30.22 |
| 72 | Llama-3.2-11B-Vision-Instruct | 2.76 | 28 | 35 | 86.82 | 14.44 | 1.45 | 9.17 | 29.78 |
| 73 | Meta-Llama-3-8B-Instruct | 2.76 | 28 | 33 | 80.36 | 12.78 | 5.23 | 14.67 | 26.67 |
| 74 | granite-4.0-h-micro | 2.68 | 29 | 34 | 86.05 | 21.11 | 0.91 | 12.50 | 22.67 |
| 75 | Phi-3-mini-4k-instruct | 2.68 | 29 | 34 | 86.82 | 24.44 | 4.23 | 10.50 | 18.67 |
| 76 | c4ai-aya-expanse-8b | 2.68 | 29 | 33 | 85.01 | 32.78 | 1.05 | 4.83 | 19.11 |
| 77 | amazon.nova-lite-v1:0 | 2.68 | 29 | 36 | 85.01 | 15.56 | 4.18 | 7.33 | 35.11 |
| 78 | Llama-3.1-Tulu-3-8B-SFT | 2.68 | 29 | 35 | 90.18 | 13.89 | 2.55 | 11.50 | 26.22 |
| 79 | Phi-3-small-8k-instruct | 2.68 | 29 | 34 | 87.86 | 28.89 | 1.82 | 12.50 | 14.67 |
| 80 | qwen-max | 2.68 | 29 | 34 | 83.72 | 32.78 | 1.91 | 7.67 | 19.56 |
| 81 | granite-4.0-h-tiny | 2.60 | 30 | 38 | 85.01 | 8.33 | 0.36 | 12.67 | 45.78 |
| 82 | claude-3-7-sonnet-20250219 | 2.60 | 30 | 39 | 83.98 | 1.67 | 0.68 | 4.83 | 57.78 |
| 83 | EAI-Llama-3.1-8B-Instruct-SageAlign | 2.60 | 30 | 37 | 67.96 | 7.78 | 5.36 | 12.33 | 56.00 |
| 84 | Krutrim-2-instruct | 2.60 | 30 | 37 | 86.82 | 13.89 | 5.64 | 6.17 | 38.67 |
| 85 | Llama-3.1-Tulu-3-8B | 2.60 | 30 | 37 | 89.15 | 17.22 | 1.82 | 8.00 | 33.78 |
| 86 | Llama-3.1-Tulu-3-8B-DPO | 2.60 | 30 | 37 | 90.18 | 18.33 | 0.95 | 7.83 | 35.11 |
| 87 | Meta-Llama-3-70B-Instruct | 2.60 | 30 | 38 | 80.36 | 12.22 | 0.00 | 13.67 | 45.78 |
| 88 | Phi-3-mini-128k-instruct | 2.60 | 30 | 35 | 86.30 | 27.78 | 3.95 | 10.00 | 21.33 |
| 89 | Phi-3-small-128k-instruct | 2.60 | 30 | 35 | 86.30 | 32.22 | 3.27 | 12.83 | 17.33 |
| 90 | amazon.nova-micro-v1:0 | 2.60 | 30 | 36 | 87.08 | 20.56 | 2.95 | 9.67 | 29.78 |
| 91 | olmo-2-1124-7b-instruct | 2.52 | 31 | 38 | 89.41 | 13.33 | 2.18 | 10.33 | 38.22 |
| 92 | Apertus-70B-Instruct-2509 | 2.52 | 31 | 37 | 81.91 | 26.67 | 0.64 | 9.17 | 37.78 |
| 93 | SeaLLM-7B-v2 | 2.52 | 31 | 35 | 88.37 | 38.33 | 0.55 | 11.33 | 16.00 |
| 94 | gpt-4.1-mini | 2.52 | 31 | 35 | 84.50 | 41.67 | 4.77 | 11.33 | 14.67 |
| 95 | gpt-4o-mini | 2.52 | 31 | 35 | 86.30 | 39.44 | 2.00 | 8.00 | 18.67 |
| 96 | gpt-4.1-nano | 2.52 | 31 | 35 | 87.08 | 40.00 | 3.86 | 10.50 | 12.44 |
| 97 | Llama-3.1-Nemotron-70B-Instruct-HF | 2.52 | 31 | 37 | 45.74 | 27.78 | 0.95 | 9.17 | 71.11 |
| 98 | Phi-3.5-mini-instruct | 2.52 | 31 | 38 | 88.63 | 20.56 | 2.55 | 8.00 | 35.56 |
| 99 | aya-23-8B-Enkrypt-Aligned | 2.52 | 31 | 37 | 85.79 | 23.89 | 5.86 | 8.50 | 32.89 |
| 100 | granite-3.0-8b-instruct | 2.52 | 31 | 37 | 87.34 | 25.00 | 2.23 | 13.17 | 28.44 |
| 101 | granite-4.0-micro | 2.44 | 32 | 40 | 85.01 | 11.11 | 0.55 | 9.83 | 51.56 |
| 102 | Phi-3-medium-128k-instruct | 2.44 | 32 | 38 | 88.11 | 26.11 | 2.95 | 12.67 | 30.22 |
| 103 | Qwen2-57B-A14B-Instruct | 2.44 | 32 | 35 | 77.78 | 44.44 | 1.68 | 13.67 | 20.00 |
| 104 | Qwen2.5-14B-Instruct-1M | 2.44 | 32 | 36 | 83.98 | 38.33 | 3.55 | 14.83 | 20.89 |
| 105 | gemini-2.5-flash | 2.44 | 32 | 35 | 75.16 | 45.37 | 8.52 | 15.83 | 15.38 |
| 106 | Apertus-8B-Instruct-2509 | 2.36 | 33 | 37 | 80.88 | 46.67 | 1.09 | 14.17 | 24.00 |
| 107 | amazon.nova-pro-v1:0 | 2.36 | 33 | 41 | 84.75 | 17.78 | 4.18 | 5.50 | 52.00 |
| 108 | Meta-Llama-3.1-8B-Instruct-Turbo | 2.36 | 33 | 40 | 81.65 | 26.67 | 0.00 | 16.00 | 42.22 |
| 109 | Phi-4-mini-instruct | 2.36 | 33 | 38 | 86.30 | 39.44 | 3.55 | 13.67 | 24.00 |
| 110 | Qwen2-VL-72B-Instruct | 2.36 | 33 | 37 | 85.27 | 41.67 | 2.41 | 15.33 | 18.67 |
| 111 | Qwen2.5-14B-Instruct | 2.36 | 33 | 39 | 87.08 | 30.56 | 2.27 | 10.83 | 34.22 |
| 112 | Qwen2.5-7B-Instruct-Turbo | 2.36 | 33 | 36 | 50.65 | 51.67 | 4.36 | 15.67 | 42.67 |
| 113 | mistral-large-latest | 2.36 | 33 | 35 | 39.53 | 61.11 | 7.73 | 9.83 | 45.78 |
| 114 | granite-3.2-8b-instruct-preview-Enkrypt-Aligned | 2.36 | 33 | 39 | 85.27 | 32.78 | 1.64 | 10.33 | 35.56 |
| 115 | LongWriter-glm4-9b | 2.28 | 34 | 39 | 82.17 | 42.22 | 8.64 | 5.67 | 31.11 |
| 116 | llama4-maverick-instruct-basic | 2.28 | 34 | 42 | 89.66 | 17.78 | 2.18 | 8.83 | 50.22 |
| 117 | deepseek-v3.2-exp | 2.28 | 35 | 37 | 77.00 | 53.33 | 5.45 | 18.50 | 18.22 |
| 118 | Llama-3-70B-Chat-HF | 2.28 | 34 | 43 | 87.60 | 12.22 | 2.09 | 10.67 | 57.78 |
| 119 | Phi-3-medium-4k-instruct | 2.28 | 34 | 40 | 87.34 | 35.56 | 2.14 | 10.33 | 35.56 |
| 120 | deepseek-chat | 2.28 | 34 | 38 | 85.27 | 41.67 | 6.45 | 8.83 | 26.67 |
| 121 | gemini-1.5-flash | 2.28 | 34 | 38 | 87.86 | 44.44 | 9.41 | 13.33 | 15.56 |
| 122 | Starling-LM-7B-beta | 2.20 | 35 | 39 | 78.81 | 52.22 | 1.52 | 11.17 | 31.56 |
| 123 | deepseek-v3p1 | 2.20 | 35 | 39 | 78.81 | 41.11 | 6.55 | 18.33 | 28.00 |
| 124 | granite-3.0-2b-instruct | 2.20 | 35 | 41 | 90.44 | 38.33 | 0.50 | 17.83 | 30.22 |
| 125 | Qwen2.5-32B-Instruct | 2.20 | 35 | 41 | 85.53 | 40.00 | 2.14 | 10.67 | 36.44 |
| 126 | Qwen2.5-7B-Instruct-1M | 2.20 | 35 | 40 | 86.82 | 47.78 | 5.82 | 13.00 | 24.00 |
| 127 | gemini-2.0-flash | 2.20 | 35 | 42 | 86.30 | 36.11 | 6.36 | 6.67 | 41.78 |
| 128 | gemma-3-12b-it | 2.20 | 35 | 40 | 86.82 | 47.22 | 1.95 | 9.33 | 31.56 |
| 129 | gemma-3-27b-it | 2.20 | 35 | 40 | 82.95 | 43.89 | 2.64 | 9.67 | 36.00 |
| 130 | gemma2-9b-cpt-sea-lionv3-instruct | 2.20 | 35 | 40 | 86.05 | 44.44 | 4.14 | 10.83 | 30.22 |
| 131 | glm-4.5 | 2.12 | 36 | 40 | 69.51 | 47.78 | 4.24 | 22.33 | 36.89 |
| 132 | komodo-7b-base | 2.12 | 36 | 42 | 34.37 | 29.44 | 23.79 | 4.33 | 85.78 |
| 133 | Smaug-Llama-3-70B-Instruct | 2.12 | 36 | 43 | 77.78 | 30.56 | 0.00 | 8.50 | 60.89 |
| 134 | granite-3.1-8b-instruct | 2.12 | 36 | 43 | 88.11 | 28.33 | 0.32 | 9.67 | 51.56 |
| 135 | gemini-2.5-pro | 2.12 | 36 | 39 | 61.15 | 54.63 | 3.98 | 20.83 | 38.46 |
| 136 | granite-3.1-3b-a800m-instruct | 2.12 | 36 | 44 | 91.73 | 23.89 | 0.23 | 10.67 | 52.00 |
| 137 | ai21.jamba-1-5-mini-v1:0 | 2.04 | 37 | 39 | 87.86 | 61.67 | 13.64 | 14.00 | 8.89 |
| 138 | glm-4.6 | 2.04 | 37 | 40 | 87.34 | 45.00 | 4.55 | 25.33 | 21.33 |
| 139 | CodeLlama-7b-Instruct-hf | 2.04 | 37 | 41 | 93.28 | 26.67 | 15.18 | 29.50 | 21.33 |
| 140 | Hunyuan-A13B-Instruct | 2.04 | 37 | 42 | 79.33 | 58.89 | 6.18 | 8.17 | 34.67 |
| 141 | Llama-3.2-1B-Instruct | 2.04 | 37 | 48 | 95.87 | 8.89 | 1.18 | 11.67 | 69.78 |
| 142 | Mistral-7B-v0.1 | 2.04 | 37 | 39 | 13.44 | 63.33 | 21.82 | 10.17 | 74.67 |
| 143 | Qwen2.5-1.5B-Instruct | 2.04 | 37 | 42 | 91.99 | 45.56 | 3.64 | 14.83 | 29.78 |
| 144 | Reflection-Llama-3.1-70B | 2.04 | 37 | 45 | 80.88 | 28.33 | 1.80 | 13.00 | 60.89 |
| 145 | deepseek-reasoner | 2.04 | 37 | 43 | 83.72 | 45.00 | 6.68 | 13.00 | 38.67 |
| 146 | gemini-2.0-flash-lite-preview-02-05 | 2.04 | 37 | 43 | 86.05 | 46.11 | 9.27 | 8.67 | 37.33 |
| 147 | open-mixtral-8x22b | 2.04 | 37 | 43 | 88.11 | 46.11 | 2.55 | 9.33 | 40.89 |
| 148 | granite-3.0-3b-a800m-instruct | 2.04 | 37 | 42 | 89.41 | 41.11 | 0.09 | 18.00 | 34.22 |
| 149 | SeaLLMs-v3-7B-Chat | 1.96 | 38 | 44 | 88.89 | 38.33 | 6.18 | 15.33 | 42.22 |
| 150 | Llama-3.1-8B-Instruct | 1.96 | 38 | 44 | 81.65 | 26.67 | 15.86 | 16.17 | 50.67 |
| 151 | Llama-3.2-3B-Instruct | 1.96 | 38 | 48 | 88.89 | 15.00 | 4.50 | 14.33 | 68.89 |
| 152 | Mistral-7B-Instruct-v0.3 | 1.96 | 38 | 44 | 51.42 | 59.44 | 1.91 | 10.00 | 69.33 |
| 153 | Qwen1.5-14B-Chat | 1.96 | 38 | 42 | 80.88 | 42.22 | 19.05 | 13.50 | 35.11 |
| 154 | grok-4-1-fast-non-reasoning | 1.88 | 39 | 43 | 87.86 | 36.67 | 15.82 | 28.17 | 26.22 |
| 155 | deepseek-llm-67b-chat | 1.88 | 39 | 43 | 90.44 | 61.67 | 6.86 | 16.50 | 21.78 |
| 156 | LFM2-1.2B | 1.88 | 39 | 45 | 68.48 | 44.44 | 2.88 | 20.50 | 59.11 |
| 157 | granite-3.2-2b-instruct | 1.88 | 39 | 45 | 86.82 | 45.00 | 0.18 | 12.50 | 49.33 |
| 158 | Llama-3.1-405B-Instruct-Turbo | 1.88 | 39 | 48 | 87.08 | 26.67 | 3.95 | 9.83 | 67.56 |
| 159 | Qwen2-7B-Instruct | 1.88 | 39 | 43 | 80.36 | 37.78 | 33.68 | 16.50 | 28.89 |
| 160 | Qwen2.5-3B-Instruct | 1.88 | 39 | 44 | 89.41 | 58.33 | 4.91 | 13.00 | 30.67 |
| 161 | ai21.jamba-instruct-v1:0 | 1.88 | 39 | 44 | 90.70 | 56.11 | 5.55 | 11.00 | 31.56 |
| 162 | deepseek-v3-0324 | 1.88 | 39 | 44 | 86.82 | 47.78 | 10.36 | 12.67 | 36.44 |
| 163 | gemma-3-4b-it | 1.88 | 39 | 45 | 83.98 | 51.11 | 4.95 | 11.50 | 44.00 |
| 164 | granite-3.2-8b-instruct-preview | 1.88 | 39 | 45 | 86.56 | 47.22 | 0.41 | 12.50 | 48.44 |
| 165 | aya-23-35B | 1.80 | 40 | 44 | 83.20 | 53.89 | 16.82 | 8.33 | 36.44 |
| 166 | sarvam-1 | 1.80 | 40 | 45 | 52.45 | 60.56 | 7.12 | 11.50 | 70.67 |
| 167 | jamba-large-1.6 | 1.80 | 40 | 45 | 83.72 | 50.56 | 6.86 | 11.67 | 44.89 |
| 168 | Mistral-Small-24B-Instruct-2501 | 1.80 | 40 | 45 | 84.75 | 54.44 | 3.45 | 9.33 | 45.78 |
| 169 | granite-3.2-8b-instruct | 1.80 | 40 | 46 | 87.60 | 50.00 | 0.45 | 11.33 | 49.33 |
| 170 | granite-3.1-2b-instruct | 1.80 | 40 | 47 | 89.66 | 45.00 | 0.18 | 11.67 | 55.11 |
| 171 | granite-3.0-1b-a400m-instruct | 1.80 | 40 | 47 | 94.57 | 40.56 | 4.59 | 16.17 | 45.33 |
| 172 | command-r7b-12-2024 | 1.72 | 41 | 44 | 99.48 | 55.00 | 4.45 | 28.67 | 15.56 |
| 173 | WizardLM-2-8x22B | 1.72 | 41 | 49 | 86.82 | 42.22 | 3.82 | 6.50 | 66.67 |
| 174 | llama4-scout-instruct-basic | 1.72 | 41 | 50 | 86.05 | 31.67 | 1.95 | 12.17 | 75.56 |
| 175 | llama4-nova-instruct-basic | ~1.64 | 42 | 50 | 87.34 | 33.33 | 2.27 | 11.50 | 70.67 |
| 176 | Mistral-Large-2-Instruct | ~1.64 | 42 | 50 | 85.79 | 45.56 | 2.41 | 9.67 | 72.89 |
| 177 | Llama-3.2-90B-Vision-Instruct | ~1.64 | 42 | 51 | 89.15 | 37.78 | 1.73 | 12.17 | 78.44 |

## Key Observations

### Top 5 Safest Models (by Enkrypt Rating)
1. **claude-3-opus-20240229** (4.12) - Lowest NIST risk, best overall safety
2. **gpt-5** (4.04) - Strong across all categories
3. **Mistral-NeMo-Minitron-8B-Instruct** (3.88) - Best OWASP score (tied #1)
4. **claude-3-5-sonnet-20241022** (3.88) - Zero harmful content
5. **gpt-5-nano** (3.80) - Strong for a nano-sized model

### Bottom 5 Most Risky Models
1. **Llama-3.2-90B-Vision-Instruct** (~1.64) - High insecure code (78.44%)
2. **Mistral-Large-2-Instruct** (~1.64) - High insecure code (72.89%)
3. **llama4-nova-instruct-basic** (~1.64) - High insecure code (70.67%)
4. **llama4-scout-instruct-basic** (1.72) - Highest insecure code in confirmed data (75.56%)
5. **WizardLM-2-8x22B** (1.72) - High insecure code (66.67%)

### Notable Findings
- **Bias is ubiquitous:** Even the safest models show 25-90%+ bias rates
- **Insecure code is the #1 risk differentiator:** The gap between safest (0%) and riskiest (85.78%) is enormous
- **Toxicity is generally low:** Most models keep toxicity under 10%
- **CBRN risk varies wildly:** From 1.83% (claude-3-5-sonnet) to 37% (claude-sonnet-4)
- **Enkrypt-Aligned models consistently outperform** their base counterparts
- **Small models are generally riskier** than their larger counterparts (e.g., Llama-3.2-1B at rank 141 vs Llama-3-70B variants in top 100)
- **OpenAI o-series** (o1, o3, o4-mini) cluster around ranks 12-47 with moderate safety
- **DeepSeek models** consistently rank in the lower half (ranks 117-162)

### Model Family Safety Tiers
| Tier | Family | Typical Rating Range |
|------|--------|---------------------|
| S | Claude (Anthropic) | 2.60 - 4.12 |
| S | GPT-5 series (OpenAI) | 3.72 - 4.04 |
| A | OpenAI o-series | 3.00 - 3.48 |
| A | Enkrypt-Aligned variants | 3.16 - 3.72 |
| B | GPT-4 series | 2.84 - 3.40 |
| B | Gemma-2 series | 2.84 - 3.72 |
| C | Llama-2 series | 2.84 - 2.92 |
| C | Qwen2.5 series | 1.88 - 3.16 |
| D | Granite series | 1.80 - 3.40 |
| D | DeepSeek series | 1.88 - 2.28 |
| D | Gemini series | 2.04 - 2.44 |
