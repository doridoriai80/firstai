from rule_engine import get_rule_response
from llm_api import get_llm_response

def chatbot():
    print("챗봇을 시작합니다. '종료'를 입력하면 끝납니다.")
    while True:
        user_input = input("You: ")
        if user_input == "종료":
            break

        # 1단계: 룰 엔진 먼저 시도
        response = get_rule_response(user_input)

        # 2단계: 룰이 없으면 LLM 호출
        if not response:
            response = get_llm_response(user_input)

        print("Bot:", response)

if __name__ == "__main__":
    chatbot()
