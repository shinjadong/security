# NotebookLM & 유튜브 학습 파이프라인

## 1. NotebookLM 사용법

### Step 1: Google NotebookLM 접속
https://notebooklm.google.com

### Step 2: 새 노트북 생성 → 소스 추가

아래 파일을 업로드:
- `hacking-security-principles.md` - 14개 핵심 원리 + 실제 사건 스토리

### Step 3: 음성 콘텐츠 생성
- "Audio Overview" 버튼 클릭
- 팟캐스트 스타일의 음성 콘텐츠 자동 생성
- 두 명의 호스트가 대화하며 내용 설명

### 추가 소스 (같이 올리면 더 좋음)
- `../phase3-ai-security/jailbreak-답지.md` - AI 공격 기법 상세
- `../phase3-ai-security/defense-답지.md` - 방어 기법 상세
- `../phase3-ai-security/key-papers.md` - 핵심 논문 해설

---

## 2. 유튜브 강의 처리 파이프라인

### 설치
```bash
# 필수 패키지
pip install yt-dlp openai-whisper deep-translator gTTS pydub

# 고품질 TTS (추천)
pip install edge-tts

# GPU 가속 Whisper (추천, CUDA 필요)
pip install faster-whisper

# Termux 추가 설정
pkg install ffmpeg
```

### 사용법

```bash
# 추천 강의 목록 보기
python scripts/youtube_pipeline.py --list

# 단일 영상 전체 처리 (다운로드 → 자막 → 번역 → 수면 음성)
python scripts/youtube_pipeline.py "https://youtube.com/watch?v=xxx"

# 웹 해킹 카테고리 전체 처리
python scripts/youtube_pipeline.py --playlist web-hacking

# 자막만 추출
python scripts/youtube_pipeline.py "URL" --subtitle-only

# 기존 자막에서 번역 + 음성 생성
python scripts/youtube_pipeline.py --from-srt subtitles/lecture.en.srt

# Whisper 모델 크기 조절 (tiny/base/small/medium/large)
python scripts/youtube_pipeline.py "URL" --whisper-model medium
```

### 처리 결과 위치
```
media/
├── downloads/      # 원본 오디오/영상
├── subtitles/      # 영어 자막 (SRT + TXT)
├── translated/     # 한국어 번역 (SRT + TXT)
└── sleep-audio/    # 수면용 한국어 음성 (MP3)
```

---

## 3. 추천 마스터 강의

### 웹 해킹 (Phase 1)
| 강의 | 채널 | 시간 | 레벨 |
|------|------|------|------|
| Web Security Academy Full Course | The Cyber Mentor | ~15h | 입문→중급 |
| Bug Bounty Hunting Full Course | The Cyber Mentor | ~4h | 입문 |
| Burp Suite for Beginners | The Cyber Mentor | ~2h | 입문 |

### 시스템 해킹 (Phase 2)
| 강의 | 채널 | 시간 | 레벨 |
|------|------|------|------|
| Linux Privilege Escalation | The Cyber Mentor | ~1.5h | 입문→중급 |
| Windows Privilege Escalation | The Cyber Mentor | ~1.5h | 입문→중급 |
| Ethical Hacking in 15 Hours | The Cyber Mentor | ~15h | 입문 |

### AI 보안 (Phase 3)
| 강의 | 채널 | 시간 | 레벨 |
|------|------|------|------|
| Prompt Injection Explained | LiveOverflow | ~30m | 입문 |
| How LLM Jailbreaks Work | Computerphile | ~15m | 입문 |

### CTF/실전
| 강의 | 채널 | 시간 | 레벨 |
|------|------|------|------|
| HackTheBox Starting Point | IppSec | ~2h | 입문 |

---

## 4. 수면 학습 루틴

```
22:00 - 취침 준비
22:30 - sleep-audio/ 폴더의 MP3 재생 (볼륨 30%)
        → 한국어 번역된 보안 강의가 차분한 목소리로 재생
23:00 - 잠들기
        → 무의식적으로 용어와 개념 반복 노출

아침 루틴:
07:00 - NotebookLM 팟캐스트 들으며 출근/운동
        → 전날 수면 중 들은 내용의 능동적 복습
```
