# Phase 0: 기초 체력 - 퀵스타트 가이드

> **원칙**: 이론서 읽지 말고, 바로 실습 → 막히면 그때 개념 역추적

---

## Day 1-3: 리눅스

### 답지: OverTheWire Bandit
```bash
# 접속
ssh bandit0@bandit.labs.overthewire.org -p 2220
# password: bandit0
```

### 레벨별 핵심 개념 (막힐 때만 보기)

| Level | 핵심 명령어 | 배우는 것 |
|-------|-----------|----------|
| 0→1 | `cat readme` | 파일 읽기 |
| 1→2 | `cat ./-` | 특수 파일명 처리 |
| 2→3 | `cat "spaces in name"` | 공백 처리 |
| 3→4 | `ls -la` | 숨김 파일 |
| 4→5 | `file ./*` | 파일 타입 식별 |
| 5→6 | `find / -user bandit7 -size 33c` | find 검색 |
| 6→7 | `grep millionth data.txt` | 텍스트 검색 |
| 7→8 | `sort data.txt \| uniq -u` | 파이프라인 |
| 8→9 | `strings data.txt` | 바이너리에서 텍스트 추출 |
| 9→10 | `base64 -d data.txt` | 인코딩/디코딩 |
| 10→11 | `tr 'A-Za-z' 'N-ZA-Mn-za-m'` | ROT13 |
| 11→12 | `xxd -r data.txt` | hex dump |
| 12→13 | gzip/bzip2/tar | 압축 해제 체인 |
| 13→14 | `ssh -i sshkey` | SSH 키 인증 |
| 14→15 | `openssl s_client` | SSL/TLS 통신 |

**왜 이게 중요한가?**
→ 보안 작업의 80%는 리눅스 CLI에서 이루어짐. Bandit은 실전 필수 명령어를 자연스럽게 습득하게 해줌.

---

## Day 4-5: 네트워크

### 답지: 바로 패킷 분석
```bash
# Termux에서 사용 가능한 도구
pkg install nmap
pkg install tcpdump

# 기본 스캔 (자신의 네트워크만)
nmap -sV 192.168.1.0/24

# 패킷 캡처
tcpdump -i wlan0 -w capture.pcap
```

### 알아야 할 최소 개념 (이것만)

```
Layer 4 (Transport): TCP/UDP
  ├─ TCP: 3-way handshake (SYN → SYN-ACK → ACK)
  ├─ 포트: 80(HTTP), 443(HTTPS), 22(SSH), 3306(MySQL)
  └─ UDP: DNS(53), DHCP(67/68)

Layer 3 (Network): IP
  ├─ IPv4 주소 구조: 192.168.1.100/24
  ├─ 서브넷: /24 = 255.255.255.0 = 254 호스트
  └─ 라우팅: 패킷이 어디로 가는가

Layer 2 (Data Link): MAC
  └─ ARP: IP → MAC 변환 (ARP spoofing의 기반)

Layer 1 (Physical): 와이어/무선
```

**왜 이게 중요한가?**
→ 모든 해킹은 결국 네트워크를 통해 이루어짐. TCP/IP 4계층만 이해하면 90%의 네트워크 공격 이해 가능.

---

## Day 6-7: Python

### 답지: 보안용 Python 스크립트 복붙 → 수정

```python
# 1. 포트 스캐너 (소켓 기초)
import socket

def scan_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0

# 사용: scan_port("192.168.1.1", 80)
```

```python
# 2. HTTP 요청 (requests 기초)
import requests

# GET 요청
r = requests.get("https://httpbin.org/get")
print(r.status_code, r.json())

# POST 요청 (로그인 시뮬레이션)
data = {"username": "admin", "password": "test"}
r = requests.post("https://httpbin.org/post", data=data)
print(r.json())
```

```python
# 3. 웹 스크래핑 (BeautifulSoup 기초)
from bs4 import BeautifulSoup
import requests

r = requests.get("https://example.com")
soup = BeautifulSoup(r.text, "html.parser")
links = [a["href"] for a in soup.find_all("a", href=True)]
print(links)
```

### Python 문법 역추적 가이드
| 막히는 것 | 검색 키워드 |
|----------|-----------|
| 리스트 다루기 | "python list comprehension" |
| 파일 읽기/쓰기 | "python pathlib read write" |
| HTTP 요청 | "python requests library" |
| 정규식 | "python re module" |
| 인코딩 | "python base64 hex encode decode" |
| 에러 처리 | "python try except" |

**왜 Python인가?**
→ 보안 도구의 80%가 Python (Metasploit은 Ruby지만). exploit-db, HackTheBox writeup 모두 Python 기반.

---

## 체크리스트

- [ ] Bandit Level 0→15 클리어
- [ ] nmap으로 자신의 네트워크 스캔
- [ ] 포트 스캐너 스크립트 직접 실행
- [ ] HTTP 요청 스크립트로 API 호출 성공
- [ ] base64/hex 인코딩-디코딩 Python으로 실행

**이것들을 할 수 있으면 Phase 1로 진행!**
