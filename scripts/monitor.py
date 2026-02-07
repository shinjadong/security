#!/usr/bin/env python3
"""LLM Security Benchmark Monitor

각 벤치마크 사이트의 새 콘텐츠를 감지하고 변경사항을 로깅.
cron으로 매일 실행: 0 8 * * * cd ~/projects/ai-security && python3 scripts/monitor.py
"""

import hashlib
import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent.parent
BENCHMARKS_DIR = BASE_DIR / "benchmarks"
BRIEFINGS_DIR = BASE_DIR / "briefings"
LOGS_DIR = BASE_DIR / "logs"
STATE_FILE = BASE_DIR / "scripts" / ".monitor_state.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOGS_DIR / "monitor.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 14) LLM-Security-Monitor/1.0"
}

# 각 소스별 모니터링 설정
SOURCES = {
    "0din": {
        "url": "https://0din.ai/blog/",
        "type": "blog_list",
        "dir": "0din",
        "selector": "article, .blog-post, a[href*='/blog/']",
    },
    "calypsoai": {
        "url": "https://calypsoai.com/calypsoai-model-leaderboard/",
        "type": "page_hash",
        "dir": "calypsoai",
    },
    "enkryptai": {
        "url": "https://leaderboard.enkryptai.com/",
        "type": "page_hash",
        "dir": "enkryptai",
    },
    "phare": {
        "url": "https://phare.giskard.ai/",
        "type": "page_hash",
        "dir": "phare",
    },
    "general_analysis": {
        "url": "https://www.generalanalysis.com/benchmarks",
        "type": "page_hash",
        "dir": "general-analysis",
    },
    "jailbreakbench": {
        "url": "https://jailbreakbench.github.io/",
        "type": "page_hash",
        "dir": "jailbreakbench",
    },
}


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False))


def fetch_page(url: str) -> Optional[str]:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as e:
        log.error(f"Failed to fetch {url}: {e}")
        return None


def content_hash(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    # script, style 태그 제거하여 실제 콘텐츠만 해시
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator=" ", strip=True)
    return hashlib.sha256(text.encode()).hexdigest()


def extract_blog_links(html: str, base_url: str) -> list[dict]:
    """0DIN 블로그 포스트 링크 추출."""
    soup = BeautifulSoup(html, "html.parser")
    posts = []
    seen = set()

    for link in soup.find_all("a", href=True):
        href = link["href"]
        if "/blog/" in href and href not in ("/blog/", "/blog/articles"):
            # 상대 경로 처리
            if href.startswith("/"):
                full_url = f"https://0din.ai{href}"
            else:
                full_url = href

            slug = href.rstrip("/").split("/")[-1]
            if slug and slug not in seen and "page=" not in slug:
                seen.add(slug)
                title = link.get_text(strip=True) or slug
                posts.append({"url": full_url, "slug": slug, "title": title})

    return posts


def check_source(name: str, config: dict, state: dict) -> list[str]:
    """소스 확인하고 변경사항 반환."""
    changes = []
    url = config["url"]

    html = fetch_page(url)
    if not html:
        return [f"[{name}] 페이지 접근 실패"]

    if config["type"] == "page_hash":
        new_hash = content_hash(html)
        old_hash = state.get(name, {}).get("hash", "")

        if old_hash and new_hash != old_hash:
            changes.append(f"[{name}] 콘텐츠 변경 감지! 새 데이터 확인 필요")
            log.info(f"{name}: content changed (hash {old_hash[:8]}→{new_hash[:8]})")
        elif not old_hash:
            log.info(f"{name}: initial hash recorded")

        state[name] = {
            "hash": new_hash,
            "last_checked": datetime.now().isoformat(),
        }

    elif config["type"] == "blog_list":
        posts = extract_blog_links(html, url)
        known_slugs = set(state.get(name, {}).get("known_slugs", []))
        new_posts = [p for p in posts if p["slug"] not in known_slugs]

        if new_posts:
            for p in new_posts:
                changes.append(f"[{name}] 새 포스트: {p['title']} ({p['url']})")
            log.info(f"{name}: {len(new_posts)} new posts found")

        all_slugs = list(known_slugs | {p["slug"] for p in posts})
        state[name] = {
            "known_slugs": all_slugs,
            "last_checked": datetime.now().isoformat(),
            "total_posts": len(all_slugs),
        }

    return changes


def generate_briefing(all_changes: list[str]) -> Path:
    """데일리 브리핑 마크다운 파일 생성."""
    today = datetime.now().strftime("%Y-%m-%d")
    briefing_file = BRIEFINGS_DIR / f"briefing-{today}.md"

    lines = [
        f"# LLM Security Benchmark Daily Briefing",
        f"**날짜**: {today}",
        f"**생성 시간**: {datetime.now().strftime('%H:%M:%S')}",
        "",
    ]

    if all_changes:
        lines.append(f"## 변경사항 ({len(all_changes)}건)")
        lines.append("")
        for change in all_changes:
            lines.append(f"- {change}")
        lines.append("")
        lines.append("## 액션 필요")
        lines.append("")
        lines.append("변경된 소스를 다시 스크래핑하여 최신 데이터를 업데이트하세요:")
        lines.append("```bash")
        lines.append("cd ~/projects/ai-security")
        lines.append("python3 scripts/update_source.py <source_name>")
        lines.append("```")
    else:
        lines.append("## 상태: 변경 없음")
        lines.append("")
        lines.append("모든 벤치마크 소스가 마지막 확인 시점과 동일합니다.")

    lines.extend([
        "",
        "---",
        "",
        "## 소스 상태 요약",
        "",
        "| 소스 | 마지막 확인 | 상태 |",
        "|------|-----------|------|",
    ])

    state = load_state()
    for name in SOURCES:
        src_state = state.get(name, {})
        last_checked = src_state.get("last_checked", "미확인")
        if last_checked != "미확인":
            last_checked = last_checked[:16].replace("T", " ")
        has_change = any(f"[{name}]" in c for c in all_changes)
        status = "변경 감지" if has_change else "동일"
        lines.append(f"| {name} | {last_checked} | {status} |")

    briefing_file.write_text("\n".join(lines), encoding="utf-8")
    return briefing_file


def main():
    log.info("=== LLM Security Benchmark Monitor 시작 ===")

    BRIEFINGS_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    state = load_state()
    all_changes = []

    for name, config in SOURCES.items():
        log.info(f"Checking {name}...")
        changes = check_source(name, config, state)
        all_changes.extend(changes)

    save_state(state)

    briefing_path = generate_briefing(all_changes)
    log.info(f"Briefing generated: {briefing_path}")

    if all_changes:
        log.info(f"총 {len(all_changes)}건 변경 감지!")
        for c in all_changes:
            log.info(f"  {c}")
    else:
        log.info("변경 없음")

    log.info("=== Monitor 완료 ===")


if __name__ == "__main__":
    main()
