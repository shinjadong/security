# CalypsoAI Security Leaderboard - September 2025

- **URL**: https://calypsoai.com/calypsoai-model-leaderboard/
- **최종 수집일**: 2026-02-08

## 메트릭 설명

### CASI (CalypsoAI Security Index)
프롬프트 인젝션, jailbreak 등 직접 공격에 대한 저항성. 높을수록 안전.
- 심각도(Severity), 복잡도(Complexity), 방어 취약점(Defensive Breaking Point) 가중치 적용
- 단순 ASR과 달리 뉘앙스 있는 평가

### AWR (Agentic Warfare Resistance)
자율적, 다단계 공격 시나리오에서의 성능.
- 복잡한 워크플로우 중 정렬(alignment) 유지 능력 평가
- Required Sophistication / Defensive Endurance / Counter-Intelligence 포함

### RTP (Risk-to-Performance Ratio)
안전성 vs 능력 트레이드오프

### CoS (Cost of Security)
보안 점수 대비 추론 비용

---

## CASI Rankings (2025년 9월)

| Rank | Provider | Model | CASI | Avg Performance | RTP | CoS |
|------|----------|-------|------|-----------------|-----|-----|
| 1 | Anthropic | Claude Sonnet 4 | 95.03 | 45.70% | 0.75 | 18.94 |
| 2 | Anthropic | Claude Sonnet 3.5 | 93.61 | 33.50% | 0.70 | 19.23 |
| 3 | OpenAI | GPT 5 Nano | 86.44 | 53.80% | 0.73 | 0.52 |
| 4 | Anthropic | Claude Sonnet 3.7 | 84.89 | 47.00% | 0.70 | 21.20 |
| 5 | OpenAI | GPT 5 Mini | 84.14 | 46.30% | 0.69 | 2.67 |
| 6 | Anthropic | Claude Haiku 3.5 | 83.59 | 23.30% | 0.59 | 5.74 |
| 7 | OpenAI | GPT 5 | 82.34 | 69.00% | 0.77 | 13.66 |
| 8 | Microsoft | Phi-4 | 79.33 | 27.90% | 0.59 | 0.79 |
| 9 | OpenAI | gpt-oss-120b | 74.76 | 61.30% | 0.69 | 1.00 |
| 10 | DeepSeek | DeepSeek-R1-Distill-Llama-70B | 72.13 | 34.50% | 0.57 | 2.25 |

## AWR Rankings (2025년 9월)

| Rank | Provider | Model | AWR | Avg Performance | RTP | CoS |
|------|----------|-------|-----|-----------------|-----|-----|
| 1 | Anthropic | Claude Sonnet 3.5 | 93.99 | 33.50% | 0.70 | 19.15 |
| 2 | Anthropic | Claude Haiku 3.5 | 91.92 | 23.30% | 0.64 | 5.22 |
| 3 | OpenAI | GPT 5 Mini | 88.31 | 46.30% | 0.72 | 2.55 |
| 4 | OpenAI | GPT 5 Nano | 87.59 | 53.80% | 0.74 | 0.51 |
| 5 | Microsoft | Phi-4 | 87.34 | 27.90% | 0.64 | 0.72 |
| 6 | Anthropic | Claude Sonnet 4 | 86.53 | 45.70% | 0.70 | 20.80 |
| 7 | OpenAI | gpt-oss-120b | 81.07 | 61.30% | 0.73 | 0.93 |
| 8 | Anthropic | Claude Sonnet 3.7 | 79.30 | 47.00% | 0.66 | 22.70 |
| 9 | OpenAI | GPT 5 | 77.20 | 53.80% | 0.68 | 0.58 |
| 10 | OpenAI | gpt-oss-20b | 76.65 | 49.00% | 0.66 | 0.33 |

---

## Threat Insights 타임라인

### 2025년 9월
- **핵심 발견**: 에이전트 레드팀이 AI 에이전트로 10,000개 공격 팩 자동 생성
- **FlipAttack**: 호모글리프(시각적 동일 유니코드 문자)로 악성 프롬프트 위장
- GPT-5 계열: GPT-4 대비 "대폭 보안 개선"
- 소형 모델: jailbreak 로직 이해 부족으로 역설적으로 더 안전

### 2025년 8월
- 에이전트 생성 프롬프트로 공격 복잡도 급증
- 평균 CASI 점수 12.5% 하락
- **MathPrompt Attack**: 집합론/대수/논리 표기법 내 유해 요청 위장

### 2025년 7월
- **Style Injection Attack**: 포맷팅/작문 스타일로 거부 메커니즘 우회
- Crescendo 같은 공개된 공격의 효과 감소 → 근본적 취약점 해결이 아닌 타겟 패칭

### 2025년 6월
- **Scenario Nesting**: 양성 작업(코드 완성, 표 생성) 안에 유해 지시 삽입
- Claude 4 Sonnet CASI 95.12로 1위 데뷔
- 평균 CASI 7% 상승

### 2025년 5월
- **AWR 독립 리더보드 신설**
- **FRAME / Trolley**: 기존 공개 공격보다 효과적인 2개 신규 에이전트 공격
- "모델이 단독 테스트에서 안전해 보여도, 더 넓은 시스템에 통합하면 새로운 취약점 노출"

### 2025년 4월
- 평균 CASI 4% 하락 (개선된 공격 생성 + 신규 공격 벡터)
- Claude 3.7 Sonnet이 3.5보다 낮은 점수 → "Appropriate Harmlessness" 튜닝 영향

## 방법론

### CASI
- Severity Assessment: 경미 ~ 치명적 영향 범위
- Complexity Scoring: 단순 텍스트 vs 정교한 인코딩 스킴
- Defensive Breaking Point: 가장 약한 방어 레이어 식별

### AWR
- Required Sophistication: 시스템 침입 최소 공격자 수준
- Defensive Endurance: 지속적 공격 하 저항 기간
- Counter-Intelligence: 실패한 공격이 필터 정보 누출하는지 여부

## 주의사항
- 기본 모델(base model) 평가, 특정 애플리케이션 아님
- 버전 변경에 따른 스냅샷
- Signature Attacks, Operational Attacks, Agentic Warfare 테스트 벡터 포함
