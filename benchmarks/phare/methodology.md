# Phare (Giskard) - 벤치마크 방법론 상세

- **URL**: https://phare.giskard.ai/ , https://phare.giskard.ai/principles/
- **논문**: https://arxiv.org/abs/2505.11365 (Phare: A Safety Probe for Large Language Models)
- **GitHub**: https://github.com/Giskard-AI/phare
- **HuggingFace 데이터셋**: https://huggingface.co/datasets/giskardai/phare
- **수집일**: 2026-02-08
- **참고**: Phare V2 블로그 (https://www.giskard.ai/knowledge/reasoning-models-dont-guarantee-better-security)

---

## 1. 개요

**Phare** (Potential Harm Assessment & Risk Evaluation)는 Giskard AI가 개발한 독립적, 다국어 LLM 안전성 벤치마크이다.
Google DeepMind, European Commission 등과 협력하여 개발되었으며, 데이터셋과 코드가 공개되어 있다.

핵심 목적: LLM의 안전성 취약점을 체계적으로 진단 (순위보다 실패 모드 발견에 초점)

---

## 2. 평가 모듈 (4개 차원)

### 2.1 Hallucination (환각/신뢰성)

환각 모듈은 3가지 보완적 하위 작업으로 구성:

#### 2.1.1 Factuality (사실성)
- 구조화된 질의응답 작업을 통해 모델의 사실 정확도 측정
- 모델이 정립된 정보를 얼마나 정확하게 검색/전달하는지 평가
- 프롬프트 자신감, 어휘적 프레이밍, 신뢰할 수 없는 출처 노출에 따른 오정보 확산 경향 평가

#### 2.1.2 Misinformation Resistance (오정보 저항성)
- 모호하거나 잘못 구성된 질문에 대해 올바르게 반박하는 능력 측정
- 잘못된 질문을 지지하는 서사를 생성하는 대신 정확히 거부하는지 평가
- 비사실적/풍자적 자료 포함하여 테스트

#### 2.1.3 Debunking (디벙킹)
- 유사과학, 음모론, 도시전설을 식별하고 반박하는 능력 테스트
- 모델이 이를 강화/증폭하는 대신 올바르게 디벙킹하는지 평가

#### 2.1.4 Tool Reliability (도구 신뢰성)
- 외부 함수(API, 데이터베이스 등)를 정확하게 활용하는 능력 측정
- 현실적이고 불완전한 사용자 요청 하에서 도구 호출의 견고성 평가

### 2.2 Bias & Stereotypes (편향/고정관념)

#### 핵심 접근법: 생성-식별 격차 (Generation-Discrimination Gap)
- 기존 벤치마크와 달리 **개방형 창작 작업**에서 자연 생성 콘텐츠를 평가
- 인위적 제약이 아닌 실제 사용 패턴을 반영

#### Self-Coherency (자기일관성) 프레임워크
- 모델 스스로의 패턴을 평가하는 혁신적 방법론
- 절차:
  1. 각 언어별 약 80개의 스토리를 고정 속성으로 생성
  2. GPT-4o-mini와 Gemini 2.0 Flash로 올바른 속성 추출 능력 평가
  3. 모델의 스토리에서 통계적 연관성 식별
  4. 같은 모델에게 이 패턴이 수용 가능한 상관관계인지 문제적 고정관념인지 질문
- **Self-Coherency Score** = 자기일관적 패턴의 비율 (%)
- 핵심 발견: 모델들이 직접 질문 시 고정관념을 인식하면서도 생성 행동에서 동일 고정관념을 재현

#### 평가 대상
- 차별적 콘텐츠
- 사회적 고정관념의 강화
- 특정 인구통계적 속성에 대한 체계적 편향

### 2.3 Harmful Content (유해 콘텐츠)

#### Vulnerable Misguidance (취약계층 오도)
- 독성이나 욕설이 아닌 **미묘한 형태의 해악**에 초점
- 사용자가 암묵적으로 유해 행동의 확인/인정을 구할 때 모델 반응 평가
- 테스트 시나리오:
  - 섭식 장애 관련 행동 확인 요청
  - 약물 오남용 관련 질문
  - 위험한 관행에 대한 검증 요청
- 평가 기준:
  - 적절한 주의 표현
  - 대안 제시
  - 전문가 상담 권유
  - 안전하지 않은 행동 강화 방지

#### Dangerous Behavior Endorsement (위험 행동 승인)
- 모델이 명시적으로 위험한 활동(범죄 행위 등)에 대한 요청에 어떻게 반응하는지 평가
- 무단 의료 조언 등 잠재적 유해 오정보 포함

### 2.4 Jailbreak (V2에서 추가)

#### 공격 유형
| Scorer | 설명 |
|--------|------|
| `jailbreak/encoding` | 인코딩 기반 우회 (base64, rot13 등) |
| `jailbreak/framing` | 프레이밍 공격 (역할극, 시나리오 설정 등) |
| `jailbreak/injection` | 프롬프트 인젝션 기반 우회 |

#### 평가 내용
- 안전 가드레일을 우회하여 유해 콘텐츠 생성을 유도하는 시도에 대한 저항성
- 추론 모델의 경우 프레이밍 공격에 대한 개선된 저항성 확인

---

## 3. 지원 언어

| 언어 | 코드 | 상태 |
|------|------|------|
| English | en | V1부터 지원 |
| French | fr | V1부터 지원 |
| Spanish | es | V1부터 지원 |

향후 언어 확장 계획 있음. 각 언어별로 문화적 다양성을 반영한 데이터를 처음부터 수집.

### 언어별 차이 발견
- 환각(오정보, 사실성) 및 유해 오도에서 유의미한 언어 격차 존재
- 프랑스어/스페인어 모델이 영어보다 더 취약한 경향

---

## 4. 평가 방법론 상세

### 4.1 데이터 파이프라인
1. **Source Gathering**: 언어별 콘텐츠 수집 (진정한 사용 패턴 반영)
   - 뉴스 기사, 위키피디아, 풍자 기사, 포럼 글
   - AI 사고 데이터베이스 사례
   - 차별적 속성에 관한 법률 문서
2. **Test Case Transformation**: 소스 자료를 평가 테스트 케이스로 변환
   - 테스트 프롬프트 + 평가 기준 쌍 생성
3. **Human Review**: 모든 샘플에 대한 인간 주석 및 품질 검증

### 4.2 모듈 구성
각 테스트 컴포넌트는 3개 파라미터로 정의:
- **Topic Area** (주제 영역)
- **Input/Output Modality** (입출력 모달리티)
- **Target Language** (대상 언어)

### 4.3 스코어링 시스템

#### LLM Judge (다수결 투표)
- 3개 모델 사용: **GPT-4o**, **Gemini 1.5 Pro**, **Claude 3.5 Sonnet**
- 동일 프롬프트, temperature=0
- 다수결(majority-vote) 전략으로 각 응답 평가
- Factuality, Misinformation, Debunking, Harmful Content 서브모듈에 적용

#### 점수 산출
- 각 모듈별 점수 = 모든 태스크와 언어의 평균
- 전체 안전성 점수 = 4개 모듈 점수의 평균

#### 인간 검증
- 서브모듈당 100개 출력을 수동 리뷰
- 언어 및 예측 레이블별로 균형 잡힌 샘플링
- 주석자가 각 샘플을 분류하고 스코어러와의 일치도 보고

### 4.4 데이터셋 관리
- 모델 학습 데이터에 벤치마크 데이터가 포함되지 않도록 **비공개 홀드아웃 데이터셋** 사용
- 독립적 검증을 위해 상당 부분의 샘플을 **공개 세트**로 릴리스
- JSONL 포맷으로 저장 (sample_id, module, task, language, generation_requests)

---

## 5. 평가 모델 목록 (V2 기준, 2026-01-05 업데이트)

### 제공사별 평가 모델
| Provider | Models |
|----------|--------|
| **Anthropic** | Claude 4.5 Haiku, Claude 4.5 Opus, Claude 4.5 Sonnet, Claude 4.1 Opus, Claude 3.7 Sonnet, Claude 3.5 Haiku, Claude 3.5 Sonnet |
| **OpenAI** | GPT-5, GPT-5 mini, GPT-5 nano, GPT-5.1, GPT-4o, GPT-4o mini, GPT-4.1, GPT-4.1 mini, GPT-4.1 nano, GPT OSS 120B |
| **Google** | Gemini 3.0 Pro Preview, Gemini 2.5 Pro, Gemini 2.5 Flash, Gemini 2.5 Flash Lite, Gemini 2.0 Flash, Gemini 2.0 Flash Lite, Gemma 3 27B IT, Gemma 3 12B IT |
| **Meta** | Llama 4 Maverick, Llama 4 Scout, Llama 3.1 405B Instruct, Llama 3.3 70B, Llama 3.1 8B |
| **Alibaba Qwen** | Qwen Plus, Qwen 3 Max, Qwen 3 8B, Qwen 3 30B VL, Qwen 2.5 Max |
| **Mistral** | Mistral Large 3, Mistral Large 2, Mistral Small 3.2, Mistral Small 3.1, Mistral Medium, Magistral Medium, Magistral Small |
| **DeepSeek** | DeepSeek V3.1, DeepSeek V3, DeepSeek V3 0324, DeepSeek R1 0528 |
| **xAI** | Grok 4, Grok 4 Fast, Grok 3, Grok 3 mini, Grok 2 |
| **Cohere** | Command A |

총 50+ 모델 평가 (전체 점수 기준 상위 50개 + 부분 점수 모델)

---

## 6. 핵심 발견 사항

### 6.1 추론 모델 != 더 나은 보안
- 추론 능력의 향상이 보안/안전성/견고성 향상과 반드시 상관관계를 갖지 않음
- GPT-5 vs GPT-4o, Gemini 1.5 Pro vs Gemini 3 Pro, Claude 3.5 Sonnet vs Claude 4.5 Sonnet 비교 시 환각 저항성의 통계적으로 유의미한 개선 없음

### 6.2 Jailbreak 저항성
- Anthropic 모델: 모두 75%+ 저항률
- Google 모델 (Gemini 3.0 Pro 제외): 50% 미만, 최저 27%
- 모델 크기와 jailbreak 공격 저항성 사이 의미 있는 상관관계 없음
- 추론 모델은 특히 프레이밍 공격에 대해 개선된 저항성

### 6.3 편향
- LM Arena의 ELO 등급과 편향 생성/인식 능력 사이 통계적 상관관계 없음
- 모든 평가 모델이 창작 생성에서 잠재적으로 유해한 고정관념 표출
- 직접 질문 시에는 이를 거부 (생성-식별 격차)

### 6.4 유해 콘텐츠
- 일관되게 높은 저항성 (70-100%)
- 신세대 모델이 이전 세대보다 성능 우수 (모델 크기 무관)
- 해악 방지 기술에 개발자들의 상당한 관심 반영

---

## 7. 기술 인프라

### GitHub 저장소 구조
- 샘플 포맷: JSONL (module, task, lang, generation_requests)
- 스코어러 이름이 데이터셋 카테고리에 직접 매핑
- 설정에서 스코어러 추가/제거로 평가 범위 조절 가능

### 파트너 및 후원
- Google DeepMind
- European Commission
- Open Collective (phare-llm-benchmark)

---

## 8. 참고 자료

- 논문: Le Jeune, P. (2025). "Phare: A Safety Probe for Large Language Models." arXiv:2505.11365
- Phare V2 분석: https://huggingface.co/blog/davidberenstein1957/phare-llm-benchmark-v2
- 환각 분석: https://huggingface.co/blog/davidberenstein1957/phare-analysis-of-hallucination-in-leading-llms
- 편향 분석: https://www.giskard.ai/knowledge/llms-recognise-bias-but-also-reproduce-harmful-stereotypes
- 유해 오도 분석: https://www.giskard.ai/knowledge/beyond-sycophancy-the-risk-of-vulnerable-misguidance-in-ai-medical-advice
