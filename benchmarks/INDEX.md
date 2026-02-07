# LLM Security Benchmark Leaderboard - 통합 인덱스

**최종 업데이트**: 2026-02-08

## 벤치마크 소스 목록

| # | 소스 | 유형 | 디렉토리 | 파일 수 |
|---|------|------|----------|---------|
| 1 | [JailbreakBench](https://jailbreakbench.github.io/) | 학술 | `jailbreakbench/` | 1 |
| 2 | [0DIN](https://0din.ai/blog/) | 실전/버그바운티 | `0din/` | 15 |
| 3 | [CalypsoAI](https://calypsoai.com/calypsoai-model-leaderboard/) | 상업/상세 | `calypsoai/` | 1 |
| 4 | [Enkrypt AI](https://leaderboard.enkryptai.com/) | 상업/간결 | `enkryptai/` | 1 |
| 5 | [Phare (Giskard)](https://phare.giskard.ai/) | 다국어 | `phare/` | 1 |
| 6 | [General Analysis](https://www.generalanalysis.com/benchmarks) | 학술/공격기법별 | `general-analysis/` | 1 |

## 벤치마크 비교 매트릭스

| 차원 | JailbreakBench | 0DIN | CalypsoAI | Enkrypt | Phare | GenAnalysis |
|------|---------------|------|-----------|---------|-------|-------------|
| **접근법** | 학술 표준 | 실전 버그바운티 | 에이전트 레드팀 | 자동화 스캔 | 다국어 평가 | 공격기법별 |
| **평가 모델 수** | 제한적 | ~5 프론티어 | ~20+ | 175+ | 50+ | 23 |
| **메트릭** | ASR, Overrefusal | Jailbreak 수 | CASI, AWR | NIST Risk, OWASP | Avg Safety | ASR |
| **공격 유형** | 표준화 세트 | 450+ 실전 프로브 | 10K+ 에이전트 생성 | 자동화 | 다국어 | TAP, Crescendo, Zero-shot |
| **업데이트** | 비정기 | 실시간 | 월간 | 주간 | 비정기 | 비정기 |
| **강점** | 재현성 | 실전 기반 | 가장 상세 | 가장 넓은 모델 범위 | 다국어 편향 | 공격기법별 상세 비교 |

## 종합 모델 안전성 랭킹 (크로스 벤치마크)

### Tier 1: 최고 안전
| Model | CalypsoAI CASI | Phare Avg | GenAnalysis ASR | 0DIN Jailbreaks | Enkrypt NIST |
|-------|---------------|-----------|-----------------|-----------------|-------------|
| Claude Sonnet 4 | 95.03 (#1) | - | 15.33% | 21 (#2) | - |
| Claude 4.5 Haiku | - | 83.16% (#1) | - | - | - |
| o4-mini | - | - | - | 6 (#1) | - |
| Claude 3 Opus | - | - | - | - | 11% (#1) |

### Tier 2: 매우 안전
| Model | CalypsoAI CASI | Phare Avg | GenAnalysis ASR | Enkrypt NIST |
|-------|---------------|-----------|-----------------|-------------|
| Claude Sonnet 3.5 | 93.61 (#2) | - | 5.0% (#1) | 14% (#4) |
| GPT 5 Nano | 86.44 (#3) | 69.53% | - | 15% (#5) |
| GPT 5 | 82.34 (#7) | 67.20% | - | 12% (#2) |
| Gemini 2.5 Pro | - | 60.55% | 16.08% (#3) | - |

### Tier 3: 주의 필요
| Model | 주요 약점 |
|-------|----------|
| DeepSeek V3 | TAP 공격 93.5% ASR, CASI 낮음 |
| Qwen 계열 | CASI 50 이하 |
| Grok 3 | Phare 53.45%, jailbreak 25.77% |

## 주요 공격 기법 트렌드 (2024-2026)

| 시기 | 공격 기법 | 설명 |
|------|----------|------|
| 2024-10 | Hex Encoding | 16진수로 유해 지시 인코딩 |
| 2024-11 | ASCII Encoding | 문자 코드로 가드레일 우회 |
| 2025-02 | Data Poisoning | 훈련 데이터에 악성 프롬프트 주입 |
| 2025-05 | FRAME/Trolley | 에이전트 시나리오 공격 |
| 2025-06 | Scenario Nesting | 양성 작업 내 유해 지시 삽입 |
| 2025-07 | Style Injection | 포맷팅/작문 스타일로 우회 |
| 2025-07 | IPI (Indirect Prompt Injection) | 이메일 등 외부 콘텐츠 인젝션 |
| 2025-08 | MathPrompt | 수학 표기법 내 유해 요청 위장 |
| 2025-09 | FlipAttack | 호모글리프 유니코드 위장 |
