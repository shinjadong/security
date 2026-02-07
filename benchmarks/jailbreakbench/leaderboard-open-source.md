# JailbreakBench - 오픈소스 모델 리더보드

- **URL**: https://jailbreakbench.github.io/tables/table_open_source.html
- **수집일**: 2026-02-08
- **설명**: JailbreakBench 오픈소스 LLM 모델에 대한 탈옥 공격 성공률 리더보드. 다양한 공격 기법(PAIR, GCG, AIM, Prompt with Random Search)과 방어 기법(SmoothLLM, Perplexity filter, Erase-and-Check 등)의 조합별 성공률을 보여준다.

---

## 리더보드 테이블

### 대상 모델
- **Vicuna-13B**: 안전 정렬이 약한 오픈소스 모델
- **Llama-2-7B**: Meta의 안전 정렬 오픈소스 모델

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
| Vicuna-13B | None | 34 | 69% |
| Llama-2-7B | None | 88 | 0% |
| Vicuna-13B | SmoothLLM | 34 | 55% |
| Llama-2-7B | SmoothLLM | 88 | 0% |
| Vicuna-13B | Perplexity filter | 34 | 69% |
| Llama-2-7B | Perplexity filter | 88 | 0% |
| Vicuna-13B | Erase-and-Check | 34 | 0% |
| Llama-2-7B | Erase-and-Check | 88 | 0% |
| Vicuna-13B | Synonym Substitution | 34 | 22% |
| Llama-2-7B | Synonym Substitution | 88 | 0% |
| Vicuna-13B | Remove Non-Dictionary | 34 | 0% |
| Llama-2-7B | Remove Non-Dictionary | 88 | 1% |

---

## 2. GCG 공격 (White-box, Suffix attack)

- **논문**: Universal and Transferable Adversarial Attacks on Aligned Language Models
- **날짜**: 2023-07-27
- **위협 모델**: White-box
- **특징**: Suffix 기반 공격, 256K 쿼리 사용

| Model | Defense | Avg Queries | Success Rate |
|-------|---------|-------------|--------------|
| Vicuna-13B | None | 256K | 80% |
| Llama-2-7B | None | 256K | 3% |
| Vicuna-13B | SmoothLLM | 256K | 4% |
| Llama-2-7B | SmoothLLM | 256K | 0% |
| Vicuna-13B | Perplexity filter | 256K | 3% |
| Llama-2-7B | Perplexity filter | 256K | 1% |
| Vicuna-13B | Erase-and-Check | 256K | 17% |
| Llama-2-7B | Erase-and-Check | 256K | 1% |
| Vicuna-13B | Synonym Substitution | 256K | 11% |
| Llama-2-7B | Synonym Substitution | 256K | 0% |
| Vicuna-13B | Remove Non-Dictionary | 256K | 18% |
| Llama-2-7B | Remove Non-Dictionary | 256K | 0% |

---

## 3. AIM 공격 (Black-box, Jailbreak Chat)

- **논문**: Jailbreak Chat
- **날짜**: 2023-03-01
- **위협 모델**: Black-box

| Model | Defense | Avg Queries | Success Rate |
|-------|---------|-------------|--------------|
| Vicuna-13B | None | -- | 90% |
| Llama-2-7B | None | -- | 0% |
| Vicuna-13B | SmoothLLM | -- | 73% |
| Llama-2-7B | SmoothLLM | -- | 0% |
| Vicuna-13B | Perplexity filter | -- | 90% |
| Llama-2-7B | Perplexity filter | -- | 0% |
| Vicuna-13B | Erase-and-Check | -- | 1% |
| Llama-2-7B | Erase-and-Check | -- | 0% |
| Vicuna-13B | Synonym Substitution | -- | 17% |
| Llama-2-7B | Synonym Substitution | -- | 0% |
| Vicuna-13B | Remove Non-Dictionary | -- | 89% |
| Llama-2-7B | Remove Non-Dictionary | -- | 0% |

---

## 4. Prompt with Random Search (Logprob access)

- **논문**: Jailbreaking Leading Safety-Aligned LLMs with Simple Adaptive Attacks
- **날짜**: 2024-04-02
- **위협 모델**: Logprob access
- **특징**: Self-transfer suffixes 사용

| Model | Defense | Avg Queries | Success Rate |
|-------|---------|-------------|--------------|
| Vicuna-13B | None | 2 | 89% |
| Llama-2-7B | None | 25 | 90% |
| Vicuna-13B | SmoothLLM | 2 | 68% |
| Llama-2-7B | SmoothLLM | 25 | 0% |
| Vicuna-13B | Perplexity filter | 2 | 88% |
| Llama-2-7B | Perplexity filter | 25 | 73% |
| Vicuna-13B | Erase-and-Check | 2 | 24% |
| Llama-2-7B | Erase-and-Check | 25 | 25% |
| Vicuna-13B | Synonym Substitution | 2 | 2% |
| Llama-2-7B | Synonym Substitution | 25 | 0% |
| Vicuna-13B | Remove Non-Dictionary | 2 | 91% |
| Llama-2-7B | Remove Non-Dictionary | 25 | 0% |

---

## 주요 분석 요약

### Vicuna-13B (안전 정렬 약함)
- 방어 없이 대부분 공격에 높은 취약성 (69~90%)
- **Erase-and-Check** 방어가 가장 효과적 (PAIR 0%, AIM 1%)
- GCG 공격에 대해서는 SmoothLLM이 효과적 (80% -> 4%)

### Llama-2-7B (안전 정렬 강함)
- 기본적으로 대부분 공격에 강건 (0~3%)
- **Prompt with Random Search**에만 취약 (90%)
- Perplexity filter 방어 시에도 73% 공격 성공 (Prompt with Random Search)
