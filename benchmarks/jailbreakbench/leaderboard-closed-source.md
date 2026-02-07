# JailbreakBench - 클로즈드소스 모델 리더보드

- **URL**: https://jailbreakbench.github.io/tables/table_closed_source.html
- **수집일**: 2026-02-08
- **설명**: JailbreakBench 클로즈드소스 LLM 모델(GPT-3.5-Turbo, GPT-4)에 대한 탈옥 공격 성공률 리더보드. 다양한 공격 기법과 방어 기법의 조합별 성공률을 보여준다.

---

## 리더보드 테이블

### 대상 모델
- **GPT-3.5-Turbo-1106**: OpenAI의 경량 상용 모델
- **GPT-4-0125-Preview**: OpenAI의 최상위 상용 모델

### 방어 기법 (Defenses)
| 방어 기법 | 설명 |
|-----------|------|
| None | 방어 없음 (기본 모델) |
| SmoothLLM | 입력 perturbation 기반 방어 |
| Perplexity filter | 높은 perplexity 입력 필터링 |
| Erase-and-Check | 토큰 삭제 후 안전성 재검증 |
| Synonym Substitution | 동의어 치환 기반 방어 |
| Remove Non-Dictionary | 사전에 없는 단어 제거 |

---

## 1. PAIR 공격 (Black-box, LLM-assisted)

- **논문**: Jailbreaking Black Box LLMs in Twenty Queries
- **날짜**: 2023-10-12
- **위협 모델**: Black-box
- **특징**: LLM을 활용한 자동화 공격

| Model | Defense | Avg Queries | Success Rate |
|-------|---------|-------------|--------------|
| GPT-3.5-Turbo-1106 | None | 30 | 71% |
| GPT-4-0125-Preview | None | 51 | 34% |
| GPT-3.5-Turbo-1106 | SmoothLLM | 30 | 5% |
| GPT-4-0125-Preview | SmoothLLM | 51 | 19% |
| GPT-3.5-Turbo-1106 | Perplexity filter | 30 | 17% |
| GPT-4-0125-Preview | Perplexity filter | 51 | 30% |
| GPT-3.5-Turbo-1106 | Erase-and-Check | 30 | 2% |
| GPT-4-0125-Preview | Erase-and-Check | 51 | 1% |
| GPT-3.5-Turbo-1106 | Synonym Substitution | 30 | 21% |
| GPT-4-0125-Preview | Synonym Substitution | 51 | 24% |
| GPT-3.5-Turbo-1106 | Remove Non-Dictionary | 30 | 18% |
| GPT-4-0125-Preview | Remove Non-Dictionary | 51 | 25% |

---

## 2. GCG 공격 (White-box, Transfer attack)

- **논문**: Universal and Transferable Adversarial Attacks on Aligned Language Models
- **날짜**: 2023-07-27
- **위협 모델**: White-box (transfer 기반)
- **특징**: Suffix 기반 공격, 256K 쿼리 (오픈소스 모델에서 생성 후 전이)

| Model | Defense | Avg Queries | Success Rate |
|-------|---------|-------------|--------------|
| GPT-3.5-Turbo-1106 | None | -- | 47% |
| GPT-4-0125-Preview | None | -- | 4% |
| GPT-3.5-Turbo-1106 | SmoothLLM | -- | 0% |
| GPT-4-0125-Preview | SmoothLLM | -- | 4% |
| GPT-3.5-Turbo-1106 | Perplexity filter | -- | 0% |
| GPT-4-0125-Preview | Perplexity filter | -- | 0% |
| GPT-3.5-Turbo-1106 | Erase-and-Check | -- | 3% |
| GPT-4-0125-Preview | Erase-and-Check | -- | 2% |
| GPT-3.5-Turbo-1106 | Synonym Substitution | -- | 15% |
| GPT-4-0125-Preview | Synonym Substitution | -- | 15% |
| GPT-3.5-Turbo-1106 | Remove Non-Dictionary | -- | 9% |
| GPT-4-0125-Preview | Remove Non-Dictionary | -- | 2% |

