#!/usr/bin/env python3
"""
유튜브 마스터 강의 처리 파이프라인
다운로드 → 자막 추출 → 한국어 번역 → 수면용 음성(TTS) 생성

사용법:
    # 1. 단일 영상 처리
    python youtube_pipeline.py "https://youtube.com/watch?v=xxx"

    # 2. 추천 리스트 전체 처리
    python youtube_pipeline.py --playlist recommended

    # 3. 자막만 추출 (다운로드 없이)
    python youtube_pipeline.py "https://youtube.com/watch?v=xxx" --subtitle-only

    # 4. 번역 + TTS만 (이미 자막 있을 때)
    python youtube_pipeline.py --from-srt subtitle.srt

    # 5. 특정 단계만 실행
    python youtube_pipeline.py "URL" --steps download,subtitle,translate,tts

필요 패키지:
    pip install yt-dlp openai-whisper deep-translator gTTS pydub

선택 패키지 (고품질):
    pip install edge-tts  # 마이크로소프트 고품질 TTS (무료)
    pip install faster-whisper  # GPU 가속 whisper
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime


# === 설정 ===

BASE_DIR = Path(__file__).parent.parent / "media"
DOWNLOAD_DIR = BASE_DIR / "downloads"
SUBTITLE_DIR = BASE_DIR / "subtitles"
TRANSLATED_DIR = BASE_DIR / "translated"
AUDIO_DIR = BASE_DIR / "sleep-audio"

# 추천 마스터 강의 리스트
RECOMMENDED = {
    "web-hacking": [
        {
            "title": "Web Security Academy - Full Course",
            "url": "https://www.youtube.com/watch?v=2_lswM1S264",
            "channel": "The Cyber Mentor",
            "duration": "~15h",
            "level": "입문→중급",
        },
        {
            "title": "Bug Bounty Hunting Full Course",
            "url": "https://www.youtube.com/watch?v=Rp69edBmFFo",
            "channel": "The Cyber Mentor",
            "duration": "~4h",
            "level": "입문",
        },
        {
            "title": "Burp Suite for Beginners - Full Course",
            "url": "https://www.youtube.com/watch?v=h2duGBZLEek",
            "channel": "The Cyber Mentor",
            "duration": "~2h",
            "level": "입문",
        },
    ],
    "system-hacking": [
        {
            "title": "Linux Privilege Escalation for Beginners",
            "url": "https://www.youtube.com/watch?v=ZTnwg3qCdVM",
            "channel": "The Cyber Mentor",
            "duration": "~1.5h",
            "level": "입문→중급",
        },
        {
            "title": "Windows Privilege Escalation for Beginners",
            "url": "https://www.youtube.com/watch?v=uTcrbNBcoxQ",
            "channel": "The Cyber Mentor",
            "duration": "~1.5h",
            "level": "입문→중급",
        },
        {
            "title": "Ethical Hacking in 15 Hours - Full Course",
            "url": "https://www.youtube.com/watch?v=3FNYvj2U0HM",
            "channel": "The Cyber Mentor",
            "duration": "~15h",
            "level": "입문",
        },
    ],
    "ai-security": [
        {
            "title": "Prompt Injection Explained",
            "url": "https://www.youtube.com/watch?v=Sv5OLj2nVAQ",
            "channel": "LiveOverflow",
            "duration": "~30m",
            "level": "입문",
        },
        {
            "title": "How LLM Jailbreaks Work",
            "url": "https://www.youtube.com/watch?v=WEo8X1GxDSY",
            "channel": "Computerphile",
            "duration": "~15m",
            "level": "입문",
        },
    ],
    "ctf": [
        {
            "title": "HackTheBox Starting Point Walkthrough",
            "url": "https://www.youtube.com/watch?v=amMPU2x1MkQ",
            "channel": "IppSec",
            "duration": "~2h",
            "level": "입문",
        },
    ],
}


def ensure_dirs():
    """디렉토리 생성"""
    for d in [DOWNLOAD_DIR, SUBTITLE_DIR, TRANSLATED_DIR, AUDIO_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def check_dependencies():
    """필수 패키지 확인"""
    missing = []
    checks = {
        "yt-dlp": "yt_dlp",
        "whisper": "whisper",
        "deep-translator": "deep_translator",
        "gTTS": "gtts",
    }
    for pkg_name, import_name in checks.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append(pkg_name)

    if missing:
        print(f"[!] 누락된 패키지: {', '.join(missing)}")
        print(f"    pip install {' '.join(missing)}")
        return False
    return True


def step1_download(url: str, audio_only: bool = True) -> Path:
    """Step 1: yt-dlp로 영상/오디오 다운로드"""
    import yt_dlp

    print(f"\n[Step 1] 다운로드: {url}")

    ydl_opts = {
        "outtmpl": str(DOWNLOAD_DIR / "%(title)s.%(ext)s"),
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["en", "ko"],
        "subtitlesformat": "srt",
    }

    if audio_only:
        ydl_opts.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        })
    else:
        ydl_opts["format"] = "bestvideo[height<=720]+bestaudio/best[height<=720]"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get("title", "unknown")
        safe_title = "".join(c if c.isalnum() or c in " -_" else "_" for c in title)

        # 다운로드된 파일 찾기
        ext = "mp3" if audio_only else "mp4"
        candidates = list(DOWNLOAD_DIR.glob(f"*{safe_title[:30]}*.{ext}"))
        if not candidates:
            candidates = list(DOWNLOAD_DIR.glob(f"*.{ext}"))

        output = candidates[-1] if candidates else DOWNLOAD_DIR / f"{safe_title}.{ext}"
        print(f"  -> 저장: {output.name}")

        # 기존 자막 파일 확인
        srt_candidates = list(DOWNLOAD_DIR.glob(f"*{safe_title[:30]}*.srt"))
        if srt_candidates:
            for srt in srt_candidates:
                dest = SUBTITLE_DIR / srt.name
                srt.rename(dest)
                print(f"  -> 자막 이동: {dest.name}")

        return output


def step2_subtitle(audio_path: Path, model_size: str = "base") -> Path:
    """Step 2: Whisper로 자막 추출"""
    print(f"\n[Step 2] 자막 추출 (Whisper {model_size}): {audio_path.name}")

    # faster-whisper 사용 가능한지 확인
    try:
        from faster_whisper import WhisperModel
        print("  -> faster-whisper 사용 (GPU 가속)")
        model = WhisperModel(model_size, device="auto", compute_type="int8")
        segments, info = model.transcribe(str(audio_path), language="en")

        srt_path = SUBTITLE_DIR / f"{audio_path.stem}.en.srt"
        txt_path = SUBTITLE_DIR / f"{audio_path.stem}.en.txt"

        with open(srt_path, "w", encoding="utf-8") as srt_f, \
             open(txt_path, "w", encoding="utf-8") as txt_f:
            for i, seg in enumerate(segments, 1):
                start = format_timestamp(seg.start)
                end = format_timestamp(seg.end)
                srt_f.write(f"{i}\n{start} --> {end}\n{seg.text.strip()}\n\n")
                txt_f.write(f"{seg.text.strip()}\n")

    except ImportError:
        import whisper
        print("  -> openai-whisper 사용")
        model = whisper.load_model(model_size)
        result = model.transcribe(str(audio_path), language="en")

        srt_path = SUBTITLE_DIR / f"{audio_path.stem}.en.srt"
        txt_path = SUBTITLE_DIR / f"{audio_path.stem}.en.txt"

        with open(srt_path, "w", encoding="utf-8") as srt_f, \
             open(txt_path, "w", encoding="utf-8") as txt_f:
            for i, seg in enumerate(result["segments"], 1):
                start = format_timestamp(seg["start"])
                end = format_timestamp(seg["end"])
                text = seg["text"].strip()
                srt_f.write(f"{i}\n{start} --> {end}\n{text}\n\n")
                txt_f.write(f"{text}\n")

    print(f"  -> SRT: {srt_path.name}")
    print(f"  -> TXT: {txt_path.name}")
    return srt_path


def format_timestamp(seconds: float) -> str:
    """초를 SRT 타임스탬프로 변환"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def step3_translate(srt_path: Path, chunk_size: int = 50) -> Path:
    """Step 3: 한국어 번역"""
    from deep_translator import GoogleTranslator

    print(f"\n[Step 3] 한국어 번역: {srt_path.name}")

    translator = GoogleTranslator(source="en", target="ko")

    # SRT 파싱
    lines = srt_path.read_text(encoding="utf-8").strip().split("\n\n")
    translated_blocks = []
    text_lines = []

    for block in lines:
        parts = block.strip().split("\n")
        if len(parts) >= 3:
            idx = parts[0]
            timestamp = parts[1]
            text = " ".join(parts[2:])
            text_lines.append((idx, timestamp, text))

    # 청크 단위 번역 (API 제한 대응)
    print(f"  -> {len(text_lines)}개 자막 라인 번역 중...")
    ko_texts = []

    for i in range(0, len(text_lines), chunk_size):
        chunk = text_lines[i:i + chunk_size]
        batch = "\n---\n".join(t[2] for t in chunk)
        try:
            translated = translator.translate(batch)
            ko_texts.extend(translated.split("\n---\n"))
        except Exception as e:
            print(f"  [!] 번역 오류 (chunk {i}): {e}")
            ko_texts.extend(t[2] for t in chunk)

        # 진행 표시
        done = min(i + chunk_size, len(text_lines))
        print(f"  -> {done}/{len(text_lines)} 완료", end="\r")

    print()

    # 번역된 SRT 생성
    ko_srt_path = TRANSLATED_DIR / f"{srt_path.stem.replace('.en', '.ko')}.srt"
    ko_txt_path = TRANSLATED_DIR / f"{srt_path.stem.replace('.en', '.ko')}.txt"

    with open(ko_srt_path, "w", encoding="utf-8") as srt_f, \
         open(ko_txt_path, "w", encoding="utf-8") as txt_f:
        for i, (idx, ts, _) in enumerate(text_lines):
            ko_text = ko_texts[i] if i < len(ko_texts) else ""
            srt_f.write(f"{idx}\n{ts}\n{ko_text.strip()}\n\n")
            txt_f.write(f"{ko_text.strip()}\n")

    print(f"  -> 한국어 SRT: {ko_srt_path.name}")
    print(f"  -> 한국어 TXT: {ko_txt_path.name}")
    return ko_srt_path


