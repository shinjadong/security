#!/bin/bash
# LLM Security Benchmark Monitor - cron 설정 스크립트
# Termux에서 실행: bash scripts/setup_cron.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
PYTHON_PATH=$(which python3)

# cron job: 매일 오전 8시 모니터링 실행
CRON_JOB="0 8 * * * cd ${PROJECT_DIR} && ${PYTHON_PATH} scripts/monitor.py >> logs/cron.log 2>&1"

# 기존 관련 cron job 제거 후 추가
(crontab -l 2>/dev/null | grep -v "monitor.py"; echo "${CRON_JOB}") | crontab -

echo "✓ Cron job 등록 완료"
echo "  시간: 매일 08:00"
echo "  명령: ${CRON_JOB}"
echo ""
echo "확인: crontab -l"
echo "로그: ${PROJECT_DIR}/logs/cron.log"
echo "브리핑: ${PROJECT_DIR}/briefings/"
