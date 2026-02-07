# JailbreakBench (학술 표준)

- **URL**: https://jailbreakbench.github.io/
- **소스**: NeurIPS 2024 Datasets and Benchmarks
- **최종 수집일**: 2026-02-08

## 개요

JailbreakBench는 jailbreak 공격 평가의 파편화 문제를 해결하기 위한 중앙 집중식 벤치마크.

### 핵심 과제 3가지
1. 유해 응답 평가 표준화
2. 비교 가능한 비용 메트릭 생성
3. 오픈소스 아티팩트를 통한 재현성 보장

## 핵심 구성요소

### 1. Jailbreak Artifacts Repository
- 최신 adversarial prompt의 진화하는 데이터셋
- GitHub에서 관리
- 모든 벤치마크 제출 시 재현성 보장을 위해 필수

### 2. 표준화된 평가 프레임워크
- 명확하게 정의된 위협 모델
- 시스템 프롬프트, 채팅 템플릿, 스코어링 함수 제공
- 다양한 모델과 공격 간 일관된 평가 가능

### 3. 리더보드
- 오픈소스 / 클로즈드소스 모델 별도 랭킹
- 공격 성공률 + 방어 효과 모니터링

### 4. JBB-Behaviors 데이터셋
- **100개 유해 행동** 테스트셋 (OpenAI 사용 정책 기반)
  - 55% 오리지널
  - AdvBench, HarmBench에서 보충
- **100개 양성 행동**: 모델 overrefusal rate 평가용

## 핵심 특징
- 재현성 강조 (adversarial prompt 제출 필수)
- 표준화된 위협 모델 및 평가 방법론
- 공격/방어 모두 제출 지원
- AdvBench, HarmBench 등 기존 안전성 연구 데이터셋 통합

## 인용
- NeurIPS 2024 Datasets and Benchmarks 논문
- 구성 데이터셋 (AdvBench, HarmBench) 별도 인용 필요
