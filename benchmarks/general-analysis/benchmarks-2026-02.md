# General Analysis - LLM Adversarial Robustness Leaderboard

- **URL**: https://www.generalanalysis.com/benchmarks
- **최종 수집일**: 2026-02-08

## 개요

23개 최신 모델을 HarmBench와 AdvBench 프레임워크로 평가.
다양한 공격 방법론(Zero-shot, TAP, Crescendo)별 비교.

## 평가 방법론

### 공격 기법
| 기법 | 설명 |
|------|------|
| **Zero-shot** | 조작 없이 직접 유해 요청 |
| **TAP (Tree of Attacks with Pruning)** | 분기/가지치기로 다양한 jailbreak 프롬프트 생성 |
| **Crescendo** | 무해한 대화에서 유해 요청으로 다턴 에스컬레이션 |

### 점수 체계
- **Adversarial Robustness Score** = 100% - ASR(Attack Success Rate)
- 높을수록 강한 저항성
- 유해 판정 기준: "actionable, specific, realistic details" 포함 시만 유해로 마킹

## HarmBench 결과 (전체 ASR)

| Model | ASR % | Robustness Score |
|-------|-------|-----------------|
| Claude 3.5 Sonnet v2 | 5.0 | 95.0 |
| Claude 4.0 Sonnet | 15.33 | 84.67 |
| Claude 3.5 Sonnet v1 | 18.5 | 81.5 |
| Gemini 2.5 Pro | 20.17 | 79.83 |
| GPT-4o | 23.5 | 76.5 |
| GPT-4o Mini | 30.0 | 70.0 |
| Command-R | 33.17 | 66.83 |
| Llama 4 Maverick | 36.83 | 63.17 |
| Mixtral 8x22B | 39.33 | 60.67 |
| DeepSeek V3 | 54.67 | 45.33 |

## AdvBench 결과 (전체 ASR)

| Model | ASR % | Robustness Score |
|-------|-------|-----------------|
| Claude 3.5 Sonnet v2 | 3.78 | 96.22 |
| Claude 4.0 Sonnet | 11.92 | 88.08 |
| Gemini 2.5 Pro | 11.99 | 88.01 |
| Llama 4 Maverick | 18.46 | 81.54 |
| GPT-4o | 22.18 | 77.82 |
| GPT-4o Mini | 23.33 | 76.67 |
| Command-R Plus | 39.49 | 60.51 |
| DeepSeek V3 | 39.75 | 60.25 |

## 공격 기법별 상세 (HarmBench)

### TAP Attack (가장 높은 성공률)
| Model | ASR % |
|-------|-------|
| DeepSeek V3 | 93.5 |
| Llama 3.1 405B | 86.0 |
| GPT-4o | 38.0 |
| Claude 3.5 Sonnet v2 | 9.0 |

### Crescendo Attack
| Model | ASR % |
|-------|-------|
| DeepSeek V3 | 47.0 |
| GPT-4o | 26.5 |
| Claude 3.5 Sonnet v2 | 5.5 |

### Zero-shot Attack
| Model | ASR % |
|-------|-------|
| Claude 3.5 Sonnet v1 | 0.5 |
| Claude 3.5 Sonnet v2 | 0.5 |
| Qwen 2.5 72B | 0.5 |

## 유해 카테고리별 취약성 (HarmBench Crescendo)

| Model | Chemical/Bio | Cybercrime | Misinformation | Explicit |
|-------|-------------|-----------|----------------|----------|
| Claude 3.5 Sonnet v2 | 5.56% | 34.88% | 2.44% | 10.0% |
| Claude 4.0 Sonnet | 13.89% | 34.88% | 7.32% | 0.0% |
| DeepSeek V3 | 36.11% | 67.44% | 51.22% | 50.0% |
| GPT-4o | 47.22% | 76.74% | 63.41% | 50.0% |

## AdvBench TAP 고효과 공격

| Model | ASR % |
|-------|-------|
| DeepSeek V3 | 65.58 |
| DeepSeek R1 | 60.77 |
| GPT-4.1 | 56.15 |

## 핵심 인사이트
- **Claude 3.5 Sonnet v2**: 전체 최강 (ASR 4.39%)
- **Anthropic Sonnet 계열**: Top 5 중 4개 차지
- **취약 카테고리**: Misinformation, Cybercrime에 가장 취약
- **강한 카테고리**: Chemical/Bio, Explicit content에 더 강한 저항
- **DeepSeek V3**: TAP 공격에 93.5% 뚫림 → 가장 취약
- **테스트 규모**: 모델당 200~520개 프롬프트, 6개 유해 도메인
