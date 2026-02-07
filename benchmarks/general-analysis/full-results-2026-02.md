# General Analysis - 전체 모델 상세 결과 (2026-02)

- **URL**: https://www.generalanalysis.com/benchmarks
- **수집일**: 2026-02-08
- **평가 프레임워크**: HarmBench + AdvBench
- **공격 기법**: Zero-shot, TAP, Crescendo
- **자동 평가자**: DeepSeek R1 (strict criteria)
- **참고**: benchmarks-2026-02.md (기존 수집 데이터), methodology.md (방법론 상세)

---

## 1. 전체 모델 리스트 (23개 모델)

General Analysis는 23개 최신 모델을 평가. 아래는 수집 가능한 전체 데이터.

### 1.1 HarmBench 전체 ASR 결과 (Overall)

| Rank | Model | Provider | ASR (%) | Robustness Score (%) |
|------|-------|----------|---------|---------------------|
| 1 | Claude 3.5 Sonnet v2 | Anthropic | 5.00 | 95.00 |
| 2 | Claude 4.0 Sonnet | Anthropic | 15.33 | 84.67 |
| 3 | Claude 3.5 Sonnet v1 | Anthropic | 18.50 | 81.50 |
| 4 | Gemini 2.5 Pro | Google | 20.17 | 79.83 |
| 5 | GPT-4o | OpenAI | 23.50 | 76.50 |
| 6 | GPT-4o Mini | OpenAI | 30.00 | 70.00 |
| 7 | Command-R | Cohere | 33.17 | 66.83 |
| 8 | Llama 4 Maverick | Meta | 36.83 | 63.17 |
| 9 | Mixtral 8x22B | Mistral | 39.33 | 60.67 |
| 10 | DeepSeek V3 | DeepSeek | 54.67 | 45.33 |

*Note: 나머지 13개 모델은 동적 웹사이트 렌더링으로 인해 검색 엔진에서 전체 추출 불가. 사이트 직접 방문 시 확인 가능.*

### 1.2 AdvBench 전체 ASR 결과 (Overall)

| Rank | Model | Provider | ASR (%) | Robustness Score (%) |
|------|-------|----------|---------|---------------------|
| 1 | Claude 3.5 Sonnet v2 | Anthropic | 3.78 | 96.22 |
| 2 | Claude 4.0 Sonnet | Anthropic | 11.92 | 88.08 |
| 3 | Gemini 2.5 Pro | Google | 11.99 | 88.01 |
| 4 | Llama 4 Maverick | Meta | 18.46 | 81.54 |
| 5 | GPT-4o | OpenAI | 22.18 | 77.82 |
| 6 | GPT-4o Mini | OpenAI | 23.33 | 76.67 |
| 7 | Command-R Plus | Cohere | 39.49 | 60.51 |
| 8 | DeepSeek V3 | DeepSeek | 39.75 | 60.25 |

### 1.3 종합 ASR (HarmBench + AdvBench 통합)

Claude 3.5 Sonnet v2의 전체 통합 ASR: **4.39%** (최강 모델)
Gemini 2.5 Pro의 전체 통합 ASR: **16.08%** (3위)

---

## 2. 공격 기법별 상세 결과

### 2.1 HarmBench - TAP Attack (가장 높은 성공률)

| Model | ASR (%) | 비고 |
|-------|---------|------|
| DeepSeek V3 | 93.50 | 거의 완전 뚫림 |
| Llama 3.1 405B | 86.00 | 대형 오픈소스 모델도 취약 |
| GPT-4o | 38.00 | 중간 수준 |
| Claude 3.5 Sonnet v2 | 9.00 | 가장 강한 저항 |

### 2.2 HarmBench - Crescendo Attack

| Model | ASR (%) | 비고 |
|-------|---------|------|
| DeepSeek V3 | 47.00 | 다중 턴에서도 취약 |
| GPT-4o | 26.50 | 에스컬레이션에 부분 취약 |
| Claude 3.5 Sonnet v2 | 5.50 | 강한 저항 |

### 2.3 HarmBench - Zero-shot Attack

