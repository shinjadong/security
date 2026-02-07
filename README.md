# Security - LLM Security Benchmark Hub

LLM 보안 벤치마크 6개 소스의 데이터를 수집하고, 변경사항을 자동 모니터링하며, 매일 브리핑을 생성하는 시스템. 화이트해커 핵심 리소스 90개 포함.

## Quick Start

```bash
# 클론
git clone https://github.com/shinjadong/security.git
cd security

# 의존성 설치
pip install -r requirements.txt

# 첫 모니터링 실행 (초기 상태 기록)
python3 scripts/monitor.py

# 브리핑 확인
python3 scripts/briefing.py

# 매일 자동 실행 (cron 등록)
bash scripts/setup_cron.sh
```

## 프로젝트 구조

```
security/
├── benchmarks/              # 6개 벤치마크 소스 데이터
│   ├── 0din/                # 0DIN 실전 버그바운티 (14개 포스트)
│   ├── calypsoai/           # CalypsoAI CASI/AWR 리더보드
│   ├── enkryptai/           # Enkrypt AI NIST/OWASP 점수
│   ├── phare/               # Phare 다국어 안전성 (50개 모델)
│   ├── general-analysis/    # General Analysis 공격기법별
│   ├── jailbreakbench/      # JailbreakBench 학술 표준
│   └── INDEX.md             # 통합 인덱스 + 크로스 벤치마크 비교
├── resources/               # 화이트해커 핵심 리소스 90개
│   ├── ai-security/         # AI 벤치마크 & GitHub 레포
│   ├── general-security/    # 취약점 DB & 인텔리전스
│   ├── redteam/             # 공격 도구 (펜테스트/모바일/네트워크)
│   ├── blueteam/            # 방어 도구 (SIEM/포렌식)
│   ├── learning/            # CTF 플랫폼 & 인증
│   ├── news/                # 보안 뉴스 & 블로그
│   └── INDEX.md             # 리소스 인덱스
├── scripts/                 # 자동화 스크립트
│   ├── monitor.py           # 변경 감지 (매일 cron)
│   ├── update_source.py     # 소스 업데이트
│   ├── briefing.py          # 브리핑 확인/요약
│   └── setup_cron.sh        # cron 등록
├── briefings/               # 일일 브리핑 파일
├── logs/                    # 모니터링 로그
└── requirements.txt
```

## 명령어

```bash
# 모니터링 (변경 감지)
python3 scripts/monitor.py

# 특정 소스 업데이트
python3 scripts/update_source.py 0din
python3 scripts/update_source.py all

# 최신 브리핑 확인
python3 scripts/briefing.py

# 전체 현황 요약
python3 scripts/briefing.py summary

# cron 등록 (매일 08:00)
bash scripts/setup_cron.sh
```

## 벤치마크 소스

| # | 소스 | 유형 | 강점 |
|---|------|------|------|
| 1 | [JailbreakBench](https://jailbreakbench.github.io) | 학술 | NeurIPS 2024 표준, 재현성 |
| 2 | [0DIN](https://0din.ai) | 실전 | Mozilla 버그바운티, 450+ 프로브 |
| 3 | [CalypsoAI](https://calypsoai.com/calypsoai-model-leaderboard) | 상업 | CASI/AWR 점수, 월간 위협 인사이트 |
| 4 | [Enkrypt AI](https://leaderboard.enkryptai.com) | 상업 | NIST/OWASP 점수, 175+ 모델 |
| 5 | [Phare](https://phare.giskard.ai) | 다국어 | 다국어 편향/환각/유해성 평가 |
| 6 | [General Analysis](https://www.generalanalysis.com/benchmarks) | 학술 | TAP/Crescendo/Zero-shot 비교 |

## 요구사항

- Python 3.10+
- `pip install -r requirements.txt`
- cron (선택): 매일 자동 모니터링

## 다른 서버에서 실행

```bash
# 1. 클론
git clone https://github.com/shinjadong/security.git
cd security

# 2. 의존성
pip install -r requirements.txt

# 3. cron 등록
bash scripts/setup_cron.sh

# 4. 첫 실행 (초기 상태 기록)
python3 scripts/monitor.py
```

모니터링 상태는 `scripts/.monitor_state.json`에 저장됩니다.
다른 서버에서 처음 실행하면 현재 상태를 기준으로 새로 기록하고, 이후 변경사항만 감지합니다.

## License

MIT
