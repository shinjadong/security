# CalypsoAI 보안 리더보드 2025년 8월 - 에이전틱 공격 팩으로 모델 보안 점수 하락

- **URL**: https://calypsoai.com/news/calypsoai-security-leaderboards-august-2025/
- **날짜**: 2025-08-01
- **수집일**: 2026-02-08
- **저자**: Jessica Brennan

---

## CalypsoAI Agentic Signature Attack Packs Force Model Security Scores Lower

CalypsoAI released its August 2025 security leaderboards demonstrating significant vulnerabilities in AI models when tested against agent-generated attack prompts. The research reveals concerning gaps in model safety as autonomous attack techniques evolve.

### Main Finding

"Security scores fell by an average of 12.5% compared to human-driven testing" when models faced CalypsoAI's complete 10,000-prompt agentic attack pack -- the first time their full arsenal was entirely agent-generated.

### Top Security Rankings

**CASI Leaderboard (Direct Attack Resistance):**

| Model | Score |
|-------|-------|
| Claude Sonnet 4 | 94.57 (highest) |
| Claude Sonnet 3.5 | Follow-up |
| Claude Sonnet 3.7 | Follow-up |
| Claude Haiku 3.5 | Follow-up |
| Grok 4 | 3.32 (lowest score ever recorded) |
| Mistral models (avg) | 13.36 |

**AWR Leaderboard (Agentic Warfare Resistance):**

| Model | Score |
|-------|-------|
| Claude Sonnet 3.5 | 93.99 (top performer) |
| Claude Haiku 3.5 | 91.92 |

### New Attack Vector

The leaderboards introduce **MathPrompt**, a jailbreaking technique using mathematical notation to disguise harmful requests.

### Key Takeaways

- 에이전트 생성 공격이 인간 주도 테스트 대비 평균 12.5% 보안 점수 하락 유발
- Claude Sonnet 4가 CASI 리더보드 1위 (94.57)
- Grok 4가 역대 최저 점수 기록 (3.32)
- Mistral 모델들 평균 13.36으로 심각한 취약성
- MathPrompt: 수학적 표기법을 이용한 새로운 탈옥 기법 등장
- Claude Sonnet 3.5가 AWR (에이전틱 전쟁 저항) 리더보드 1위 (93.99)