| Model | ASR (%) | 비고 |
|-------|---------|------|
| Claude 3.5 Sonnet v1 | 0.50 | 기본 가드레일 매우 강함 |
| Claude 3.5 Sonnet v2 | 0.50 | 동일 수준 |
| Qwen 2.5 72B | 0.50 | 오픈소스 중 강한 저항 |

### 2.4 AdvBench - TAP Attack (고효과)

| Model | ASR (%) | 비고 |
|-------|---------|------|
| DeepSeek V3 | 65.58 | AdvBench에서도 취약 |
| DeepSeek R1 | 60.77 | 추론 모델도 뚫림 |
| GPT-4.1 | 56.15 | OpenAI 신모델도 취약 |

---

## 3. 유해 카테고리별 상세 결과 (HarmBench Crescendo)

### 3.1 모델별 카테고리 ASR (%)

| Model | Chemical/Bio | Cybercrime | Misinformation | Explicit |
|-------|-------------|-----------|----------------|----------|
| Claude 3.5 Sonnet v2 | 5.56 | 34.88 | 2.44 | 10.00 |
| Claude 4.0 Sonnet | 13.89 | 34.88 | 7.32 | 0.00 |
| DeepSeek V3 | 36.11 | 67.44 | 51.22 | 50.00 |
| GPT-4o | 47.22 | 76.74 | 63.41 | 50.00 |

### 3.2 카테고리별 분석

| 카테고리 | 취약성 수준 | 설명 |
|----------|-----------|------|
| **Cybercrime** | 매우 높음 | 모든 모델에서 가장 높은 ASR. Claude v2도 34.88% |
| **Misinformation** | 높음 | DeepSeek/GPT-4o 50%+ 뚫림. Claude는 강하게 저항 |
| **Chemical/Bio** | 중간 | 모델별 편차 큼 (5.56~47.22%) |
| **Explicit** | 중간 | Claude 4.0 Sonnet 0%로 완전 차단. 나머지 10~50% |

---

## 4. 제공사별 분석

### 4.1 Anthropic (Claude 계열)
- **Top 5 중 4개 차지** (Sonnet 계열이 지배적)
- Claude 3.5 Sonnet v2: 전체 최강 (ASR 4.39%)
- 특징: Zero-shot 거의 완벽 차단, TAP에서도 9%로 최저
- Explicit 콘텐츠에서 Claude 4.0 Sonnet 0% 달성

### 4.2 Google (Gemini 계열)
- Gemini 2.5 Pro: 3위 (ASR 16.08%)
- HarmBench/AdvBench 모두 안정적 성능

### 4.3 OpenAI (GPT 계열)
- GPT-4o: 중상위권 (HarmBench ASR 23.50%)
- GPT-4o Mini: GPT-4o보다 약간 취약 (30.00%)
- GPT-4.1: AdvBench TAP에서 56.15% 뚫림 (주의)

### 4.4 Meta (Llama 계열)
- Llama 4 Maverick: 중간 수준
- Llama 3.1 405B: TAP에 86% 뚫림 (매우 취약)

### 4.5 DeepSeek
- **가장 취약한 모델군**
- DeepSeek V3: TAP 93.50%, Crescendo 47.00%
- DeepSeek R1: AdvBench TAP 60.77% (추론 모델임에도 취약)

### 4.6 Mistral
- Mixtral 8x22B: HarmBench ASR 39.33%

### 4.7 Cohere
- Command-R: HarmBench 33.17%
- Command-R Plus: AdvBench 39.49%

### 4.8 Alibaba (Qwen)
- Qwen 2.5 72B: Zero-shot 0.50% (기본 가드레일 강함)
- 전체 ASR 데이터는 사이트에서 확인 필요

---

## 5. 추가 확인된 모델 (23개 추정 전체 리스트)

웹 검색 및 기존 데이터에서 확인된 모델 목록 (전체 23개 중):

