# World-Class White Hat Hacker + AI Security Master Roadmap

## 핵심 원칙: "Exploit 먼저 보고, 왜 되는지 파악"

```
일반적 학습: 이론 → 실습 → 응용
탑다운 학습: 최종 Exploit/Writeup → "왜?" → 필요한 개념만 역추적
```

---

## Phase 0: 기초 체력 (2주)

> **목표**: 리눅스/네트워크/프로그래밍 최소 문해력

| 주제 | 답지 | 시간 |
|------|------|------|
| 리눅스 | OverTheWire Bandit 0~15 | 3일 |
| 네트워크 | `tcpdump`, `wireshark` 패킷 캡처 후 분석 | 2일 |
| Python | 소켓 프로그램 복붙 후 수정 | 2일 |

### 해설지 (막힐 때만)
- 리눅스: https://linuxjourney.com
- 네트워크: TCP/IP 4계층 다이어그램
- Python: 문법은 AI에게 질문

→ 상세: [phase0-basics/](phase0-basics/)

---

## Phase 1: 웹 해킹 기초 (4주)

> **목표**: OWASP Top 10 전부 실제로 터뜨려보기

### 주별 계획
- **Week 1**: SQL Injection - PortSwigger Labs 답안 먼저 → sqlmap 자동화 → 수동 재현
- **Week 2**: XSS - DOM/Reflected/Stored 차이 이해
- **Week 3**: Auth/Session - JWT, Session, Cookie 구조 + Burp Suite 토큰 조작
- **Week 4**: SSRF, XXE, Deserialization - HackTheBox 쉬운 웹 머신 Writeup 5개

### 핵심 도구
- Burp Suite Pro ($449/년) - 프록시, 생산성 10배
- ffuf - 퍼징
- sqlmap - SQLi 자동화

→ 상세: [phase1-web-hacking/](phase1-web-hacking/)

---

## Phase 2: 시스템 해킹 + 권한 상승 (6주)

> **목표**: 리눅스/윈도우 박스 root/admin 따기

### 주별 계획
- **Week 1-2**: HackTheBox Easy 10박스 Writeup 정독 (Lame, Jerry, Blue, Netmon, Archetype)
- **Week 3-4**: HTB Medium 5박스 직접 풀기, 막히면 Writeup → 역추적
- **Week 5-6**: TryHackMe "Complete Beginner" → "Offensive Pentesting" → AD 경로

### 핵심 도구
- nmap, gobuster, linpeas, winpeas
- GTFOBins (Linux), LOLBAS (Windows)

→ 상세: [phase2-system-hacking/](phase2-system-hacking/)

---

## Phase 3: AI/LLM 보안 특화 (4주)

> **목표**: Jailbreak/Prompt Injection 실제 공격 & 방어

### 주별 계획
- **Week 1**: Jailbreak 기법 전체 조망 - JailbreakBench artifacts 분석
- **Week 2**: Prompt Injection 공격 - Indirect PI, RAG 시스템 공격
- **Week 3**: 방어 기법 분석 - Constitutional AI, Moderation API, Guardrails
- **Week 4**: Red Team 실전 - 0DIN/HackerOne 버그바운티, 나만의 기법 개발

### 필독 논문 3편
1. "Jailbroken: How Does LLM Safety Training Fail?" - 안전 훈련 실패 구조
2. "Universal and Transferable Adversarial Attacks on Aligned LLMs" - GCG 공격 원리
3. "Ignore This Title and HackAPrompt" - Prompt Injection 분류 체계

→ 상세: [phase3-ai-security/](phase3-ai-security/)

---

## Phase 4: Advanced + 전문화 (8주+)

> **목표**: 월드클래스 레벨 도달

### Track A: AI Red Team 전문가
- Anthropic/OpenAI Red Team 지원
- 독자적 Jailbreak 연구 & 발표
- Bug Bounty: 0DIN, HackerOne AI
- 자동화 AI 취약점 스캐너 개발

### Track B: 전통 보안 + AI 융합
- OSCP → OSWE → OSEP
- AI 기반 보안 도구 개발
- 기업 펜테스트 + AI 시스템 감사

### 팔로우할 전문가
- @simonw - Prompt Injection 선구자
- @IppSec - 시스템 해킹 교과서 (유튜브)
- @NahamSec - Bug Bounty
- Anthropic/OpenAI Research Blog

→ 상세: [phase4-advanced/](phase4-advanced/)

---

## 타임라인

| 기간 | Phase | 목표 |
|------|-------|------|
| Month 1-2 | Phase 0+1 | PortSwigger 전체 클리어 |
| Month 3-4 | Phase 2 | HTB Medium 혼자 풀기 |
| Month 5-6 | Phase 3 | 나만의 Jailbreak 기법 개발 + 버그 리포트 1건 |
| Month 7+ | Phase 4 | 인증 취득 or 연구 발표, 업계 인지도 확보 |
