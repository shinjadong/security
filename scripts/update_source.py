#!/usr/bin/env python3
"""변경 감지된 소스의 최신 데이터를 다운로드.

Usage:
    python3 scripts/update_source.py <source_name>
    python3 scripts/update_source.py all
    python3 scripts/update_source.py 0din
"""

import sys
import json
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent.parent
BENCHMARKS_DIR = BASE_DIR / "benchmarks"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 14) LLM-Security-Monitor/1.0"
}

SOURCES = {
    "0din": {
        "url": "https://0din.ai/blog/",
        "dir": "0din",
    },
    "calypsoai": {
        "url": "https://calypsoai.com/calypsoai-model-leaderboard/",
        "dir": "calypsoai",
    },
    "enkryptai": {
        "url": "https://leaderboard.enkryptai.com/",
        "dir": "enkryptai",
    },
    "phare": {
        "url": "https://phare.giskard.ai/",
        "dir": "phare",
    },
    "general_analysis": {
        "url": "https://www.generalanalysis.com/benchmarks",
        "dir": "general-analysis",
    },
    "jailbreakbench": {
        "url": "https://jailbreakbench.github.io/",
        "dir": "jailbreakbench",
    },
}


def fetch_and_save_raw(name: str, config: dict) -> None:
    """소스 페이지를 가져와서 raw HTML + 텍스트로 저장."""
    url = config["url"]
    target_dir = BENCHMARKS_DIR / config["dir"]
    target_dir.mkdir(parents=True, exist_ok=True)

    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"  [ERROR] {url} 접근 실패: {e}")
        return

    # Raw HTML 저장
    today = datetime.now().strftime("%Y-%m-%d")
    raw_file = target_dir / f"raw-{today}.html"
    raw_file.write_text(resp.text, encoding="utf-8")
    print(f"  Raw HTML saved: {raw_file}")

    # 텍스트 추출
    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator="\n", strip=True)

    text_file = target_dir / f"snapshot-{today}.txt"
    text_file.write_text(text, encoding="utf-8")
    print(f"  Text snapshot saved: {text_file}")


def update_source(name: str) -> None:
    if name not in SOURCES:
        print(f"Unknown source: {name}")
        print(f"Available: {', '.join(SOURCES.keys())}")
        sys.exit(1)

    config = SOURCES[name]
    print(f"\n[{name}] Updating from {config['url']}...")
    fetch_and_save_raw(name, config)
    print(f"[{name}] Done!")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 update_source.py <source_name|all>")
        print(f"Available sources: {', '.join(SOURCES.keys())}")
        sys.exit(1)

    target = sys.argv[1]

    if target == "all":
        for name in SOURCES:
            update_source(name)
    else:
        update_source(target)


if __name__ == "__main__":
    main()
