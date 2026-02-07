# Enkrypt AI Safety Leaderboard

- **URL**: https://leaderboard.enkryptai.com/
- **문서**: https://docs.enkryptai.com/resources/leaderboard
- **최종 수집일**: 2026-02-08

## 평가 카테고리 (5개)

1. **Bias (편향)**: 모델 출력의 내재된 편견/차별 패턴
2. **Harmful Content (유해 콘텐츠)**: 유해 목적 콘텐츠 생성 위험
3. **Toxicity (독성)**: 모욕적/공격적 언어 생성 확률
4. **CBRN**: 화학/생물/방사능/핵 관련 위험
5. **Insecure Code Generation (불안전 코드)**: 취약한 코드 생성 위험

## 점수 체계

### NIST Risk Score
- 0~62.5 범위
- 낮을수록 안전
- 5개 테스트 카테고리 평균 위험 백분율

### Enkrypt AI Rating
- NIST Risk Score를 역으로 매핑
- 5 (안전) ~ 0 (위험)
- 높을수록 안전

### OWASP Score
- OWASP Top 10 for LLMs 2025 기준 가중 평균
- LLM01 Prompt Injection (가중치 10) ~ LLM10 Unbounded Consumption (가중치 1)

## Top 50 모델 랭킹 (2026년 2월 기준)

| Rank | Model | NIST Risk | OWASP | Bias% | Harmful% | Toxicity% | CBRN% | Insecure Code% |
|------|-------|-----------|-------|-------|----------|-----------|-------|---------------|
| 1 | claude-3-opus-20240229 | 11% | 13% | 25.58 | 7.78 | 0.09 | 4.33 | 15.11 |
| 2 | gpt-5 | 12% | 14% | 40.05 | 6.67 | 2.91 | 7.11 | 2.22 |
| 3 | Mistral-NeMo-Minitron-8B | 14% | 13% | 7.49 | 45.56 | 0 | 6.67 | 10.22 |
| 4 | claude-3-5-sonnet-20241022 | 14% | 19% | 35.4 | 0 | 0.09 | 1.83 | 32.89 |
| 5 | gpt-5-nano | 15% | 18% | 60.98 | 7.22 | 3.09 | 2 | 1.33 |

*(전체 175+ 모델 포함)*

## 핵심 인사이트

- **1위**: Claude 3 Opus (NIST 11%)
- **Claude 계열**: 상위 안전성 위치 지배
- **Bias가 가장 높은 위험 카테고리**: 7~99% 범위
- **Toxicity가 가장 낮음**: 0~34%
- **GPT-5**: 2위 (NIST 12%)

## vs 다른 리더보드

Enkrypt AI의 차별점:
- Azure Foundry 비판: 직접 프롬프트만 평가, jailbreak/프롬프트 인젝션/CoT 누출/스타일 전환 회피 미포함
- 단일 턴 평가 → 실제 동적 공격 놓침
- Enkrypt: 5개 위험 카테고리, NIST 프레임워크 직접 매핑

## 업데이트 주기
- 신규 모델: Day Zero 업데이트
- 모델 업데이트: 주간 갱신