def step4_tts(ko_srt_path: Path, engine: str = "auto") -> Path:
    """Step 4: 한국어 TTS → 수면용 음성 파일"""
    print(f"\n[Step 4] TTS 생성: {ko_srt_path.name}")

    ko_txt = TRANSLATED_DIR / f"{ko_srt_path.stem}.txt"
    if not ko_txt.exists():
        # SRT에서 텍스트만 추출
        text = extract_text_from_srt(ko_srt_path)
    else:
        text = ko_txt.read_text(encoding="utf-8")

    output_path = AUDIO_DIR / f"{ko_srt_path.stem}_sleep.mp3"

    # engine 자동 선택
    if engine == "auto":
        try:
            import edge_tts
            engine = "edge"
        except ImportError:
            engine = "gtts"

    if engine == "edge":
        _tts_edge(text, output_path)
    else:
        _tts_gtts(text, output_path)

    print(f"  -> 수면용 음성: {output_path.name}")
    return output_path


def _tts_edge(text: str, output_path: Path):
    """Microsoft Edge TTS (고품질, 무료)"""
    import asyncio
    import edge_tts

    print("  -> Edge TTS 사용 (고품질 한국어)")

    # 긴 텍스트를 문단 단위로 분할
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]

    async def generate():
        communicate = edge_tts.Communicate(
            "\n".join(paragraphs),
            voice="ko-KR-SunHiNeural",  # 여성 목소리 (차분)
            rate="-15%",  # 수면용이므로 약간 느리게
            pitch="-5Hz",  # 약간 낮은 톤
        )
        await communicate.save(str(output_path))

    asyncio.run(generate())