---

## 3. AIM 공격 (Black-box, Jailbreak Chat)

- **논문**: Jailbreak Chat
- **날짜**: 2023-03-01
- **위협 모델**: Black-box

| Model | Defense | Avg Queries | Success Rate |
|-------|---------|-------------|--------------|
| GPT-3.5-Turbo-1106 | None | -- | 0% |
| GPT-4-0125-Preview | None | -- | 0% |
| GPT-3.5-Turbo-1106 | SmoothLLM | -- | 0% |
| GPT-4-0125-Preview | SmoothLLM | -- | 0% |
| GPT-3.5-Turbo-1106 | Perplexity filter | -- | 0% |
| GPT-4-0125-Preview | Perplexity filter | -- | 0% |
| GPT-3.5-Turbo-1106 | Erase-and-Check | -- | 0% |
| GPT-4-0125-Preview | Erase-and-Check | -- | 0% |
| GPT-3.5-Turbo-1106 | Synonym Substitution | -- | 0% |
| GPT-4-0125-Preview | Synonym Substitution | -- | 0% |
| GPT-3.5-Turbo-1106 | Remove Non-Dictionary | -- | 0% |
| GPT-4-0125-Preview | Remove Non-Dictionary | -- | 0% |

---

## 4. Prompt with Random Search (Logprob access)

- **논문**: Jailbreaking Leading Safety-Aligned LLMs with Simple Adaptive Attacks
- **날짜**: 2024-04-02
- **위협 모델**: Logprob access
- **특징**: Self-transfer suffixes 사용

| Model | Defense | Avg Queries | Success Rate |
|-------|---------|-------------|--------------|
| GPT-3.5-Turbo-1106 | None | 3 | 93% |
| GPT-4-0125-Preview | None | 1K | 78% |
| GPT-3.5-Turbo-1106 | SmoothLLM | 3 | 4% |
| GPT-4-0125-Preview | SmoothLLM | 1K | 56% |
| GPT-3.5-Turbo-1106 | Perplexity filter | 3 | 61% |
| GPT-4-0125-Preview | Perplexity filter | 1K | 70% |
| GPT-3.5-Turbo-1106 | Erase-and-Check | 3 | 8% |
| GPT-4-0125-Preview | Erase-and-Check | 1K | 10% |
| GPT-3.5-Turbo-1106 | Synonym Substitution | 3 | 5% |
| GPT-4-0125-Preview | Synonym Substitution | 1K | 5% |
| GPT-3.5-Turbo-1106 | Remove Non-Dictionary | 3 | 11% |
| GPT-4-0125-Preview | Remove Non-Dictionary | 1K | 46% |

---

## 주요 분석 요약

### GPT-3.5-Turbo-1106
- AIM 공격에는 완전 면역 (0%)
- PAIR 공격에 71% 취약 (방어 없을 때)
- **Prompt with Random Search**가 가장 위협적 (93%, 단 3쿼리)
- SmoothLLM이 Prompt with Random Search에 효과적 (93% -> 4%)

### GPT-4-0125-Preview
- AIM 공격에 완전 면역 (0%)
- PAIR, GCG 공격에 상대적으로 강건 (34%, 4%)
- **Prompt with Random Search**에 매우 취약 (78%)
- GPT-4에서는 SmoothLLM이 제한적 효과 (78% -> 56%)
- Erase-and-Check가 전반적으로 가장 효과적인 방어

### 오픈소스 vs 클로즈드소스 비교
- AIM 공격: 클로즈드소스 모델이 훨씬 강건 (0% vs Vicuna 90%)
- Prompt with Random Search: 클로즈드소스도 높은 취약성 (GPT-3.5: 93%, GPT-4: 78%)
- 전반적으로 GPT-4가 가장 안전하나, 적응형 공격에는 여전히 취약
