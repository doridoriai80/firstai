def get_rule_response(user_input):
    rules = {
        "안녕": "안녕하세요! 무엇을 도와드릴까요?",
        "날씨": "오늘의 날씨는 맑음입니다.",
        "이름": "저는 AI 챗봇입니다.",
    }
    for keyword, response in rules.items():
        if keyword in user_input:
            return response
    return None
