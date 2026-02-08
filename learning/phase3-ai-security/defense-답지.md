# AI/LLM 방어 기법 답지 + 해설

> **학습법**: "왜 이 방어가 작동하는가" 그리고 "왜 결국 뚫리는가"를 함께 이해

---

## 1. 방어 레이어 전체 구조

```
[사용자 입력]
    ↓
Layer 1: Input Filter (키워드/패턴 매칭)        ← 가장 약함
    ↓
Layer 2: Perplexity/Anomaly Detection           ← GCG 전용
    ↓
Layer 3: System Prompt (안전 지시)               ← 우회 가능
    ↓
Layer 4: Safety Training (RLHF/Constitutional AI) ← 핵심 방어
    ↓
Layer 5: Output Filter (생성 후 검열)            ← 최후 방어선
    ↓
[출력]
```

**해설**: 왜 다층 방어가 필요한가?
- 단일 레이어는 반드시 우회됨 (모든 벤치마크가 증명)
- 각 레이어가 다른 유형의 공격을 담당
- **핵심 원칙**: Defense in Depth (심층 방어)

---

## 2. 안전 훈련 방법론 답지

### 2.1 RLHF (Reinforcement Learning from Human Feedback)

**답 (작동 방식)**:
```
1. 유해 질문에 대한 여러 응답 생성
2. 인간 평가자가 "거부" vs "답변" 순위 매김
3. Reward Model 학습: 거부 = 높은 점수
4. PPO로 모델 최적화: 거부하는 방향으로 학습
```

**왜 작동하나?**:
- 인간의 판단 기준을 모델에 직접 주입
- "유해한 것"에 대한 구체적 예시 학습

**왜 뚫리나?**:
- 학습 데이터에 포함되지 않은 새로운 공격 형태
- 인코딩/프레이밍으로 "유해 판단 임계값" 미달
- **Competing Objectives**: "도움이 되라" vs "안전하라" 사이의 충돌

---

### 2.2 Constitutional AI (Anthropic)

**답 (작동 방식)**:
```
1. 모델이 유해 응답 생성
2. "이 응답이 헌법(principles)을 위반하는가?" 자기 평가
3. 위반이면 자체 수정 응답 생성
4. 수정된 응답으로 학습
5. 반복 (Self-Improvement Loop)
```

**왜 Claude가 가장 안전한 이유**:
- RLHF처럼 인간 라벨에만 의존하지 않음
- 모델 스스로 "왜 이것이 유해한가" 추론
- 규칙 기반이 아닌 원칙 기반 → 새로운 공격에도 일반화

**왜 그래도 뚫리나?** (Claude도 Cybercrime에서 34.88%):
- 코딩 도움과 악성 코드의 경계가 모호
- "합법적 사용 사례"로 프레이밍 가능
- 헌법 자체의 모호성

---

### 2.3 Guardrails (외부 방어 시스템)

**답 (아키텍처)**:
```
[사용자] → [Guardrail 입력 검사] → [LLM] → [Guardrail 출력 검사] → [사용자]
                ↓                                    ↓
         유해? → 차단                          유해? → 차단
```

**주요 도구**:
| 도구 | 특성 | 한계 |
|------|------|------|
| Lakera Guard | API 기반, 실시간 | 새로운 공격 패턴 대응 지연 |
| Rebuff | 오픈소스, 자체 호스팅 | 규칙 기반, 적응력 낮음 |
| OpenAI Moderation API | 카테고리별 점수 | OpenAI 모델에 최적화 |
| MCP Gateway (Enkrypt AI) | 런타임 가드레일 | 상용 제품 |

**왜 외부 Guardrail이 필요한가?**:
- 모델 내부 안전만으로는 부족 (34.88% Cybercrime 뚫림)
- 모델 교체해도 방어 유지
- 정책 변경 시 모델 재학습 없이 업데이트 가능

---

## 3. 공격별 최적 방어 매칭

| 공격 기법 | 최적 방어 | 이유 |
|-----------|----------|------|
| GCG (Adversarial Suffix) | SmoothLLM + Perplexity Filter | suffix의 정확한 토큰 의존성 파괴 |
| TAP | Constitutional AI + 출력 필터 | 다양한 프롬프트 변형에 원칙 기반 대응 |
| Crescendo | 대화 히스토리 분석 + 에스컬레이션 탐지 | 점진적 위험 증가 패턴 감지 |
| Hex/Base64 인코딩 | 입력 전처리 (조기 디코딩) | 디코딩 후 안전 검사 적용 |
| Role-Playing (DAN) | RLHF 강화 학습 | 캐릭터 연기와 안전 정책 분리 훈련 |
| Style Injection | 내용 기반 판단 (형식 무시) | 포맷이 아닌 의미에 집중 |
| Prompt Injection | 입력 분리 (신뢰 경계) | 사용자 입력 vs 외부 데이터 구분 |

---

## 4. 모델 제공사별 방어 전략 비교

### Anthropic (Claude)
- Constitutional AI + 강화된 RLHF
- 결과: CASI 95.03, HarmBench ASR 4.39% (최저)
- 강점: 원칙 기반 → 새로운 공격에도 일반화
- 약점: 과도한 거부 (false positive) 경향

