# AI Security Benchmark Hub

## 프로젝트 개요
LLM 보안 벤치마크 6개 소스의 데이터 수집, 모니터링, 브리핑 자동화 시스템.
화이트해커 핵심 리소스 90개 포함.

## 구조
- `benchmarks/` - 6개 벤치마크 소스 데이터 (스크래핑 결과)
- `resources/` - 보안 리소스 (AI보안, 일반보안, 레드팀, 블루팀, 학습, 뉴스)
- `scripts/` - 모니터링/업데이트/브리핑 스크립트
- `briefings/` - 일일 브리핑 파일
- `logs/` - 모니터링 로그

## 명령어
```bash
# 모니터링 (변경 감지)
python3 scripts/monitor.py

# 소스 업데이트
python3 scripts/update_source.py <source_name|all>

# 브리핑 확인
python3 scripts/briefing.py
python3 scripts/briefing.py summary

# cron 설정
bash scripts/setup_cron.sh
```

## 벤치마크 소스
1. JailbreakBench (학술) - jailbreakbench/
2. 0DIN (실전) - 0din/ (14개 포스트)
3. CalypsoAI (상세) - calypsoai/
4. Enkrypt AI (간결) - enkryptai/
5. Phare (다국어) - phare/
6. General Analysis (공격기법별) - general-analysis/

## 코딩 컨벤션
- Python 3.10+, PEP 8
- Type hints 사용
- pathlib 우선
- 한국어 주석/문서, 영어 코드
