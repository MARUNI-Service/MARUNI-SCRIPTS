# 🚀 빠른 시작 가이드

AI 응답 비교 테스트를 처음 실행하는 분들을 위한 단계별 가이드입니다.

## ⏱️ 예상 소요 시간: 30-40분

## 📝 사전 준비

### 1. Python 설치 확인

```bash
python --version
# Python 3.7 이상이어야 합니다
```

Python이 없다면 https://www.python.org/downloads/ 에서 설치하세요.

### 2. 라이브러리 설치

```bash
cd scripts
pip install -r requirements.txt
```

### 3. 서버 실행

**새 터미널을 열어서** 서버를 실행합니다:

```bash
# 프로젝트 루트 디렉토리에서
./gradlew bootRun
```

서버가 완전히 시작될 때까지 기다립니다 (1-2분).

확인 방법: 브라우저에서 http://localhost:8080/actuator/health 접속

---

## 🎯 테스트 실행

### 1단계: Baseline 테스트

**터미널 1 (서버 실행 중)**: 그대로 둡니다.

**터미널 2 (테스트 실행)**:
```bash
cd scripts
python ai_response_comparison_test.py
```

스크립트가 자동으로 5개 시나리오를 테스트합니다 (약 5분 소요).

---

### 2단계: 개선안 1 테스트 (프롬프트 고도화)

스크립트가 다음과 같이 표시합니다:

```
⚙️  설정 변경이 필요합니다!

📋 변경 사항:
   파일: src/main/resources/application-ai.yml

   변경 내용:
   maruni.conversation.ai.system-prompt:
     "당신은 '마루'라는 이름의 따뜻한 AI 친구입니다.
      ..."

📌 단계:
   1. application-ai.yml 파일 수정
   2. 서버 재시작 (Ctrl+C 후 ./gradlew bootRun)
   3. 서버가 완전히 시작될 때까지 대기

✋ 준비가 완료되면 Enter를 눌러 테스트를 시작하세요...
```

**할 일:**

1. **VS Code에서** `src/main/resources/application-ai.yml` 파일 열기

2. `scripts/config/improved_prompt_config.yml` 파일 내용을 복사

3. `application-ai.yml`의 해당 부분에 붙여넣기

4. **터미널 1**에서:
   ```bash
   # Ctrl+C로 서버 중지
   ./gradlew bootRun  # 서버 재시작
   ```

5. 서버가 완전히 시작되면 **터미널 2**에서 **Enter** 입력

스크립트가 다시 5개 시나리오를 테스트합니다 (약 5분).

---

### 3단계: 개선안 2 테스트 (파라미터 조정)

같은 방식으로:

1. `scripts/config/improved_params_config.yml` 내용 확인

2. `application-ai.yml` 수정:
   ```yaml
   spring.ai.openai.chat.options.temperature: 0.9
   spring.ai.openai.chat.options.max-tokens: 150
   maruni.conversation.ai.max-response-length: 200
   ```

3. 서버 재시작

4. Enter 입력

---

### 4단계: 개선안 3 테스트 (통합)

1. `scripts/config/improved_combined_config.yml` 내용 적용
   - 프롬프트 + 파라미터 모두 변경

2. 서버 재시작

3. Enter 입력

---

## 📊 결과 확인

테스트가 완료되면:

```
🎉 모든 테스트 완료!
💾 결과 저장 완료: scripts/output/responses_20250109_143022.json
📄 보고서 생성 완료: scripts/output/comparison_report_20250109_143022.md
```

**보고서 열기:**

1. VS Code에서 `scripts/output/comparison_report_*.md` 파일 열기

2. Markdown Preview로 보기 (Ctrl+Shift+V 또는 우클릭 → "Open Preview")

---

## 🎨 보고서 샘플

보고서에는 다음 내용이 포함됩니다:

### 시나리오별 비교 표

| 설정 | AI 응답 | 감정 분석 | 평가 점수 | 별점 |
|------|---------|-----------|-----------|------|
| **baseline** | 좋은 날씨네요! | POSITIVE | 2/3 | ⭐⭐⭐ |
| **improved_prompt** | 정말 좋은 날씨네요! 산책 다녀오셨어요? | POSITIVE | 3/3 | ⭐⭐⭐⭐⭐ |
| **improved_params** | 와, 정말 화창한 날씨네요! 기분이 좋아지시겠어요 | POSITIVE | 3/3 | ⭐⭐⭐⭐⭐ |
| **improved_combined** | 정말 좋은 날씨네요! 이런 날은 공원 산책 가시면 좋겠어요~ | POSITIVE | 3/3 | ⭐⭐⭐⭐⭐ |

### 종합 평가

- **최종 추천**: `improved_combined`
- 가장 자연스럽고 공감적인 응답
- 노인 돌봄 서비스 목적에 가장 부합

---

## ⚠️ 문제 해결

### "서버에 연결할 수 없습니다"

→ 서버가 실행 중인지 확인: `./gradlew bootRun`

### "회원가입 실패"

→ 데이터베이스가 실행 중인지 확인: `docker-compose up -d`

### "메시지 전송 오류: timeout"

→ OPENAI_API_KEY 환경변수가 설정되어 있는지 확인

### 프롬프트 변경이 적용 안 됨

→ 서버를 **완전히 재시작**했는지 확인 (Ctrl+C 후 다시 실행)

---

## 💰 비용 안내

- **OpenAI API 비용**: 약 $0.02 (30원)
- 5개 시나리오 × 4개 설정 = 20회 호출
- GPT-4o 모델 사용

---

## 📞 도움이 필요하신가요?

1. `scripts/README.md` 파일의 상세 가이드 참조
2. 서버 로그 확인
3. `scripts/output/` 폴더의 JSON 파일 확인

---

## ✅ 체크리스트

테스트 전 확인:

- [ ] Python 3.7 이상 설치
- [ ] `pip install -r requirements.txt` 완료
- [ ] 서버 실행 중 (http://localhost:8080/actuator/health 응답 확인)
- [ ] OPENAI_API_KEY 환경변수 설정
- [ ] 데이터베이스 실행 중

준비 완료! 🚀

```bash
python ai_response_comparison_test.py
```
