# AI 응답 개선 비교 테스트 스크립트

MARUNI 프로젝트의 AI 대화 응답을 다양한 설정으로 테스트하고 자동으로 비교 보고서를 생성하는 Python 스크립트입니다.

## 📋 개요

**✨ 새로운 기능: Spring Profiles 자동 전환!**
- 더 이상 `application-ai.yml` 파일을 수동으로 수정할 필요가 없습니다
- Profile만 전환하면 자동으로 설정 적용
- 더 빠르고 안전한 테스트 프로세스

이 스크립트는 다음 작업을 자동화합니다:

1. **5개 시나리오 테스트**
   - 긍정적 일상 대화
   - 부정적 감정 대화
   - 건강 관련 대화
   - 멀티턴 대화 (이전 대화 기억)
   - 가족 관련 대화

2. **4가지 설정 비교**
   - Baseline: 현재 설정
   - 개선안 1: 시스템 프롬프트 고도화
   - 개선안 2: Temperature + 응답 길이 조정
   - 개선안 3: 통합 설정

3. **자동 보고서 생성**
   - 시나리오별 응답 비교표
   - 자동 평가 (별점)
   - 종합 분석 및 권장 사항

## 🚀 빠른 시작

### 1. Python 환경 설정

```bash
# Python 3.7 이상 필요
python --version

# 필요한 라이브러리 설치
pip install -r requirements.txt
```

### 2. 서버 실행 (Baseline Profile, Test 환경)

첫 테스트를 위해 **Test 환경 + Baseline Profile**로 서버를 실행합니다:

```bash
# 프로젝트 루트 디렉토리에서
./gradlew bootRun --args='--spring.profiles.active=test,ai,ai-baseline'

# Windows 환경
gradlew.bat bootRun --args='--spring.profiles.active=test,ai,ai-baseline'
```

**💡 Test 환경의 장점**:
- ✅ **H2 인메모리 DB** 사용 → PostgreSQL/Docker 불필요
- ✅ **빠른 시작** → 1-2초 내 실행
- ✅ **데이터 격리** → 매번 깨끗한 상태로 테스트
- ✅ **설치 불필요** → 바로 실행 가능

서버가 완전히 시작될 때까지 기다립니다 (http://localhost:8080)

### 3. 스크립트 실행

```bash
# scripts 디렉토리로 이동
cd scripts

# 테스트 실행
python ai_response_comparison_test.py
```

## 📖 사용 방법

### 진행 과정

스크립트는 대화형으로 진행됩니다:

```
1. [Baseline] 테스트 시작
   → 5개 시나리오 자동 테스트
   → 완료

2. Profile 변경 안내 표시
   → 서버 재시작 (새로운 Profile로)
   → Enter 입력하여 계속

3. [개선안 1] 테스트 시작
   → 5개 시나리오 자동 테스트
   → 완료

4. (2-3 반복)

5. 모든 테스트 완료
   → JSON 결과 저장
   → Markdown 보고서 생성
```

### 설정 변경 가이드 (Spring Profiles 사용)

이제 `application-ai.yml` 파일을 수정할 필요 없이, **Spring Profile만 전환**하면 됩니다!

#### 개선안 1: 시스템 프롬프트 고도화

**Profile**: `ai-improved1`

```bash
# 서버 재시작 시
./gradlew bootRun --args='--spring.profiles.active=test,ai,ai-improved1'

# Windows
gradlew.bat bootRun --args='--spring.profiles.active=test,ai,ai-improved1'
```

설정 파일: `src/main/resources/application-ai-improved1.yml` (자동 적용)

#### 개선안 2: Temperature + 응답 길이 조정

**Profile**: `ai-improved2`

```bash
# 서버 재시작 시
./gradlew bootRun --args='--spring.profiles.active=test,ai,ai-improved2'

# Windows
gradlew.bat bootRun --args='--spring.profiles.active=test,ai,ai-improved2'
```

설정 파일: `src/main/resources/application-ai-improved2.yml` (자동 적용)

#### 개선안 3: 통합 설정

**Profile**: `ai-improved3`

```bash
# 서버 재시작 시
./gradlew bootRun --args='--spring.profiles.active=test,ai,ai-improved3'

# Windows
gradlew.bat bootRun --args='--spring.profiles.active=test,ai,ai-improved3'
```

설정 파일: `src/main/resources/application-ai-improved3.yml` (자동 적용)

## 📊 결과 확인

테스트 완료 후 `scripts/output/` 디렉토리에 생성됩니다:

```
scripts/output/
├── responses_20250109_143022.json      # 원시 응답 데이터
└── comparison_report_20250109_143022.md # 비교 보고서
```

### 보고서 내용

1. **테스트 개요**
   - 테스트 설정 목록
   - 시나리오 목록

2. **시나리오별 비교**
   - 각 설정별 AI 응답
   - 감정 분석 결과
   - 자동 평가 점수 및 별점

3. **종합 평가**
   - 설정별 평균 점수
   - 장단점 분석
   - 최종 권장 사항

## 🔧 고급 설정

### 서버 URL 변경

```python
tester = AIResponseComparisonTest(base_url="http://your-server:8080")
```

### 시나리오 커스터마이징

`ai_response_comparison_test.py` 파일의 `load_scenarios()` 메서드를 수정하여 시나리오를 추가/변경할 수 있습니다.

## ⚠️ 주의사항

1. **OpenAI API 비용**
   - 총 20회 API 호출 발생 (5 시나리오 × 4 설정)
   - 예상 비용: ~$0.02 (약 30원)

2. **테스트 시간**
   - 각 설정당 약 5-10분 소요
   - 총 30-40분 예상 (설정 변경 시간 포함)

3. **서버 재시작 필수**
   - 각 Profile 변경 시 반드시 서버 재시작 필요
   - Spring Boot Profile은 런타임 변경 불가
   - 스크립트가 명령어를 자동으로 안내합니다

4. **대화 이력**
   - 각 시나리오는 새로운 사용자로 테스트
   - 이전 테스트의 대화 이력은 영향 없음

## 🐛 문제 해결

### 서버 연결 실패

```
❌ 서버에 연결할 수 없습니다.
```

**해결 방법**:
- 서버가 실행 중인지 확인: `./gradlew bootRun`
- URL 확인: `http://localhost:8080/actuator/health`

### 회원가입 실패

```
❌ 회원가입 실패: 400
```

**해결 방법**:
- 데이터베이스가 실행 중인지 확인
- 이전 테스트 데이터 정리 필요할 수 있음

### OpenAI API 오류

```
❌ 메시지 전송 오류: timeout
```

**해결 방법**:
- OPENAI_API_KEY 환경변수 확인
- API 키 유효성 확인
- 네트워크 연결 확인