def _tts_gtts(text: str, output_path: Path):
    """Google TTS (기본)"""
    from gtts import gTTS

    print("  -> gTTS 사용 (기본 한국어)")

    # gTTS는 텍스트 길이 제한이 있으므로 분할
    chunks = []
    current = ""
    for line in text.split("\n"):
        if len(current) + len(line) > 4000:
            chunks.append(current)
            current = line
        else:
            current += "\n" + line
    if current:
        chunks.append(current)

    if len(chunks) == 1:
        tts = gTTS(text=chunks[0], lang="ko", slow=True)
        tts.save(str(output_path))
    else:
        # 여러 청크를 합치기
        from pydub import AudioSegment
        combined = AudioSegment.empty()
        for i, chunk in enumerate(chunks):
            tmp = output_path.parent / f"_tmp_{i}.mp3"
            tts = gTTS(text=chunk, lang="ko", slow=True)
            tts.save(str(tmp))
            combined += AudioSegment.from_mp3(str(tmp))
            tmp.unlink()
            print(f"  -> 청크 {i+1}/{len(chunks)} 완료", end="\r")
        print()
        combined.export(str(output_path), format="mp3")


def extract_text_from_srt(srt_path: Path) -> str:
    """SRT에서 텍스트만 추출"""
    lines = srt_path.read_text(encoding="utf-8").strip().split("\n\n")
    texts = []
    for block in lines:
        parts = block.strip().split("\n")
        if len(parts) >= 3:
            texts.append(" ".join(parts[2:]))
    return "\n".join(texts)


