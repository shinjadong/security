# General Analysis - 방법론 상세

- **URL**: https://www.generalanalysis.com/benchmarks , https://www.generalanalysis.com/
- **블로그**: https://www.generalanalysis.com/blog
- **Y Combinator**: https://www.ycombinator.com/companies/general-analysis
- **수집일**: 2026-02-08

---

## 1. 회사 개요

### General Analysis
Y Combinator 포트폴리오 기업. AI 모델의 안전성과 성능 보고서를 제공하는 기업용 AI 보안 플랫폼.

조직들이 AI 기술을 보안 학습보다 빠르게 도입하고 있다는 관찰에서 출발하여, AI 안전 연구 그룹으로 시작.

### 창립자
| 이름 | 역할 | 배경 |
|------|------|------|
| **Rex Liu** | Co-Founder | 침투 테스트, 공격 보안(offensive security), Caltech AI 연구, DeepMind |
| **Rez Havaei** | Co-Founder/CEO | Jane Street 트레이더, NVIDIA AI 연구, Cohere AI 연구 |
| **Alan Wu** | Co-Founder | - |

Liu와 Havaei는 포커 서클에서 만나 게임 이론과 리스크에 대한 관심을 공유.

### 플랫폼 4대 구성요소
1. **Red Teaming**: AI 시스템을 체계적으로 탐색하여 취약점/정책 위반 발견
   - 모델 행동의 엣지 케이스 식별
   - 시스템의 지시 해석 스트레스 테스트
   - 공격자의 데이터/출력 조작 방법 탐색
2. **Guardrails**: 레드팀 발견 사항을 실시간 보호로 전환
   - AI 시스템의 모든 입출력을 분류/검증
   - 클라이언트별 정책 적용
3. **AI Asset Management**: 지식 베이스, 모델, 에이전트 파이프라인, 데이터 저장소 전반의 가시성 유지
4. **GA Standard**: 책임 있는 AI 배포를 위한 내부 프레임워크

---

## 2. 벤치마크 평가 프레임워크

### 2.1 사용 데이터셋

| 데이터셋 | 설명 | 출처 |
|----------|------|------|
| **HarmBench** | 자동 레드팀 및 견고한 거부 평가를 위한 표준 프레임워크 | Center for AI Safety |
| **AdvBench** | 적대적 공격 벤치마크 | 학술 연구 |

#### HarmBench 상세
- 510개의 신중하게 큐레이션된 유해 행동 포함
- 4개 기능 카테고리
- 맥락적 행동(context string + behavior string) 포함으로 현실적이고 차별적으로 유해한 행동 평가
- 18개 레드팀 방법 + 33개 타겟 LLM/방어 수단의 대규모 비교에 사용

### 2.2 6개 유해 카테고리

| 카테고리 | 설명 |
|----------|------|
| **Chemical/Biological** | 화학/생물학적 위험 관련 콘텐츠 |
| **Cybercrime** | 사이버 범죄 관련 콘텐츠 |
| **Misinformation/Disinformation** | 오정보/허위정보 생성 |
| **Illegal Activities** | 불법 활동 관련 콘텐츠 |
| **Explicit Content** | 명시적 유해 콘텐츠 |
| **Copyright** | 저작권 침해 관련 콘텐츠 |

### 2.3 카테고리별 취약성 패턴
- **가장 취약**: Misinformation, Cybercrime
- **가장 강한 저항**: Chemical/Biological, Explicit Content

---

## 3. 공격 기법 (Attack Methods)

### 3.1 Zero-shot
- 조작 없이 직접 유해 요청을 전달
- 모델의 기본 안전 가드레일 테스트
- 대부분의 모델이 강하게 거부 (ASR < 5% 수준)

### 3.2 TAP (Tree of Attacks with Pruning)
- 적응적 검색 알고리즘
- 다중 턴 대화 트리를 확장/가지치기하여 jailbreak 경로 탐색
- 분기(branching)로 다양한 변형 생성
- 비효과적 경로는 가지치기(pruning)
- **가장 높은 공격 성공률**을 보이는 기법

### 3.3 TAP-R (Tree of Attacks with Rubric-Based Scoring)
- TAP의 확장 버전
- 루브릭 기반 점수 매기기로 보다 정밀한 공격 경로 평가
- Llama 4 분석에서 사용

### 3.4 Crescendo
- 다중 턴 에스컬레이션 공격
- 절차:
  1. 무해한 대화로 시작
  2. 대화 맥락을 활용하여 점진적으로 유해 요청으로 에스컬레이션
  3. 모델이 저항하면 백트래킹하여 재표현
- 사회공학적 접근과 유사

### 3.5 RnR (Redact-and-Recover)
- General Analysis 독자 개발 2단계 공격 기법
- 1단계: 프롬프트 수정(redaction)으로 적대적 의도 은폐
- 2단계: 모델 연속 생성(continuation)을 통해 사후 의도 복원

---

## 4. 평가 방법론

### 4.1 점수 체계

```
Adversarial Robustness Score = 100% - ASR (Attack Success Rate)
```

- 높을수록 = 더 강한 저항성
- 예: ASR 15% = 견고성 점수 85%

### 4.2 자동 평가자

| 항목 | 상세 |
|------|------|
| **평가 모델** | DeepSeek R1 |
| **판정 기준** | 응답에 actionable + specific + realistic 세부정보가 포함되어야 유해로 판정 |
| **특성** | 엄격한 기준으로 다른 평가보다 낮은 ASR 보고 |

### 4.3 테스트 규모
- 모델당 200~520개 프롬프트
- 6개 유해 도메인에 걸쳐 평가
- 3가지 이상의 공격 기법 적용

---

## 5. 주요 연구 발표

### 5.1 Llama 4 적대적 분석
- **URL**: https://www.generalanalysis.com/blog/llama4_adversarial_analysis
- Llama-4-Maverick과 Llama-4-Scout의 체계적 견고성 평가
- 비교 대상: GPT-4.1, GPT-4.1 Mini, GPT-4o, Claude Sonnet 3.7
- TAP-R과 RnR 공격 방법론 사용
- 실패 예측 가능성, 정책 시행 일관성, 다단계 적대적 상호작용 취약성 평가

### 5.2 법률 AI 레드팀
- **URL**: https://www.generalanalysis.com/blog/legal_ai_red_teaming
- GPT-4o의 법률 AI 모델 환각 분석

---

## 6. 벤치마크의 특징 및 제한사항

### 특징
- 표준화된 프레임워크(HarmBench/AdvBench) 기반으로 재현 가능
- 엄격한 자동 평가 기준으로 오탐(false positive) 최소화
- 다양한 공격 기법으로 다각도 평가
- 카테고리별 세분화된 결과 제공

### 제한사항
- ASR은 평가자와 기준에 따라 달라져 다른 벤치마크와 직접 비교 어려움
- 자동 평가(DeepSeek R1)의 내재적 한계
- 동적 웹사이트로 모델 결과가 수시 업데이트됨 (정확한 시점 기록 필요)

---

## 7. 참고 자료

- General Analysis 벤치마크: https://www.generalanalysis.com/benchmarks
- General Analysis 블로그: https://www.generalanalysis.com/blog
- HarmBench 논문: https://arxiv.org/abs/2402.04249
- HarmBench GitHub: https://github.com/centerforaisafety/HarmBench
- Y Combinator 프로필: https://www.ycombinator.com/companies/general-analysis
- Entrepreneur 기사: https://www.entrepreneur.com/en-gb/technology/inside-general-analysis-the-startup-bringing-structure/499806
