# Claude Code 컨텍스트 문서

**마지막 업데이트**: 2025-11-09
**작업 상태**: AI 응답 개선 비교 테스트 스크립트 완성

---

## 📂 프로젝트 구조

```
~/coding/maruni/
├── maruni-server/              # Spring Boot 백엔드 프로젝트
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/anyang/maruni/
│   │   │   │   └── domain/conversation/  # AI 대화 도메인
│   │   │   └── resources/
│   │   │       └── application-ai.yml     # AI 설정 파일 (여기를 수정)
│   │   └── test/
│   └── docs/                   # 프로젝트 문서
│
└── scripts/                    # AI 응답 테스트 스크립트 (현재 위치)
    ├── ai_response_comparison_test.py  # 메인 테스트 스크립트
    ├── requirements.txt                # Python 라이브러리
    ├── README.md                       # 상세 가이드
    ├── QUICKSTART.md                   # 빠른 시작 가이드
    ├── config/                         # 설정 파일 예시
    │   ├── baseline_config.yml
    │   ├── improved_prompt_config.yml
    │   ├── improved_params_config.yml
    │   └── improved_combined_config.yml
    └── output/                         # 테스트 결과 저장 (자동 생성)
        ├── responses_*.json            # 원시 응답 데이터
        └── comparison_report_*.md      # 비교 보고서
```

---

## 🎯 현재 작업 상황

### 완료된 작업 ✅

1. **Conversation 도메인 구조 파악**
   - Rich Domain Model (ConversationEntity, MessageEntity)
   - OpenAI GPT-4o 연동 (OpenAIResponseAdapter)
   - 키워드 기반 감정 분석 (KeywordBasedEmotionAnalyzer)
   - 멀티턴 대화 지원 (최근 5턴 히스토리)

2. **AI 응답 개선 방안 제안**
   - 즉시 적용 가능한 3가지 개선안
   - 중간 난이도 개선 방안
   - 고급 기능 제안

3. **Python 테스트 스크립트 개발 완료**
   - 5개 시나리오 자동 테스트
   - 4가지 설정 비교 (baseline, improved_prompt, improved_params, improved_combined)
   - 자동 평가 및 보고서 생성

### 다음 단계 📋

- [ ] 테스트 스크립트 실행 (Baseline)
- [ ] 개선안 1 적용 및 테스트
- [ ] 개선안 2 적용 및 테스트
- [ ] 개선안 3 적용 및 테스트
- [ ] 비교 보고서 분석 및 최종 권장안 도출

---

## 🔑 핵심 파일 위치

### 수정이 필요한 파일

**AI 설정 파일**:
```
~/coding/maruni/maruni-server/src/main/resources/application-ai.yml
```

이 파일을 수정하여 AI 응답을 개선합니다.

### 참조 설정 파일

**설정 예시 파일들** (복사해서 사용):
```
~/coding/maruni/scripts/config/
├── baseline_config.yml         # 현재 설정
├── improved_prompt_config.yml  # 개선안 1: 프롬프트 고도화
├── improved_params_config.yml  # 개선안 2: 파라미터 조정
└── improved_combined_config.yml # 개선안 3: 통합
```

### 테스트 스크립트

**실행 파일**:
```
~/coding/maruni/scripts/ai_response_comparison_test.py
```

---

## 🚀 빠른 실행 방법

### 1. Python 환경 준비

```bash
cd ~/coding/maruni/scripts
pip install -r requirements.txt
```

### 2. 서버 실행 (새 터미널)

```bash
cd ~/coding/maruni/maruni-server
./gradlew bootRun
```

### 3. 테스트 실행

```bash
cd ~/coding/maruni/scripts
python ai_response_comparison_test.py
```

---

## 📊 테스트 시나리오

### 5개 시나리오 정의

1. **긍정적 일상 대화**
   - 메시지: "오늘 날씨가 참 좋네요"
   - 평가: 공감, 질문, 친근함

2. **부정적 감정 대화**
   - 메시지: "요즘 혼자 있으니까 외로워요"
   - 평가: 공감, 위로, 긍정적 방향

3. **건강 관련 대화**
   - 메시지: "무릎이 좀 아파요"
   - 평가: 공감, 의료조언 회피, 관심

4. **멀티턴 대화**
   - 컨텍스트: 이전에 공원 산책 이야기
   - 메시지: "오늘도 공원 다녀올까 해요"
   - 평가: 이전 대화 언급, 자연스러운 연결, 구체적 질문

5. **가족 관련 대화**
   - 컨텍스트: 손자 시험 이야기
   - 메시지: "시험 결과가 좋게 나왔대요"
   - 평가: 이전 대화 기억, 함께 기뻐하기, 추가 질문

---

## 🎨 AI 개선 방안

