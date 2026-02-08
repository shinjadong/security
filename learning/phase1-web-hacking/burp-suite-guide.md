# Burp Suite 실전 가이드

> 최종 업데이트: 2026-02-08
> Burp Suite Community/Professional Edition 2025.x 기준

---

## 목차

1. [개요 및 설치](#개요-및-설치)
2. [Proxy 설정](#proxy-설정)
3. [Target 분석](#target-분석)
4. [Repeater 사용법](#repeater-사용법)
5. [Intruder 공격 설정](#intruder-공격-설정)
6. [Scanner (Pro)](#scanner-pro)
7. [유용한 확장 프로그램](#유용한-확장-프로그램)
8. [실전 워크플로우](#실전-워크플로우)

---

## 개요 및 설치

### Burp Suite란?

웹 애플리케이션 보안 테스트를 위한 통합 플랫폼. HTTP/HTTPS 트래픽을 가로채고(intercept), 분석하고, 수정하여 취약점을 발견하는 도구.

### 에디션 비교

| 기능 | Community (무료) | Professional |
|------|-----------------|-------------|
| Proxy | O | O |
| Repeater | O | O |
| Intruder | 제한 (속도 제한) | O (무제한) |
| Scanner | X | O (자동 스캔) |
| Collaborator | X | O (OOB 탐지) |
| 확장 프로그램 | O | O |

### 설치

```bash
# Kali Linux (기본 설치됨)
burpsuite

# 다른 Linux
# 1. https://portswigger.net/burp/releases 에서 다운로드
chmod +x burpsuite_community_linux_*.sh
./burpsuite_community_linux_*.sh

# Java 필요 (Burp이 자체 JRE 포함하지만, 별도 설치 시)
sudo apt install default-jdk
```

---

## Proxy 설정

### 답지: 설정 방법

#### 1단계: Burp Proxy Listener 확인

```
Proxy 탭 > Proxy settings > Proxy Listeners
기본값: 127.0.0.1:8080
```

#### 2단계: 브라우저 프록시 설정

**방법 A: Burp 내장 브라우저 (추천)**

```
Proxy 탭 > Intercept > Open browser
# Chromium 기반 브라우저가 열리며 프록시 자동 설정됨
# CA 인증서도 자동 설치됨 -> HTTPS 가로채기 즉시 가능
```

**방법 B: FoxyProxy 확장 (Firefox)**

```
1. Firefox에 FoxyProxy 확장 설치
2. FoxyProxy 설정:
   - Title: Burp Suite
   - Type: HTTP
   - Hostname: 127.0.0.1
   - Port: 8080
3. FoxyProxy 아이콘 > "Burp Suite" 선택
```

**방법 C: 시스템 전체 프록시**

```bash
# Linux 환경변수 설정
export http_proxy=http://127.0.0.1:8080
export https_proxy=http://127.0.0.1:8080
```

#### 3단계: CA 인증서 설치 (HTTPS 가로채기용)

```
1. 브라우저에서 http://burpsuite 또는 http://127.0.0.1:8080 접속
2. "CA Certificate" 클릭하여 cacert.der 다운로드
3. 브라우저에 인증서 등록:
   - Firefox: Settings > Privacy & Security > Certificates > Import
   - Chrome: Settings > Privacy > Security > Manage certificates > Import
4. "Trust this CA to identify websites" 체크
```

#### 4단계: Intercept 사용

```
Proxy > Intercept 탭

[Intercept is on]  - 요청을 가로채어 수정 가능
[Intercept is off] - 요청을 자동 통과 (History에는 기록됨)

가로챈 요청에 대한 액션:
- Forward     : 요청을 서버로 전달
- Drop        : 요청을 버림
- Action      : Repeater/Intruder 등으로 전송
```

### 해설: 왜 프록시가 필요한가

- 브라우저와 서버 사이의 **모든 HTTP/HTTPS 통신**을 볼 수 있음
- 자바스크립트가 전송하는 숨겨진 요청도 확인 가능
- 요청/응답을 **실시간으로 수정** 가능
- 클라이언트 측 검증을 **완전히 무력화** 가능

### 실습 포인트

- Intercept를 끈 상태로 먼저 사이트를 탐색 -> HTTP History에서 전체 트래픽 파악
- 그 후 의심스러운 요청만 Repeater로 보내서 수동 테스트

---

## Target 분석

### 답지: Site Map 활용

```
Target 탭 > Site map

구조:
target.com
├── /                        # 메인 페이지
├── /api/                    # API 엔드포인트
│   ├── /api/users           # 사용자 관련
│   ├── /api/orders          # 주문 관련
│   └── /api/admin           # 관리자 기능 (중요!)
├── /login                   # 인증 페이지
├── /static/                 # 정적 파일
└── /uploads/                # 업로드 디렉토리
```

### Scope 설정 (중요!)

```
Target > Scope settings

Include in scope:
  Protocol: Any
  Host: target.com
  Port: Any
  File: ^/.*

Exclude from scope:
  *.google.com
  *.googleapis.com
  *.facebook.com

# 장점:
# 1. 불필요한 트래픽 필터링
# 2. Intruder/Scanner가 스코프 내만 테스트
# 3. HTTP History에서 스코프 외 요청 숨기기
```

### 해설: 왜 Target 분석이 중요한가

- 공격 표면(Attack Surface)을 먼저 파악해야 효율적인 테스트 가능
- API 엔드포인트, 파라미터, 인증 메커니즘을 미리 이해
- 스코프를 설정해야 테스트 대상 외의 사이트를 공격하지 않음 (법적 보호)

---

## Repeater 사용법

> 가장 많이 사용하는 도구. 요청을 수동으로 수정하고 반복 전송.

### 답지: 기본 사용법

#### 요청을 Repeater로 보내기

```
1. HTTP History에서 요청 우클릭 > "Send to Repeater" (Ctrl+R)
2. 또는 Intercept에서 Action > Send to Repeater
```

#### Repeater 인터페이스

```
┌─────────────────────────────┬─────────────────────────────┐
│         Request              │          Response            │
│                              │                              │
│ POST /api/login HTTP/1.1     │ HTTP/1.1 200 OK              │
│ Host: target.com             │ Content-Type: application/json│
│ Content-Type: application/   │                              │
│   json                       │ {"status": "success",        │
│                              │  "token": "eyJhbG..."}       │
│ {"username": "admin",        │                              │
│  "password": "test123"}      │                              │
│                              │                              │
│ [Send]                       │                              │
└─────────────────────────────┴─────────────────────────────┘
```

#### 핵심 조작법

```
# 1. 파라미터 수정
원래: {"username": "admin", "password": "test123"}
수정: {"username": "admin' OR 1=1--", "password": "anything"}
-> [Send] 클릭하여 응답 확인

# 2. HTTP 메서드 변경
원래: POST /api/users/delete
수정: GET /api/users/delete
-> 메서드 검증 우회 시도

# 3. 헤더 추가/수정
원래: Cookie: session=my_session
수정: Cookie: session=victim_session
-> 세션 하이재킹 시도

# 4. Content-Type 변경
원래: Content-Type: application/json
수정: Content-Type: application/xml
-> 파서 차이를 이용한 공격

# 5. 인코딩 조작
선택 후 우클릭 > Convert selection
- URL encode
- URL decode
- HTML encode
- Base64 encode/decode
- Hex encode
```

#### 2025 신기능: Custom Actions

```
Repeater 탭에서 우클릭 > Custom actions

기능:
- 요청/응답을 자동으로 수정하고 재전송
- 디코딩/인코딩을 메시지 에디터에서 직접 수행
- 응답에 주석을 추가하여 빠른 비교 분석
- 탭에 메모 설정 가능 (테스트 기록용)
```

### 해설: 왜 Repeater가 핵심인가

- **수동 테스트의 핵심 도구**: 하나의 요청을 정밀하게 조작
- 자동 스캐너가 놓치는 **로직 취약점** 발견 가능
- 요청-응답 쌍을 나란히 비교하며 **차이 분석** 가능
- 멀티탭으로 여러 요청을 동시에 테스트

### 실습 포인트

1. 로그인 요청을 Repeater로 보내서 SQLi 페이로드 수동 테스트
2. API 엔드포인트의 ID 값을 변경하며 IDOR 확인
3. 응답의 HTTP 상태 코드와 본문 차이를 비교하여 블라인드 취약점 탐지

---

## Intruder 공격 설정

> 파라미터에 대한 자동화된 대량 요청 전송. 퍼징, 브루트포스, 열거 등에 사용.

### 답지: Intruder 설정 단계

#### 1단계: 요청을 Intruder로 보내기

```
HTTP History/Repeater에서 우클릭 > "Send to Intruder" (Ctrl+I)
```

#### 2단계: Positions 설정 (공격 위치 지정)

```
POST /api/login HTTP/1.1
Host: target.com
Content-Type: application/json

{"username": "admin", "password": "SS test123 SS"}
                                   ^^          ^^
                              payload marker (SS 기호)

# 자동 설정: "Auto SS" 버튼 (너무 많이 잡힘)
# 수동 설정: 공격할 부분만 선택 > "Add SS" 버튼
# 클리어: "Clear SS" 로 모든 마커 제거 후 필요한 것만 추가
```

#### 3단계: Attack Type 선택

```
1. Sniper (스나이퍼) - 기본값
   - 하나의 페이로드 세트를 각 위치에 순차 삽입
   - 용도: 단일 파라미터 퍼징
   - 예: position 1에 payload 1,2,3 -> position 2에 payload 1,2,3

2. Battering Ram (공성추)
   - 같은 페이로드를 모든 위치에 동시 삽입
   - 용도: 동일한 값이 여러 곳에 필요할 때
   - 예: username=PAYLOAD&confirm_username=PAYLOAD

3. Pitchfork (쇠스랑)
   - 여러 페이로드 세트를 각 위치에 병렬로 삽입
   - 용도: username:password 쌍 테스트 (Credential Stuffing)
   - 예: position 1에 user1, position 2에 pass1 (동시)
         position 1에 user2, position 2에 pass2 (동시)

4. Cluster Bomb (집속탄)
   - 모든 페이로드 조합을 테스트
   - 용도: 모든 username x 모든 password 조합
   - 예: 3개 username x 100개 password = 300 요청
   - 주의: 조합이 기하급수적으로 증가 가능
```

#### 4단계: Payloads 설정

```
Payload Sets:
  Payload set: 1 (position 1에 해당)
  Payload type: [선택]

주요 Payload Types:
┌─────────────────────┬─────────────────────────────────────┐
│ Simple list          │ 직접 입력하거나 파일에서 로드        │
│ Numbers              │ 숫자 범위 (From: 1, To: 1000,       │
│                      │  Step: 1)                           │
│ Brute forcer         │ 문자 집합으로 모든 조합 생성         │
│ Runtime file         │ 대용량 파일을 메모리에 올리지 않고    │
│                      │ 한 줄씩 읽음                        │
│ Dates                │ 날짜 범위 생성                       │
│ Null payloads        │ 빈 페이로드 N번 반복 (Race condition)│
│ Character frobber    │ 한 문자씩 변경하여 차이 관찰         │
└─────────────────────┴─────────────────────────────────────┘

Payload Processing (전처리):
- Add prefix/suffix: 페이로드 앞뒤에 문자열 추가
- Encode: URL encode, Base64 encode, Hash (MD5, SHA)
- Match/Replace: 특정 문자열 치환
```

#### 5단계: Settings (결과 분석 설정)

```
Grep - Match:
  # 응답에서 특정 문자열 검색
  "Invalid credentials"    # 실패 표시
  "Welcome"                # 성공 표시
  "error"                  # 에러 표시

Grep - Extract:
  # 응답에서 특정 패턴 추출
  시작: "token":"
  끝:   "
  # 각 응답에서 토큰 값을 자동 추출

Redirections:
  Follow redirections: Always / Never / On-site only
```

### 실전 공격 예시

#### 예시 1: 로그인 브루트포스

```
Target: POST /login
Positions:
  {"username": "admin", "password": "SS FUZZ SS"}

Attack Type: Sniper
Payload: /usr/share/wordlists/rockyou.txt (상위 10000개)

Settings:
  Grep - Match: "Welcome" (성공), "Invalid" (실패)

결과 분석:
  Status Code 다름 -> 200 vs 302 (리다이렉트 = 성공)
  Length 다름 -> 성공 응답은 길이가 다름
  Grep Match -> "Welcome" 체크된 것 = 성공
```

#### 예시 2: IDOR 열거

```
Target: GET /api/users/SS 1 SS/profile
Attack Type: Sniper
Payload Type: Numbers (From: 1, To: 10000, Step: 1)

결과 분석:
  200 OK -> 접근 가능한 프로필
  403 Forbidden -> 존재하지만 접근 불가
  404 Not Found -> 존재하지 않음
```

#### 예시 3: 디렉토리 퍼징

```
Target: GET /SS FUZZ SS HTTP/1.1
Attack Type: Sniper
Payload: /usr/share/wordlists/dirb/common.txt

결과 분석:
  200 -> 존재하는 페이지
  301/302 -> 리다이렉트 (디렉토리일 가능성)
  403 -> 존재하지만 접근 거부
```

#### 예시 4: Race Condition (Null Payloads)

```
Target: POST /api/apply-coupon
Positions: (페이로드 마커 없이 전체 요청)
Attack Type: Sniper
Payload Type: Null payloads (Generate: 100)

Settings:
  Number of threads: 25 (동시 요청)
  # 쿠폰이 여러 번 적용되는지 확인

# 2023.9+ 버전에서는 Send group in parallel 기능 사용 가능
# Repeater에서 여러 탭 선택 > "Send group (parallel)"
```

### 해설: 왜 Intruder가 강력한가

- **수동으로 수천 번 요청하는 것을 자동화**
- 응답의 미세한 차이(길이, 상태 코드, 특정 문자열)를 체계적으로 비교
- Community Edition에서도 사용 가능 (속도 제한 있음)
- Pro 버전의 "Turbo Intruder" 확장은 초당 수만 요청 가능

### 실습 포인트

- 먼저 Repeater에서 수동으로 취약점 존재 여부를 확인한 후, Intruder로 자동화
- Attack Type 선택이 핵심: 단일 파라미터는 Sniper, 자격증명 쌍은 Pitchfork
- 결과 분석 시 **Length** 정렬이 가장 유용 (비정상 응답은 길이가 다름)

---

## Scanner (Pro)

### 답지: 자동 스캐닝

```
방법 1: 능동 스캔
Target > Site map > 대상 우클릭 > "Actively scan this host"

방법 2: 수동 스캔 (Crawl Only)
Dashboard > New scan > "Crawl only" 선택

방법 3: 특정 요청만 스캔
HTTP History에서 우클릭 > "Scan selected items"

스캔 설정:
  Crawl:
    - Maximum crawl depth: 5-10
    - Maximum unique locations: 1000
  Audit:
    - Issue types: 전체 또는 특정 취약점만 선택
    - Insertion points: URL parameters, body parameters, cookies, headers
```

### 해설: Scanner의 한계

- **로직 취약점은 탐지 불가** (IDOR, 비즈니스 로직 결함)
- False Positive 발생 가능 -> 반드시 수동 검증 필요
- 과도한 스캔은 서버에 부하를 줄 수 있음
- Community Edition에서는 사용 불가

---

## 유용한 확장 프로그램

### BApp Store에서 설치 (Extensions > BApp Store)

```
필수 확장:
┌──────────────────────┬──────────────────────────────────────┐
│ Autorize              │ 자동 권한 테스트 (IDOR/BAC 탐지)     │
│ Logger++              │ 향상된 로깅 + 필터링                  │
│ Param Miner           │ 숨겨진 파라미터/헤더 발견             │
│ Turbo Intruder        │ 초고속 요청 전송 (Python 스크립트)    │
│ JSON Web Tokens       │ JWT 디코딩/편집                      │
│ Active Scan++         │ 추가 스캔 검사 항목                   │
│ Backslash Powered     │ 고급 서버 사이드 인젝션 탐지          │
│   Scanner             │                                      │
│ Hackvertor            │ 태그 기반 인코딩/변환                 │
│ InQL                  │ GraphQL 취약점 스캐닝                 │
│ HTTP Request          │ Request Smuggling 탐지                │
│   Smuggler            │                                      │
└──────────────────────┴──────────────────────────────────────┘
```

### Autorize 사용법 (IDOR/BAC 자동 탐지)

```
1. 저권한 사용자의 쿠키/토큰 복사
2. Autorize 탭 > "Cookie" 필드에 저권한 세션 값 붙여넣기
3. "Intercept Filters" 설정 (스코프 내 요청만)
4. "Autorize is ON" 활성화
5. 고권한 사용자로 사이트 브라우징

원리:
- 고권한 요청을 감지 -> 저권한 세션으로 동일 요청 자동 전송
- 응답 비교:
  - 동일 = Bypassed! (권한 검사 없음)
  - 다름 = Enforced (정상)
```

---

## 실전 워크플로우

### 전체 테스트 흐름

```
┌─────────────────────────────────────────────────────────┐
│  Phase 1: 정찰 (Reconnaissance)                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │ 1. Intercept OFF 상태로 타겟 사이트 전체 탐색      │  │
│  │ 2. 모든 기능 사용 (로그인, 검색, 프로필, 설정 등)  │  │
│  │ 3. Target > Site map에서 구조 파악                  │  │
│  │ 4. Scope 설정                                      │  │
│  └───────────────────────────────────────────────────┘  │
│                         ▼                                │
│  Phase 2: 분석 (Analysis)                               │
│  ┌───────────────────────────────────────────────────┐  │
│  │ 1. HTTP History에서 흥미로운 요청 식별              │  │
│  │    - 파라미터가 있는 요청                           │  │
│  │    - API 엔드포인트                                 │  │
│  │    - 파일 업로드/다운로드                           │  │
│  │    - 인증/인가 관련 요청                            │  │
│  │ 2. 각 요청을 Repeater로 전송 (Ctrl+R)              │  │
│  │ 3. Param Miner로 숨겨진 파라미터 탐색              │  │
│  └───────────────────────────────────────────────────┘  │
│                         ▼                                │
│  Phase 3: 수동 테스트 (Manual Testing)                  │
│  ┌───────────────────────────────────────────────────┐  │
│  │ Repeater에서 각 취약점 유형별 수동 테스트:          │  │
│  │                                                    │  │
│  │ [SQLi 테스트]                                      │  │
│  │   ' -> 에러 확인                                   │  │
│  │   ' OR 1=1-- -> 인증 우회 확인                     │  │
│  │   ' UNION SELECT NULL-- -> 컬럼 수 확인            │  │
│  │                                                    │  │
│  │ [XSS 테스트]                                       │  │
│  │   <script>alert(1)</script> -> 반사 확인            │  │
│  │   "onmouseover="alert(1) -> 속성 삽입 확인         │  │
│  │                                                    │  │
│  │ [IDOR 테스트]                                      │  │
│  │   ID 값 변경하여 다른 사용자 데이터 접근 확인       │  │
│  │   Autorize로 자동 검증                              │  │
│  │                                                    │  │
│  │ [SSRF 테스트]                                      │  │
│  │   URL 파라미터에 내부 주소 삽입                     │  │
│  │   http://127.0.0.1, http://169.254.169.254         │  │
│  └───────────────────────────────────────────────────┘  │
│                         ▼                                │
│  Phase 4: 자동화 공격 (Automated Attacks)               │
│  ┌───────────────────────────────────────────────────┐  │
│  │ 확인된 취약점에 대해 Intruder로 자동화:             │  │
│  │                                                    │  │
│  │ - 브루트포스 공격 (로그인, 2FA 코드)               │  │
│  │ - IDOR 열거 (사용자 ID 범위 스캔)                  │  │
│  │ - 퍼징 (다양한 페이로드로 입력 테스트)              │  │
│  │ - 디렉토리 열거                                    │  │
│  │                                                    │  │
│  │ Pro: Scanner로 추가 취약점 자동 탐지               │  │
│  └───────────────────────────────────────────────────┘  │
│                         ▼                                │
│  Phase 5: 보고 (Reporting)                              │
│  ┌───────────────────────────────────────────────────┐  │
│  │ 1. 발견된 취약점 정리                               │  │
│  │ 2. 재현 단계 (요청/응답 캡처 포함)                  │  │
│  │ 3. 영향도 분석                                     │  │
│  │ 4. 수정 권고안                                     │  │
│  │                                                    │  │
│  │ Pro: Target > Issues에서 자동 보고서 생성          │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 취약점별 Burp 워크플로우 요약

#### SQL Injection 발견 워크플로우

```
1. HTTP History에서 파라미터가 있는 요청 찾기
   (검색, 필터, 정렬, 사용자 조회 등)

2. Repeater로 전송

3. 기본 테스트:
   원본: id=1
   테스트: id=1'            -> SQL 에러 확인
          id=1 AND 1=1     -> 정상 응답 (True)
          id=1 AND 1=2     -> 비정상 응답 (False)
          -> 차이 있으면 SQLi 존재!

4. 유형 확인:
   - 에러가 보이면 -> Error-based
   - 응답 차이만 있으면 -> Boolean-blind
   - 아무 차이 없으면 -> id=1 AND SLEEP(5) 로 Time-based 확인

5. sqlmap으로 자동화:
   Repeater에서 요청 복사 > 파일 저장 > sqlmap -r request.txt
```

#### XSS 발견 워크플로우

```
1. 입력값이 응답에 반영되는 곳 찾기
   (검색 결과, 프로필 이름, 댓글 등)

2. Repeater로 전송

3. 반영 위치 파악:
   입력: UNIQUESTRING12345
   응답에서 검색: 어디에 어떤 컨텍스트로 반영되는지 확인
   - HTML 본문: <p>UNIQUESTRING12345</p>
   - HTML 속성: <input value="UNIQUESTRING12345">
   - JavaScript: var x = "UNIQUESTRING12345";
   - URL: <a href="UNIQUESTRING12345">

4. 컨텍스트에 맞는 페이로드:
   - HTML 본문: <script>alert(1)</script>
   - HTML 속성: " onmouseover="alert(1)
   - JavaScript: ";alert(1)//
   - URL: javascript:alert(1)

5. 필터링 확인 및 우회:
   <script> 차단됨? -> <img src=x onerror=alert(1)>
   alert 차단됨? -> confirm(1) 또는 prompt(1)
   괄호 차단됨? -> alert`1`
```

### 단축키 모음

```
Ctrl+R          Repeater로 전송
Ctrl+I          Intruder로 전송
Ctrl+Shift+T    새 Repeater 탭
Ctrl+U          URL 인코딩
Ctrl+Shift+U    URL 디코딩
Ctrl+B          Base64 인코딩
Ctrl+Shift+B    Base64 디코딩
Ctrl+H          HTML 인코딩
Tab             Intercept에서 Forward
Ctrl+F          응답에서 검색
```

---

## 참고 자료

- [Burp Suite 공식 문서](https://portswigger.net/burp/documentation)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [Burp Suite 2025 릴리스 노트](https://portswigger.net/burp/releases)
- [Burp Suite Comprehensive Guide 2025](https://www.shadecoder.com/topics/burp-suite-a-comprehensive-guide-for-2025)
- [Burp Suite Pro Tips 2025](https://www.onlinehashcrack.com/guides/security-tools/burp-suite-pro-tips-2025-supercharge-testing.php)
