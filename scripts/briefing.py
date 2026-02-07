#!/usr/bin/env python3
"""최신 브리핑 파일 표시 또는 모든 벤치마크의 현재 상태 요약 생성.

Usage:
    python3 scripts/briefing.py          # 최신 브리핑 표시
    python3 scripts/briefing.py summary  # 전체 현황 요약 생성
"""

import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
BENCHMARKS_DIR = BASE_DIR / "benchmarks"
BRIEFINGS_DIR = BASE_DIR / "briefings"


def show_latest_briefing() -> None:
    """가장 최근 브리핑 파일 출력."""
    briefings = sorted(BRIEFINGS_DIR.glob("briefing-*.md"), reverse=True)
    if not briefings:
        print("아직 브리핑이 없습니다. 먼저 monitor.py를 실행하세요.")
        return

    latest = briefings[0]
    print(latest.read_text(encoding="utf-8"))


def generate_summary() -> None:
    """전체 벤치마크 현황 요약."""
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [
        f"# LLM Security Benchmark 전체 현황",
        f"**생성일**: {today}",
        "",
        "## 수집된 데이터 통계",
        "",
    ]

    total_files = 0
    for source_dir in sorted(BENCHMARKS_DIR.iterdir()):
        if source_dir.is_dir():
            md_files = list(source_dir.glob("*.md"))
            total_files += len(md_files)
            lines.append(f"### {source_dir.name}")
            lines.append(f"- 파일 수: {len(md_files)}")
            for f in sorted(md_files):
                lines.append(f"  - `{f.name}`")
            lines.append("")

    lines.insert(4, f"**총 파일 수**: {total_files}")
    lines.insert(5, "")

    summary_file = BRIEFINGS_DIR / f"summary-{today}.md"
    summary_file.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"\n--- 저장됨: {summary_file}")


def main():
    BRIEFINGS_DIR.mkdir(parents=True, exist_ok=True)

    if len(sys.argv) > 1 and sys.argv[1] == "summary":
        generate_summary()
    else:
        show_latest_briefing()


if __name__ == "__main__":
    main()