### Baseline (현재)
```yaml
temperature: 0.7
max-tokens: 100
max-response-length: 100
system-prompt: "당신은 노인 돌봄 전문 AI 상담사입니다. 따뜻하고 공감적으로 30자 이내로 응답하세요."
```

### 개선안 1: 시스템 프롬프트 고도화
- 페르소나 '마루' 부여
- 구체적인 대화 스타일 정의
- 금지 사항 명시

### 개선안 2: Temperature + 응답 길이 조정
```yaml
temperature: 0.9      # 더 창의적
max-tokens: 150       # 더 긴 응답
max-response-length: 200
```

### 개선안 3: 통합 설정
- 개선안 1 + 개선안 2
- 최종 권장 설정

---

## 🔧 주요 설정 변경 방법

### 방법 1: 설정 파일 복사
```bash
# 개선안 1 적용 예시
cat ~/coding/maruni/scripts/config/improved_prompt_config.yml
# 내용 복사 → application-ai.yml에 붙여넣기
```

### 방법 2: 직접 수정
`~/coding/maruni/maruni-server/src/main/resources/application-ai.yml` 파일을 직접 편집

---

## 💾 결과 파일

테스트 실행 후 자동 생성:

### JSON 응답 데이터
```
~/coding/maruni/scripts/output/responses_YYYYMMDD_HHMMSS.json
```

**포함 내용**:
- 모든 시나리오별 실제 응답
- 감정 분석 결과
- 타임스탬프

### Markdown 비교 보고서
```
~/coding/maruni/scripts/output/comparison_report_YYYYMMDD_HHMMSS.md
```

**포함 내용**:
- 시나리오별 비교 표
- 자동 평가 (별점)
- 설정별 평균 점수
- 종합 분석
- 최종 권장 사항

---

## 🐛 문제 해결

### 서버 연결 실패
```bash
# 서버 상태 확인
curl http://localhost:8080/actuator/health

# 서버 재시작
cd ~/coding/maruni/maruni-server
./gradlew bootRun
```

### Python 라이브러리 오류
```bash
cd ~/coding/maruni/scripts
pip install -r requirements.txt --upgrade
```

### OPENAI_API_KEY 오류
```bash
# .env 파일 확인
cat ~/coding/maruni/maruni-server/.env

# 환경변수 확인
echo $OPENAI_API_KEY
```

---

## 📖 문서 참조

### 프로젝트 문서
```
~/coding/maruni/maruni-server/docs/domains/conversation.md
```
- Conversation 도메인 상세 구조
- API 명세
- 핵심 메서드

### 스크립트 가이드
```
~/coding/maruni/scripts/README.md       # 상세 가이드
~/coding/maruni/scripts/QUICKSTART.md   # 빠른 시작
```

---

## 🎯 Claude에게 전달할 프롬프트

다음 대화 세션에서 이 프롬프트를 사용하세요:

```
MARUNI 프로젝트의 AI 응답 개선 작업을 이어서 진행하려고 합니다.

**현재 상황**:
- Conversation 도메인 구조 파악 완료
- AI 응답 개선 방안 3가지 제안 완료
- Python 테스트 스크립트 개발 완료

**프로젝트 구조**:
- Spring Boot 프로젝트: ~/coding/maruni/maruni-server
- 테스트 스크립트: ~/coding/maruni/scripts

**다음 작업**:
[여기에 하고 싶은 작업 작성]

자세한 컨텍스트는 ~/coding/maruni/scripts/CONTEXT_FOR_CLAUDE.md 파일을 참조해주세요.
```

---

## 💡 추가 작업 아이디어

### 즉시 가능한 작업
- [ ] 테스트 스크립트 실행하여 실제 응답 비교
- [ ] 보고서 기반 최종 설정 결정
- [ ] application-ai.yml에 최종 설정 적용

### 향후 개선 작업
- [ ] 회원 정보 연동 (실제 이름, 나이, 관심사)
- [ ] 페르소나 시스템 구현
- [ ] 대화 스타일 커스터마이징
- [ ] 장기 메모리 시스템 추가

### 분석 작업
- [ ] 실제 응답 데이터 상세 분석
- [ ] 감정 분석 정확도 평가
- [ ] 멀티턴 대화 효과성 측정

---

## 📞 참고 정보

**프로젝트**: MARUNI (노인 돌봄 AI 플랫폼)
**도메인**: Conversation (AI 대화)
**기술 스택**: Spring Boot 3.5, OpenAI GPT-4o, Python 3.x
**작업 목표**: AI 응답을 더 사람처럼 자연스럽게 개선

**비용**: OpenAI API 약 $0.02 (20회 호출)
**소요 시간**: 30-40분 (테스트 자동화)

---

**다음 작업 시작 시 이 문서를 Claude에게 공유하세요!**
