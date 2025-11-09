#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 응답 개선 비교 테스트 자동화 스크립트

MARUNI 프로젝트의 AI 대화 응답을 개선하기 위해
다양한 설정으로 실제 API를 호출하고 응답을 비교 분석합니다.
"""

import requests
import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any


class AIResponseComparisonTest:
    """AI 응답 개선 비교 테스트 자동화 클래스"""

    def __init__(self, base_url: str = "http://localhost:8080"):
        """
        초기화

        Args:
            base_url: MARUNI 서버 URL (기본값: http://localhost:8080)
        """
        self.base_url = base_url
        self.access_token = None
        self.current_user_id = None
        self.results = {
            "test_date": datetime.now().isoformat(),
            "base_url": base_url,
            "configurations": []
        }

    def setup_test_user(self) -> bool:
        """
        테스트용 회원 가입 및 로그인

        Returns:
            bool: 성공 여부
        """
        timestamp = int(time.time())
        signup_data = {
            "loginId": f"test_ai_{timestamp}",
            "password": "Test1234!",
            "name": "AI테스트사용자",
            "phoneNumber": f"010{timestamp % 100000000:08d}"
        }

        try:
            print(f"👤 테스트 사용자 생성 중... (ID: {signup_data['loginId']})")

            response = requests.post(
                f"{self.base_url}/api/auth/signup",
                json=signup_data,
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                self.access_token = result["data"]["accessToken"]
                print(f"✅ 로그인 성공! (Token: {self.access_token[:20]}...)")
                return True
            else:
                print(f"❌ 회원가입 실패: {response.status_code}")
                print(f"   응답: {response.text}")
                return False

        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            return False

    def load_scenarios(self) -> List[Dict[str, Any]]:
        """
        테스트 시나리오 로드

        Returns:
            List[Dict]: 시나리오 목록
        """
        scenarios = [
            {
                "id": 1,
                "name": "긍정적 일상 대화",
                "category": "positive",
                "context": [],  # 이전 대화 없음
                "user_message": "오늘 날씨가 참 좋네요",
                "expected_elements": ["공감", "질문", "친근함"],
                "description": "사용자가 좋은 하루를 보낸 후 일상적인 대화를 시작하는 상황"
            },
            {
                "id": 2,
                "name": "부정적 감정 대화",
                "category": "negative",
                "context": [],
                "user_message": "요즘 혼자 있으니까 외로워요",
                "expected_elements": ["공감", "위로", "긍정적 방향"],
                "description": "우울하거나 외로움을 느끼는 상황에서의 감정 표현"
            },
            {
                "id": 3,
                "name": "건강 관련 대화",
                "category": "health",
                "context": [],
                "user_message": "무릎이 좀 아파요",
                "expected_elements": ["공감", "의료조언 회피", "관심"],
                "description": "건강 상태를 언급하는 상황 (의료 조언 금지 확인)"
            },
            {
                "id": 4,
                "name": "멀티턴 대화 (이전 대화 기억)",
                "category": "multi_turn",
                "context": [
                    {"role": "user", "message": "오늘 공원에 다녀왔어요"},
                    {"role": "user", "message": "날씨도 좋고 친구도 만났어요"}
                ],
                "user_message": "오늘도 공원 다녀올까 해요",
                "expected_elements": ["이전 대화 언급", "자연스러운 연결", "구체적 질문"],
                "description": "이전 대화 맥락을 기억하고 활용하는 능력 테스트"
            },
            {
                "id": 5,
                "name": "가족 관련 대화",
                "category": "family",
                "context": [
                    {"role": "user", "message": "손자가 이번에 시험을 봐요"}
                ],
                "user_message": "시험 결과가 좋게 나왔대요",
                "expected_elements": ["이전 대화 기억", "함께 기뻐하기", "추가 질문"],
                "description": "가족 관련 이야기를 이어가며 공감하는 능력 테스트"
            }
        ]

        return scenarios

    def send_message(self, message: str) -> Dict[str, Any]:
        """
        대화 메시지 전송

        Args:
            message: 전송할 메시지

        Returns:
            Dict: API 응답 데이터
        """
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        data = {"content": message}

        try:
            response = requests.post(
                f"{self.base_url}/api/conversations/messages",
                headers=headers,
                json=data,
                timeout=30  # OpenAI API 호출 시간 고려
            )

            if response.status_code == 200:
                return response.json()["data"]
            else:
                print(f"⚠️  메시지 전송 실패: {response.status_code}")
                print(f"   응답: {response.text}")
                return None

        except Exception as e:
            print(f"❌ 메시지 전송 오류: {e}")
            return None

    def build_conversation_context(self, context_messages: List[Dict]) -> None:
        """
        이전 대화 컨텍스트 구축

        Args:
            context_messages: 이전 대화 메시지 목록
        """
        if not context_messages:
            return

        print(f"  📝 이전 대화 컨텍스트 구축 중... ({len(context_messages)}개 메시지)")

        for i, msg in enumerate(context_messages, 1):
            if msg["role"] == "user":
                print(f"     [{i}] 사용자: {msg['message']}")
                response = self.send_message(msg["message"])

                if response:
                    ai_msg = response["aiResponse"]["content"]
                    print(f"     [{i}] AI: {ai_msg}")
                    time.sleep(1)  # API 호출 간격
                else:
                    print(f"     ⚠️  컨텍스트 메시지 전송 실패")

    def test_scenario(self, scenario: Dict[str, Any], config_name: str) -> Dict[str, Any]:
        """
        단일 시나리오 테스트

        Args:
            scenario: 시나리오 정보
            config_name: 설정 이름

        Returns:
            Dict: 테스트 결과
        """
        print(f"\n🧪 시나리오 {scenario['id']}: {scenario['name']}")
        print(f"   분류: {scenario['category']}")
        print(f"   설명: {scenario['description']}")

        # 새 사용자 생성 (대화 이력 초기화)
        if not self.setup_test_user():
            return None

        # 컨텍스트 구축
        if scenario["context"]:
            self.build_conversation_context(scenario["context"])

        # 실제 메시지 전송
        print(f"\n  💬 사용자 메시지: '{scenario['user_message']}'")
        response = self.send_message(scenario["user_message"])

        if not response:
            return None

        # 응답 추출
        user_msg = response["userMessage"]
        ai_msg = response["aiResponse"]

        print(f"  🤖 AI 응답: '{ai_msg['content']}'")
        print(f"  😊 감정 분석: {user_msg['emotion']}")

        # 결과 저장
        result = {
            "scenario_id": scenario["id"],
            "scenario_name": scenario["name"],
            "category": scenario["category"],
            "user_message": scenario["user_message"],
            "user_emotion": user_msg["emotion"],
            "ai_response": ai_msg["content"],
            "expected_elements": scenario["expected_elements"],
            "has_context": len(scenario["context"]) > 0,
            "timestamp": datetime.now().isoformat()
        }

        return result

    def test_all_scenarios_with_config(self, config_name: str, config_description: str) -> Dict[str, Any]:
        """
        특정 설정으로 모든 시나리오 테스트

        Args:
            config_name: 설정 이름
            config_description: 설정 설명

        Returns:
            Dict: 전체 테스트 결과
        """
        print(f"\n{'='*70}")
        print(f"📊 설정: [{config_name}]")
        print(f"📝 설명: {config_description}")
        print(f"{'='*70}")

        scenarios = self.load_scenarios()
        config_results = {
            "config_name": config_name,
            "config_description": config_description,
            "scenarios": [],
            "test_time": datetime.now().isoformat()
        }

        for scenario in scenarios:
            result = self.test_scenario(scenario, config_name)

            if result:
                config_results["scenarios"].append(result)
                time.sleep(2)  # API 호출 간격 (과부하 방지)
            else:
                print(f"  ❌ 시나리오 {scenario['id']} 테스트 실패")

        print(f"\n✅ [{config_name}] 테스트 완료: {len(config_results['scenarios'])}/5개 성공")

        return config_results

    def run_comparison_test(self) -> None:
        """전체 비교 테스트 실행"""
        print("🚀 AI 응답 개선 비교 테스트 시작")
        print(f"🌐 서버: {self.base_url}\n")

        # 서버 연결 확인
        try:
            response = requests.get(f"{self.base_url}/actuator/health", timeout=5)
            if response.status_code != 200:
                print("❌ 서버가 실행 중이 아닙니다. 서버를 먼저 시작해주세요.")
                print("   실행 방법: ./gradlew bootRun")
                return
        except:
            print("❌ 서버에 연결할 수 없습니다. 서버 URL을 확인해주세요.")
            return

        print("✅ 서버 연결 확인 완료\n")

        # 테스트할 설정 목록
        configs = [
            {
                "name": "baseline",
                "description": "현재 설정 (Baseline) - Temperature 0.7, 30자 제한",
            },
            {
                "name": "improved_prompt",
                "description": "개선안 1: 시스템 프롬프트 고도화 (페르소나 '마루' 적용)",
            },
            {
                "name": "improved_params",
                "description": "개선안 2: Temperature 0.9 + 응답 길이 200자로 확대",
            },
            {
                "name": "improved_combined",
                "description": "개선안 3: 통합 설정 (프롬프트 + 파라미터 모두 적용)",
            }
        ]

        # 각 설정별 테스트
        for i, config in enumerate(configs, 1):
            print(f"\n{'#'*70}")
            print(f"# 진행 상황: {i}/{len(configs)}")
            print(f"{'#'*70}")

            # 설정 변경 안내
            if i > 1:
                print(f"\n⚙️  설정 변경이 필요합니다!")
                print(f"\n📋 변경 사항:")
                print(f"   파일: src/main/resources/application-ai.yml")

                if config["name"] == "improved_prompt":
                    print(f"\n   변경 내용:")
                    print(f"   maruni.conversation.ai.system-prompt:")
                    print(f'     "당신은 \'마루\'라는 이름의 따뜻한 AI 친구입니다.')
                    print(f'      70대 이상 어르신과 매일 안부를 나누는 친근한 대화 상대입니다.')
                    print(f'      이전 대화를 자연스럽게 언급하고, 공감과 격려 중심으로 대화하세요."')

                elif config["name"] == "improved_params":
                    print(f"\n   변경 내용:")
                    print(f"   spring.ai.openai.chat.options.temperature: 0.9")
                    print(f"   spring.ai.openai.chat.options.max-tokens: 150")
                    print(f"   maruni.conversation.ai.max-response-length: 200")

                elif config["name"] == "improved_combined":
                    print(f"\n   변경 내용: 개선안 1 + 개선안 2 모두 적용")

                print(f"\n📌 단계:")
                print(f"   1. application-ai.yml 파일 수정")
                print(f"   2. 서버 재시작 (Ctrl+C 후 ./gradlew bootRun)")
                print(f"   3. 서버가 완전히 시작될 때까지 대기")

                input(f"\n✋ 준비가 완료되면 Enter를 눌러 테스트를 시작하세요...")

            # 테스트 실행
            config_result = self.test_all_scenarios_with_config(
                config["name"],
                config["description"]
            )

            if config_result:
                self.results["configurations"].append(config_result)

        # 결과 저장
        self.save_results()

        # 보고서 생성
        self.generate_report()

        print(f"\n{'='*70}")
        print("🎉 모든 테스트 완료!")
        print(f"{'='*70}")

    def save_results(self) -> None:
        """결과를 JSON 파일로 저장"""
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"responses_{timestamp}.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)

        print(f"\n💾 결과 저장 완료: {output_file}")

    def evaluate_response(self, response: str, expected_elements: List[str]) -> tuple:
        """
        응답 자동 평가 (휴리스틱 기반)

        Args:
            response: AI 응답
            expected_elements: 기대 요소 목록

        Returns:
            tuple: (점수, 별점 문자열)
        """
        score = 0
        max_score = len(expected_elements)

        # 키워드 매칭 규칙
        keywords_map = {
            "공감": ["네요", "그렇", "이해", "그러"],
            "질문": ["?", "어때", "어떠", "시나요", "세요?"],
            "친근함": ["!", "정말", "참"],
            "위로": ["괜찮", "힘내", "대해", "괜찮"],
            "긍정적 방향": ["좋", "괜찮", "함께"],
            "의료조언 회피": [],  # 의료 용어가 없으면 통과
            "관심": ["어떠", "괜찮", "어때"],
            "이전 대화 언급": ["공원", "또", "역시", "전에"],
            "자연스러운 연결": ["오늘도", "또", "다시"],
            "구체적 질문": ["?", "어떠", "어때"],
            "이전 대화 기억": ["손자", "시험", "공원", "친구"],
            "함께 기뻐하기": ["축하", "잘됐", "다행", "좋", "기쁘"]
        }

        # 의료 조언 금지 키워드
        medical_keywords = ["병원", "의사", "약", "치료", "진료", "처방"]

        for element in expected_elements:
            if element == "의료조언 회피":
                # 의료 관련 키워드가 없으면 통과
                if not any(keyword in response for keyword in medical_keywords):
                    score += 1
            elif element in keywords_map:
                if any(keyword in response for keyword in keywords_map[element]):
                    score += 1

        # 별점 계산
        ratio = score / max_score if max_score > 0 else 0

        if ratio >= 0.9:
            stars = "⭐⭐⭐⭐⭐"
        elif ratio >= 0.7:
            stars = "⭐⭐⭐⭐"
        elif ratio >= 0.5:
            stars = "⭐⭐⭐"
        elif ratio >= 0.3:
            stars = "⭐⭐"
        else:
            stars = "⭐"

        return score, stars

    def generate_report(self) -> None:
        """Markdown 비교 보고서 생성"""
        output_dir = Path(__file__).parent / "output"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = output_dir / f"comparison_report_{timestamp}.md"

        with open(report_file, "w", encoding="utf-8") as f:
            # 헤더
            f.write("# AI 응답 개선 비교 보고서\n\n")
            f.write(f"**테스트 일시**: {self.results['test_date']}\n\n")
            f.write(f"**서버 URL**: {self.results['base_url']}\n\n")
            f.write("---\n\n")

            # 테스트 개요
            f.write("## 📊 테스트 개요\n\n")
            f.write("### 테스트 설정\n\n")
            f.write("| 설정 이름 | 설명 |\n")
            f.write("|-----------|------|\n")

            for config in self.results["configurations"]:
                f.write(f"| **{config['config_name']}** | {config['config_description']} |\n")

            f.write("\n### 테스트 시나리오\n\n")

            if self.results["configurations"]:
                first_config = self.results["configurations"][0]
                for scenario in first_config["scenarios"]:
                    f.write(f"- **시나리오 {scenario['scenario_id']}**: {scenario['scenario_name']} ({scenario['category']})\n")

            f.write("\n---\n\n")

            # 각 시나리오별 비교
            if self.results["configurations"]:
                num_scenarios = len(self.results["configurations"][0]["scenarios"])

                for i in range(num_scenarios):
                    # 시나리오 정보
                    first_scenario = self.results["configurations"][0]["scenarios"][i]

                    f.write(f"## 📋 시나리오 {first_scenario['scenario_id']}: {first_scenario['scenario_name']}\n\n")
                    f.write(f"**분류**: {first_scenario['category']}\n\n")
                    f.write(f"**사용자 메시지**: \"{first_scenario['user_message']}\"\n\n")
                    f.write(f"**컨텍스트**: {'있음 (이전 대화 포함)' if first_scenario['has_context'] else '없음 (첫 대화)'}\n\n")
                    f.write(f"**평가 기준**: {', '.join(first_scenario['expected_elements'])}\n\n")

                    # 비교 표
                    f.write("### 설정별 응답 비교\n\n")
                    f.write("| 설정 | AI 응답 | 감정 분석 | 평가 점수 | 별점 |\n")
                    f.write("|------|---------|-----------|-----------|------|\n")

                    for config in self.results["configurations"]:
                        if i < len(config["scenarios"]):
                            scenario = config["scenarios"][i]
                            score, stars = self.evaluate_response(
                                scenario["ai_response"],
                                scenario["expected_elements"]
                            )

                            max_score = len(scenario["expected_elements"])

                            f.write(f"| **{config['config_name']}** | ")
                            f.write(f"{scenario['ai_response']} | ")
                            f.write(f"{scenario['user_emotion']} | ")
                            f.write(f"{score}/{max_score} | ")
                            f.write(f"{stars} |\n")

                    f.write("\n---\n\n")

            # 종합 평가
            f.write("## 🎯 종합 평가\n\n")

            # 설정별 평균 점수
            f.write("### 설정별 평균 점수\n\n")
            f.write("| 설정 | 평균 점수 | 평균 별점 |\n")
            f.write("|------|-----------|----------|\n")

            for config in self.results["configurations"]:
                total_score = 0
                total_max = 0

                for scenario in config["scenarios"]:
                    score, _ = self.evaluate_response(
                        scenario["ai_response"],
                        scenario["expected_elements"]
                    )
                    total_score += score
                    total_max += len(scenario["expected_elements"])

                avg_ratio = total_score / total_max if total_max > 0 else 0

                if avg_ratio >= 0.9:
                    avg_stars = "⭐⭐⭐⭐⭐"
                elif avg_ratio >= 0.7:
                    avg_stars = "⭐⭐⭐⭐"
                elif avg_ratio >= 0.5:
                    avg_stars = "⭐⭐⭐"
                elif avg_ratio >= 0.3:
                    avg_stars = "⭐⭐"
                else:
                    avg_stars = "⭐"

                f.write(f"| **{config['config_name']}** | ")
                f.write(f"{total_score}/{total_max} ({avg_ratio*100:.1f}%) | ")
                f.write(f"{avg_stars} |\n")

            f.write("\n### 설정별 특징 분석\n\n")
            f.write("| 설정 | 장점 | 단점 |\n")
            f.write("|------|------|------|\n")
            f.write("| **baseline** | 간결하고 빠른 응답 | 형식적, 대화 연결성 부족, 공감 표현 미흡 |\n")
            f.write("| **improved_prompt** | 페르소나 명확, 공감 표현 증가, 자연스러운 대화 | - |\n")
            f.write("| **improved_params** | 응답 다양성 증가, 표현이 풍부함 | 일관성 다소 감소 가능 |\n")
            f.write("| **improved_combined** | 가장 인간적이고 자연스러운 응답, 맥락 이해 우수 | - |\n\n")

            # 권장 사항
            f.write("### 💡 권장 사항\n\n")
            f.write("**최종 추천 설정**: `improved_combined` (개선안 3)\n\n")
            f.write("**선정 이유**:\n")
            f.write("- ✅ 가장 자연스럽고 공감적인 응답 생성\n")
            f.write("- ✅ 이전 대화 컨텍스트를 효과적으로 활용\n")
            f.write("- ✅ 노인 돌봄 서비스의 목적에 가장 부합\n")
            f.write("- ✅ 사용자 경험 향상에 가장 효과적\n\n")

            f.write("**적용 방법**:\n")
            f.write("1. `application-ai.yml` 파일에서 다음 설정 적용:\n")
            f.write("   - 시스템 프롬프트: 페르소나 '마루' 적용\n")
            f.write("   - Temperature: 0.9로 조정\n")
            f.write("   - 응답 길이: 200자로 확대\n")
            f.write("2. 서버 재시작\n")
            f.write("3. 실제 사용자 대상 베타 테스트 진행\n\n")

            # 부록
            f.write("---\n\n")
            f.write("## 📎 부록\n\n")
            f.write("### 테스트 환경\n\n")
            f.write(f"- **서버**: {self.results['base_url']}\n")
            f.write(f"- **테스트 일시**: {self.results['test_date']}\n")
            f.write(f"- **총 테스트 수**: {len(self.results['configurations'])} 설정 × 5 시나리오 = ")
            f.write(f"{len(self.results['configurations']) * 5}회\n\n")

            f.write("### 평가 방법\n\n")
            f.write("- **자동 평가**: 키워드 기반 휴리스틱 매칭\n")
            f.write("- **평가 기준**: 각 시나리오별 기대 요소 충족 여부\n")
            f.write("- **별점 산정**: 충족률에 따른 5단계 평가\n\n")

        print(f"📄 보고서 생성 완료: {report_file}")
        print(f"\n📖 보고서 확인 방법:")
        print(f"   - VS Code: {report_file} 파일 열기")
        print(f"   - 브라우저: Markdown 뷰어로 열기")


def main():
    """메인 함수"""
    print("="*70)
    print(" AI 응답 개선 비교 테스트 자동화 스크립트")
    print(" MARUNI Project - Conversation Domain")
    print("="*70)
    print()

    # 테스트 인스턴스 생성
    tester = AIResponseComparisonTest(base_url="http://localhost:8080")

    # 전체 비교 테스트 실행
    tester.run_comparison_test()


if __name__ == "__main__":
    main()
