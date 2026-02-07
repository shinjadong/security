# 9월 릴리스: 더 스마트한 방어와 더 강한 공격

- **URL**: https://calypsoai.com/news/september-release-smarter-defenses-and-stronger-attacks/
- **날짜**: 2025-09-09
- **수집일**: 2026-02-08
- **저자**: Jessica Brennan

---

## September Release: Smarter Defenses and Stronger Attacks

CalypsoAI's September release introduces significant updates across its Inference platform, focusing on defensive capabilities, expanded attack vectors, and improved user experience. The update emphasizes making AI security tools more intuitive and effective for enterprise deployments.

---

## Inference Defend Updates

### AI Assistant for Scanner Creation
A new AI Assistant helps refine custom scanner prompts by optimizing them according to CalypsoAI's best practices. Users retain full control, able to accept suggestions or maintain their original prompts.

### Redaction Feature
"Redact sensitive content instead of blocking it" is now available. Regex and keyword scanners can replace matched content with asterisks, allowing responses while protecting sensitive data. The platform states that "redacted content is never stored in prompt history."

### Enhanced Access Controls
Scanner access settings now offer improved flexibility:
- Toggle access for all projects
- Select all current projects with exclusion of future ones
- Choose specific projects via multi-select interface

---

## Inference Red-Team Enhancements

### Expanded Attack Pack
The latest signature attack pack delivers over **11,500 new adversarial prompts** across multiple families including MathPrompt, DAN, and payload splitting techniques.

### FlipAttack Vector
A new attack method "flips word order, characters, or sentences before asking the model to denoise the text -- disguising harmful requests and bypassing safeguards."

### TLS Operational Improvements
The TLS attack received reworking to support additional security header checks and reduced false positives by lowering minimum recommended version to TLS 1.2.

### Refusal Checker
A new capability evaluates model responses based on the response alone, not attack prompts, and recognizes error messages as refusals, improving accuracy.

### Campaign Creation
Direct links to Reports pages now appear in toast messages when creating campaigns, streamlining workflow.

### Rate Limiting Options
New _Max concurrent requests_ setting allows testing smaller models without rate limit errors.

---

## Platform Improvements

### Default Model Visibility
The global default model now appears above connection lists, with confirmation toasts and undo options when changes occur.

---

## Bug Fixes

September's patch addressed:
- Report alerts and button sizing
- Provider misconfiguration error messaging
- Custom scanner, report, and agent attack prompt UI issues
- Formatting consistency across views

### Key Takeaways

- AI 어시스턴트 기반 커스텀 스캐너 생성 지원
- 민감 콘텐츠 차단 대신 마스킹(Redaction) 기능 추가
- 11,500개 이상의 새로운 적대적 프롬프트 포함 공격 팩 확장
- FlipAttack: 단어/문자/문장 순서를 뒤집어 유해 요청을 위장하는 새 공격 벡터
- Refusal Checker: 응답만으로 거부 여부를 평가하는 새 기능
- TLS 공격 개선으로 오탐 감소