| # | Model | Provider | 데이터 확인 수준 |
|---|-------|----------|-----------------|
| 1 | Claude 3.5 Sonnet v2 | Anthropic | HarmBench + AdvBench 전체 |
| 2 | Claude 4.0 Sonnet | Anthropic | HarmBench + AdvBench 전체 |
| 3 | Claude 3.5 Sonnet v1 | Anthropic | HarmBench 전체 |
| 4 | Claude 3.7 Sonnet | Anthropic | 일부 (Llama 4 비교 분석) |
| 5 | Gemini 2.5 Pro | Google | HarmBench + AdvBench 전체 |
| 6 | GPT-4o | OpenAI | HarmBench + AdvBench 전체 |
| 7 | GPT-4o Mini | OpenAI | HarmBench + AdvBench 전체 |
| 8 | GPT-4.1 | OpenAI | AdvBench TAP 부분 |
| 9 | GPT-4.1 Mini | OpenAI | 일부 (Llama 4 비교 분석) |
| 10 | Command-R | Cohere | HarmBench 전체 |
| 11 | Command-R Plus | Cohere | AdvBench 전체 |
| 12 | Llama 4 Maverick | Meta | HarmBench + AdvBench 전체 |
| 13 | Llama 4 Scout | Meta | 일부 (Llama 4 분석) |
| 14 | Llama 3.1 405B | Meta | HarmBench TAP 부분 |
| 15 | Mixtral 8x22B | Mistral | HarmBench 전체 |
| 16 | DeepSeek V3 | DeepSeek | HarmBench + AdvBench 전체 |
| 17 | DeepSeek R1 | DeepSeek | AdvBench TAP 부분 |
| 18 | Qwen 2.5 72B | Alibaba | Zero-shot 부분 |
| 19-23 | (미확인 5개) | - | 사이트 직접 확인 필요 |

*Note: generalanalysis.com은 JavaScript 기반 동적 렌더링 사이트로, 검색 엔진 캐시에서 전체 23개 모델의 완전한 수치를 추출하기 어려움. 위 데이터는 검색 결과, 블로그 포스트, 기존 수집 데이터를 종합한 것임.*

---

## 6. Llama 4 적대적 분석 상세 (블로그 분석)

- **출처**: https://www.generalanalysis.com/blog/llama4_adversarial_analysis
- Llama 4 Maverick과 Llama 4 Scout의 체계적 견고성 평가
- 비교 대상: GPT-4.1, GPT-4.1 Mini, GPT-4o, Claude Sonnet 3.7

### 사용 공격 기법
1. **TAP-R**: 루브릭 기반 점수 매기기로 다중 턴 대화 트리 확장/가지치기
2. **RnR (Redact-and-Recover)**: General Analysis 독자 개발 2단계 공격

### 핵심 발견
- Llama-4-Maverick과 Llama-4-Scout 모두 트리 기반 공격에 지속적 취약성
- 실패 예측 가능성, 정책 시행 일관성, 다단계 적대적 상호작용 취약성 평가

---

## 7. 핵심 인사이트 종합

### 모델 순위 (전체 ASR 기준, 낮을수록 좋음)
1. **Claude 3.5 Sonnet v2** (4.39%) - 전체 최강
2. **Claude 4.0 Sonnet** (~13.6%) - 2위
3. **Gemini 2.5 Pro** (16.08%) - 3위
4. **Claude 3.5 Sonnet v1** (~18.5%) - 4위
5. **GPT-4o** (~22.8%) - 중상위

### 공격 기법별 위험도
| 기법 | 위험도 | 최고 ASR | 해당 모델 |
|------|--------|---------|----------|
| TAP | 극히 높음 | 93.50% | DeepSeek V3 |
| Crescendo | 높음 | 47.00% | DeepSeek V3 |
| Zero-shot | 낮음 | < 5% | 대부분 모델 |

### 핵심 패턴
- Anthropic Sonnet 계열이 Top 5 중 4개 차지 (압도적)
- Cybercrime 카테고리가 모든 모델에서 가장 취약
- DeepSeek 계열이 전반적으로 가장 취약 (특히 TAP 공격)
- 추론 모델(DeepSeek R1)도 적대적 공격에 취약
- Zero-shot 기본 가드레일은 대부분 모델에서 강함
