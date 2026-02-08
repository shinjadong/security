# Phase 4: 월드클래스 레벨 도달 가이드

> **원칙**: "전문가들의 결과물(답지)을 먼저 분석하고, 그 수준에 도달하는 역추적"

---

## Track A: AI Red Team 전문가

### 답지: 이 사람들이 하는 일

| 전문가/조직 | 핵심 Output | 따라가기 |
|------------|------------|---------|
| Simon Willison | Prompt Injection 분류 체계 | simonwillison.net |
| Anthropic Red Team | Constitutional AI, Claude 안전성 | anthropic.com/research |
| OpenAI Red Team | GPT 안전 평가, System Card | openai.com/research |
| 0DIN (Mozilla) | 실제 버그 헌팅 Writeup | 0din.ai/blog |
| Pliny the Liberator | Jailbreak 연구 (DAN 계열) | @elder_plinius |
| General Analysis | HarmBench 기반 벤치마크 | generalanalysis.com |

### 커리어 경로 답지

```
Level 1: Bug Bounty Hunter (지금 시작 가능)
├─ 플랫폼: 0DIN, HackerOne AI
├─ 목표: 첫 버그 리포트 제출
├─ 보상: $500~$5,000/건
└─ 소요: 2-3개월

Level 2: AI Security Researcher (6개월+)
├─ 독자적 Jailbreak 기법 개발
├─ 블로그/논문 발표 (최소 2편)
├─ 컨퍼런스: DEF CON AI Village, NeurIPS
└─ 포트폴리오: GitHub 공개 연구

Level 3: Red Team Lead (1-2년)
├─ 기업 AI 시스템 감사 (컨설팅)
├─ Anthropic/OpenAI 레드팀 참여
├─ 도구 개발: 자동화된 AI 취약점 스캐너
└─ 팀 빌딩: 주니어 레드팀 멘토링

Level 4: World-Class (2년+)
├─ 업계 인지도 (트위터 팔로워, 인용)
├─ 독자적 프레임워크/도구 발표
├─ 정책 자문 (EU AI Act, 한국 AI 규제)
└─ 스타트업 창업 or 빅테크 시니어
```

### AI 버그 바운티 시작 가이드

```
1. 0DIN 가입 (Mozilla)
   └─ 450+ 공개 프로브, 14+ 블로그 writeup
   └─ 매월 CTF 대회 참여

2. HackerOne AI Programs
   └─ OpenAI, Anthropic 등 AI 기업 프로그램
   └─ 범위: jailbreak, data extraction, system prompt leak

3. 첫 리포트 전략
   └─ 기존 기법 변형부터 시작
   └─ Hex + Crescendo 조합 등
   └─ 재현 가능한 PoC 필수
```

---

## Track B: 전통 보안 + AI 융합

### 인증 로드맵 답지

| 인증 | 난이도 | 가격 | 핵심 내용 | 순서 |
|------|--------|------|----------|------|
| **eJPT** | 입문 | $249 | 기초 펜테스트 | 1번째 |
| **OSCP** | 중급 | $1,749 | 실전 침투 테스트 24시간 시험 | 2번째 |
| **OSWE** | 고급 | $1,749 | 웹 앱 보안 소스코드 분석 | 3번째 |
| **OSEP** | 고급 | $1,749 | 우회 기법, AD 공격 | 4번째 |
| **GXPN** | 전문가 | $8,525 | 고급 침투 테스트 | 선택 |

### OSCP 답지 스타일 학습법
```
1. HTB Pro Lab "Dante" 클리어 (OSCP 시뮬레이션)
2. Proving Grounds Practice 30박스
3. TJ_Null의 OSCP 대비 HTB 머신 리스트 전체 풀기
4. 막히면 IppSec 유튜브 Writeup 보기
```

---

## 팔로우할 전문가 답지

### AI 보안 (필수)
| 이름 | 플랫폼 | 핵심 콘텐츠 |
|------|--------|------------|
| Simon Willison | 블로그, X | Prompt Injection 선구자, LLM 보안 분석 |
| Anthropic Blog | 블로그 | Constitutional AI, 안전 연구 |
| Enkrypt AI Blog | 블로그 | 리더보드, MCP 보안, 실증 연구 |
| Marco Figueroa | 0DIN | Hex jailbreak, ChatGPT 탐색 |
| CalypsoAI Blog | 블로그 | 월별 위협 인사이트, 공격 벡터 |

### 전통 보안 (필수)
| 이름 | 플랫폼 | 핵심 콘텐츠 |
|------|--------|------------|
| IppSec | YouTube | HTB 머신 Writeup (교과서급) |
| John Hammond | YouTube | CTF, 악성코드 분석 |
| NahamSec | YouTube, X | Bug Bounty 실전 |
| LiveOverflow | YouTube | 깊은 기술 분석 |
| TomNomNom | GitHub, X | 보안 도구 개발 |

### 뉴스/트렌드 (매일 5분)
| 소스 | 내용 |
|------|------|
| The Hacker News | 보안 뉴스 |
| Krebs on Security | 심층 분석 |
| SANS ISC | 일일 보안 브리핑 |
| r/netsec | 커뮤니티 |

---

## CTF 대회 로드맵

### 입문 (지금 시작)
| 플랫폼 | 특성 | 링크 |
|--------|------|------|
| PicoCTF | 교육용, 가장 쉬움 | picoctf.org |
| OverTheWire | 리눅스 기초 | overthewire.org |
| TryHackMe | 가이드형 학습 | tryhackme.com |

### 중급 (Phase 2 이후)
| 플랫폼 | 특성 | 링크 |
|--------|------|------|
| HackTheBox | 실전 머신 | hackthebox.com |
| VulnHub | 오프라인 VM | vulnhub.com |
| PortSwigger Labs | 웹 보안 전문 | portswigger.net |

### 고급 (Phase 3-4)
| 플랫폼 | 특성 | 링크 |
|--------|------|------|
| 0DIN CTF | AI 보안 특화 | 0din.ai |
| DEF CON CTF | 세계 최고 대회 | defcon.org |
| Google CTF | 어려운 문제 | capturetheflag.withgoogle.com |
| Pwn2Own | 제로데이 대회 | zerodayinitiative.com |

---

## 도구 개발 로드맵

### AI 보안 도구 아이디어 (직접 만들기)

```
Level 1: 자동화 스크립트
├─ Jailbreak 프롬프트 변형 자동 생성기
├─ LLM 응답 안전성 자동 평가기
└─ MCP 서버 기본 보안 스캐너

Level 2: 프레임워크
├─ TAP 공격 자동화 도구
├─ 다중 모델 동시 레드팀 프레임워크
└─ Guardrail 성능 벤치마크 도구

Level 3: 제품
├─ AI 모델 보안 감사 플랫폼
├─ 실시간 Prompt Injection 탐지 서비스
└─ MCP 보안 레지스트리
```

---

## 현실적 마일스톤

| 시점 | 목표 | 검증 방법 |
|------|------|----------|
| 1개월 | Phase 0+1 기본 클리어 | PortSwigger SQLi/XSS 전체 풀기 |
| 3개월 | 첫 AI 버그 리포트 | 0DIN/HackerOne 제출 |
| 6개월 | 나만의 Jailbreak 기법 | 블로그 포스트 or GitHub 공개 |
| 9개월 | OSCP 취득 | 인증서 |
| 12개월 | 컨퍼런스 발표 | DEF CON AI Village or 한국 보안 컨퍼런스 |
| 18개월 | 업계 인지도 | 트위터 팔로워 1000+, 논문 인용 |
