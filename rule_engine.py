import time
from conversation_manager import ConversationManager

def get_rule_response(user_input, conversation_manager: ConversationManager = None):
    """
    규칙 기반 응답 생성
    
    Args:
        user_input: 사용자 입력
        conversation_manager: 대화 히스토리 관리자 (선택사항)
    """
    start_time = time.time()
    
    rules = {
        "안녕": "안녕하세요! 무엇을 도와드릴까요?",
        "날씨": "오늘의 날씨는 맑음입니다.",
        "이름": "저는 AI 챗봇입니다.",
        "시간": f"현재 시간은 {time.strftime('%H:%M:%S')}입니다.",
        "도움말": "다음 명령어들을 사용할 수 있습니다:\n- '히스토리': 대화 기록 보기\n- '요약': 대화 요약 보기\n- '검색 [키워드]': 메시지 검색\n- '초기화': 대화 기록 삭제",
        "히스토리": "대화 기록을 보여드리겠습니다.",
        "요약": "대화 요약을 보여드리겠습니다.",
        "초기화": "대화 기록을 초기화하겠습니다."
    }
    
    for keyword, response in rules.items():
        if keyword in user_input:
            response_time = time.time() - start_time
            
            # 대화 히스토리에 추가
            if conversation_manager:
                conversation_manager.add_message("user", user_input, response_time, "rule_engine")
                conversation_manager.add_message("assistant", response, response_time, "rule_engine")
            
            return response
    
    return None