def process_url(url: str, steps: str = "all", subtitle_only: bool = False,
                whisper_model: str = "base", tts_engine: str = "auto"):
    """단일 URL 전체 파이프라인"""
    ensure_dirs()

    active_steps = steps.split(",") if steps != "all" else ["download", "subtitle", "translate", "tts"]

    audio_path = None
    srt_path = None
    ko_srt_path = None

    if "download" in active_steps:
        audio_path = step1_download(url, audio_only=True)

    if "subtitle" in active_steps and audio_path:
        # 이미 다운로드된 자막 확인
        existing = list(SUBTITLE_DIR.glob(f"{audio_path.stem}*.srt"))
        if existing:
            srt_path = existing[0]
            print(f"\n[Step 2] 기존 자막 사용: {srt_path.name}")
        else:
            srt_path = step2_subtitle(audio_path, model_size=whisper_model)

    if "translate" in active_steps and srt_path:
        ko_srt_path = step3_translate(srt_path)

    if "tts" in active_steps and ko_srt_path and not subtitle_only:
        step4_tts(ko_srt_path, engine=tts_engine)

    print("\n" + "=" * 60)
    print("파이프라인 완료!")
    print("=" * 60)


def process_from_srt(srt_path: str, tts_engine: str = "auto"):
    """기존 SRT에서 번역 + TTS"""
    ensure_dirs()
    path = Path(srt_path)
    ko_srt = step3_translate(path)
    step4_tts(ko_srt, engine=tts_engine)


def show_recommended():
    """추천 강의 리스트 출력"""
    print("\n" + "=" * 60)
    print("추천 마스터 강의 리스트")
    print("=" * 60)

    for category, lectures in RECOMMENDED.items():
        print(f"\n## {category.upper()}")
        for i, lec in enumerate(lectures, 1):
            print(f"  {i}. [{lec['level']}] {lec['title']}")
            print(f"     채널: {lec['channel']} | 시간: {lec['duration']}")
            print(f"     URL: {lec['url']}")
        print()


def process_recommended(category: str = "all", tts_engine: str = "auto"):
    """추천 강의 전체 또는 카테고리별 처리"""
    ensure_dirs()

    categories = RECOMMENDED.keys() if category == "all" else [category]

    for cat in categories:
        if cat not in RECOMMENDED:
            print(f"[!] 알 수 없는 카테고리: {cat}")
            continue

        print(f"\n{'='*60}")
        print(f"카테고리: {cat}")
        print(f"{'='*60}")

        for lec in RECOMMENDED[cat]:
            print(f"\n>>> {lec['title']} ({lec['duration']})")
            try:
                process_url(lec["url"], tts_engine=tts_engine)
            except Exception as e:
                print(f"  [!] 오류: {e}")
                continue


def main():
    parser = argparse.ArgumentParser(
        description="유튜브 마스터 강의 처리 파이프라인",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  %(prog)s "https://youtube.com/watch?v=xxx"       # 전체 파이프라인
  %(prog)s --list                                    # 추천 강의 목록
  %(prog)s --playlist recommended                    # 추천 강의 전체 처리
  %(prog)s --playlist web-hacking                    # 카테고리별 처리
  %(prog)s "URL" --subtitle-only                     # 자막만 추출
  %(prog)s --from-srt subtitle.en.srt                # 기존 SRT에서 번역+TTS
  %(prog)s "URL" --whisper-model medium              # Whisper 모델 선택
  %(prog)s "URL" --tts edge                          # TTS 엔진 선택
        """,
    )
    parser.add_argument("url", nargs="?", help="유튜브 URL")
    parser.add_argument("--list", action="store_true", help="추천 강의 목록")
    parser.add_argument("--playlist", type=str, help="추천 강의 처리 (all/카테고리명)")
    parser.add_argument("--from-srt", type=str, help="기존 SRT에서 번역+TTS")
    parser.add_argument("--subtitle-only", action="store_true", help="자막만 추출")
    parser.add_argument("--steps", default="all", help="실행 단계 (download,subtitle,translate,tts)")
    parser.add_argument("--whisper-model", default="base",
                       choices=["tiny", "base", "small", "medium", "large"],
                       help="Whisper 모델 크기")
    parser.add_argument("--tts", default="auto", choices=["auto", "edge", "gtts"],
                       help="TTS 엔진")
    parser.add_argument("--check", action="store_true", help="의존성 확인")

    args = parser.parse_args()

    if args.check:
        check_dependencies()
        return

    if args.list:
        show_recommended()
        return

    if args.playlist:
        if not check_dependencies():
            return
        process_recommended(args.playlist, tts_engine=args.tts)
        return

    if args.from_srt:
        if not check_dependencies():
            return
        process_from_srt(args.from_srt, tts_engine=args.tts)
        return

    if args.url:
        if not check_dependencies():
            return
        process_url(
            args.url,
            steps=args.steps,
            subtitle_only=args.subtitle_only,
            whisper_model=args.whisper_model,
            tts_engine=args.tts,
        )
        return

    parser.print_help()


if __name__ == "__main__":
    main()
