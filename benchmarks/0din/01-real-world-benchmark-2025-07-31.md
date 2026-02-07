# 0DIN's Real-World Jailbreak Benchmark: The Gold Standard For LLM Security Evaluation

- **URL**: https://0din.ai/blog/0din-s-real-world-jailbreak-benchmark-the-gold-standard-for-llm-security-evaluation
- **저자**: Marco Figueroa
- **날짜**: 2025-07-31
- **수집일**: 2026-02-08

## 평가 방법론

2가지 상호 보완적 데이터 소스:

### 1. 커뮤니티 기반 취약점 보고
- 6대륙 글로벌 보안 연구자 네트워크
- 0DIN 플랫폼을 통한 jailbreak 시도 제출
- 취약점 테스트 70% 이상 시 보상 지급

### 2. 자동 스캐너 스윕
- 전 프론티어 모델에 대한 주간 평가
- 전용 0DIN Scanner 프로브로 자율 테스트
- **현재 규모**: 450개 이상 활성 프로브

---

## Top 5 가장 안전한 모델 랭킹

| Rank | Model | Jailbreaks | 핵심 특성 |
|------|-------|-----------|----------|
| 1 | o4-mini | 6 | Fast-Fail Guardrail |
| 2 | Claude Sonnet 4 | 21 | Hybrid Reasoning Guardian |
| 3 | GPT-4o | 28 | Omni-Modal Sentinel |
| 4 | Claude Opus 4 | 38 | ASL-3 Fortress |
| 5 | Claude Sonnet 3.7 | 82 | Extended Thinking Sentinel |

---

## 상세 모델 분석

### 1. o4-mini — Fast-Fail Guardrail (6 Jailbreaks)

**방어 아키텍처 (3층)**:
1. **Multimodal Moderation Pipeline**: 텍스트-이미지 동시 스코어링 → ASCII art/스테가노그래피 공격 차단
2. **Segmented Context Window Processing**: 프롬프트를 의미 세그먼트로 분할, 고위험 부분 UUID로 교체 후 정책 검증
3. **Truncated Reasoning Traces**: 공개 API에서 내부 추론 체인 대폭 축약 → 공격자 피드백 차단

### 2. Claude Sonnet 4 — Hybrid Reasoning Guardian (21 Jailbreaks)

**특징**:
- 단일 대화 내 빠른 추론 ↔ 확장된 사고 모드 전환
- 불필요 거부 45% 감소 (표준 모드), 31% 감소 (확장 사고 모드) vs Claude 3.5 Sonnet
- 50+ 취약점 테스트에서 90.0% 통과율
- **더 많은 jailbreak 이유**: 에이전트 기능 → 확대된 공격면

### 3. GPT-4o — Omni-Modal Sentinel (28 Jailbreaks)

**방어 메커니즘**:
- 통합 멀티모달 정책 방화벽: 11개 유해 카테고리 위험 점수
- 실시간 음성 모니터링: 45개 언어에서 ≥95% 정밀도, 100% 재현율
- 글로벌 레드팀 피드백 루프: 29개국 100+ 외부 전문가
- 보호된 Chain-of-Thought: 정제된 요약만 API 사용자에게 전달
- **잔여 취약점**: 오디오 입력 → 음성 프롬프트 인젝션, 배경 노이즈 스테가노그래피

### 4. Claude Opus 4 — ASL-3 Fortress (38 Jailbreaks)

**고급 안전 아키텍처**:
- RSP (Responsible Scaling Policy) 게이팅: ASL-3 공개 최고 안전 등급
- Constitutional AI v2.0: 42개 원칙, 다단계 자기비판 후 응답 재작성
- Dynamic Prompt-Classifier Ensemble: 경량 트랜스포머가 실시간 부분 생성 모니터링
- 연속 취약점 흡수: 외부 jailbreak 보고 → RLHF 업데이트

### 5. Claude Sonnet 3.7 — Extended Thinking Sentinel (82 Jailbreaks)

**특징**:
- 확장된 토큰 시퀀스로 깊은 추론
- 불필요 거부 45% 감소 vs 전작
- 37개 jailbreak 시도 100% 차단 (독립 테스트)
- **높은 jailbreak 수 이유**: 확장 사고 → 더 많은 논리 경로 → 정교한 공격의 표면적 확대

---

## 핵심 교훈

1. **안전을 핵심 아키텍처에 내장**: wrapper 기반 방어보다 효과적 (o4-mini)
2. **동적 증거 기반 헌법 채택**: 실제 침해 기반 보안 프레임워크 진화 (Opus)
3. **전체 규모 적대적 시나리오 시뮬레이션**: 정적 프롬프트 라이브러리로는 시간적 패턴 놓침
4. **계층적 스로틀링/샌드박싱**: 불완전해도 방어 업그레이드 시간 확보

## 결론

- 보안은 정적 체크포인트 → 능동적 진화 시스템으로 전환
- **혁신-취약점 패러독스**: 기능 확장마다 새 공격면 생성
- 3대 핵심 실천: Constitutional Alignment > Continuous Red-Teaming > Adaptive Threat Modeling