### OpenAI (GPT)
- RLHF + 별도 Moderation API
- 결과: CASI 82-86, HarmBench ASR ~23%
- 강점: 대규모 인간 피드백 데이터
- 약점: 타겟 패칭 위주 → 근본적 취약점 미해결

### Google (Gemini)
- Safety Settings API (카테고리별 임계값 조절)
- 결과: HarmBench ASR ~20%
- 강점: 사용자가 안전 수준 조절 가능
- 약점: 낮은 설정에서 취약

### DeepSeek
- 기본 RLHF만 적용
- 결과: TAP 93.50%, 유해 출력 11x
- 강점: 성능 대비 비용 효율
- 약점: 안전 투자 부족, 데이터 오염

---

## 5. MCP/에이전트 시스템 방어 답지

### 13가지 MCP 취약점과 방어 (Enkrypt AI 연구)

| 취약점 | 방어 | 구현 |
|--------|------|------|
| Prompt Injection | 입력 검증 + 컨텍스트 분리 | 사용자 지시와 도구 결과 분리 |
| Tool Poisoning | 도구 정의 버전관리 + 서명 | 코드 리뷰처럼 도구 정의 검증 |
| Command Injection | 미검증 입력 제거 + 화이트리스트 | `shell=True` 금지 |
| SQL Injection | 파라미터화 쿼리 | ORM 사용 권장 |
| Token Theft | 시크릿 관리자 + 최소 권한 | 환경 변수에 토큰 저장 금지 |
| Tool Shadowing | 네임스페이싱 + 레지스트리 | 호모글리프 검사 |
| Supply Chain Attack | 의존성 검증 + 드리프트 모니터링 | 도구 해시 비교 |
| Context Bleeding | 세션 격리 | 도구 간 컨텍스트 공유 최소화 |

### 3계층 보안 스택 (Enkrypt AI 비전)

```
Layer 1: MCP Registry      ← 배포 전: 신뢰된 도구 카탈로그
Layer 2: MCP Scanner        ← 배포 전: 보안 분석
Layer 3: MCP Gateway        ← 런타임: 정책 적용
```

---

## 6. 방어의 근본적 한계 (답지)

### "왜 완벽한 방어는 불가능한가?"

1. **Competing Objectives Problem**
   - "도움이 되라" vs "안전하라" = 근본적 충돌
   - 예: 사이버보안 교육 vs 해킹 도구 제공의 경계

2. **Distribution Shift**
   - 학습 데이터에 없는 새로운 공격 형태 계속 등장
   - 방어 패치 → 새로운 우회 → 다시 패치 (군비 경쟁)

3. **Generalization vs Specificity**
   - 너무 일반적 방어 = 정상 사용 차단 (false positive)
   - 너무 구체적 방어 = 변형에 취약

4. **인간 판단의 모호성**
   - "유해한 것"의 정의가 문화/맥락에 따라 다름
   - RLHF 라벨의 일관성 문제

### CalypsoAI의 핵심 발견:
> "모델이 단독 테스트에서 안전해 보여도, 더 넓은 시스템에 통합하면 새로운 취약점 노출"

→ **시스템 레벨 보안**이 모델 레벨 보안만큼 중요

---

## 7. 실습: 간단한 Guardrail 구현

### Python으로 기본 입출력 필터 만들기

```python
import re

class SimpleGuardrail:
    """가장 기본적인 LLM 가드레일 구현"""

    # Layer 1: 키워드 기반 입력 필터
    BLOCKED_PATTERNS = [
        r"how to (make|build|create) (a )?(bomb|weapon|explosive)",
        r"(hack|crack|break into) .*(system|network|account)",
        r"(write|generate|create) .*(malware|virus|ransomware)",
    ]

    # Layer 2: 인코딩 탐지
    ENCODING_PATTERNS = [
        r"([0-9a-fA-F]{2}\s){5,}",       # hex
        r"[A-Za-z0-9+/]{20,}={0,2}",      # base64
    ]

    def check_input(self, text: str) -> tuple[bool, str]:
        # 키워드 필터
        for pattern in self.BLOCKED_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return False, f"Blocked: matched pattern '{pattern}'"

        # 인코딩 탐지
        for pattern in self.ENCODING_PATTERNS:
            if re.search(pattern, text):
                return False, "Warning: encoded content detected"

        return True, "OK"

    def check_output(self, text: str) -> tuple[bool, str]:
        # 출력에서 유해 콘텐츠 탐지
        dangerous_indicators = [
            r"step \d+:.*(?:mix|combine|inject|exploit)",
            r"import (?:os|subprocess|socket)",  # 위험한 import
        ]
        for pattern in dangerous_indicators:
            if re.search(pattern, text, re.IGNORECASE):
                return False, f"Output blocked: {pattern}"
        return True, "OK"
```

**이 코드의 한계** (왜 실전에서 부족한가):
1. 키워드 매칭은 동의어/우회 표현에 무력
2. 인코딩 탐지가 정상 코드의 base64 사용도 차단
3. 컨텍스트 이해 없이 패턴만 매칭 → 높은 false positive
4. **교훈**: 규칙 기반만으로는 LLM 공격 방어 불가 → AI 기반 방어 필요
