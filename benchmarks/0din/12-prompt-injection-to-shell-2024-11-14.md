# Prompt Injection to Shell: OpenAI ChatGPT 컨테이너 환경

- **URL**: https://0din.ai/blog/prompt-injecting-your-way-to-shell-openai-s-containerized-chatgpt-environment
- **저자**: Marco Figueroa
- **날짜**: 2024-11-14
- **수집일**: 2026-02-08

## 핵심 발견

ChatGPT의 Debian 기반 컨테이너에서 파일 관리, 코드 실행, 지시 추출이 가능.
이것은 의도된 설계이며 보안 취약점이 아님.

## 주요 발견 사항

### 파일 시스템 탐색
- `list files /`로 전체 디렉토리 구조 노출
- `/home/sandbox/.openai_internal/` 내부 설정 파일
- Debian Bookworm 기반 + 커스텀 설정

### 파일 관리
1. `/mnt/data/`에 파일 업로드
2. 업로드된 Python 스크립트 실행
3. 컨테이너 내 파일 이동 (`shutil.move`)
4. 디렉토리 리스팅으로 확인

### 중요 발견: 크로스 유저 파일 공유
공유 프롬프트로 다른 사용자가 디렉토리 파일 접근 가능

### GPT 지시/지식 추출
- 시스템 지시, 설정, 행동 가이드라인 추출 가능
- 압축 아카이브로 다운로드 가능

## 버그 vs 기능

OpenAI의 입장: 대부분 샌드박스 상호작용은 **의도된 기능**.
- 코드 실행 = 데이터 분석용 정당 기능
- 모든 활동이 샌드박스 내 격리
- `uname -a`, `whoami`, `ps`로 경계 확인 가능

### 진짜 취약점 = 샌드박스 탈출
- 샌드박스 외부 코드 실행
- 호스트 시스템 파일 접근
- 보호된 커널 데이터 읽기
- 무단 권한 코드 실행
