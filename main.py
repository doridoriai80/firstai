from rule_engine import get_rule_response
from llm_api import get_llm_response
from conversation_manager import ConversationManager
import json

def print_conversation_history(conversation_manager):
    """대화 기록 출력"""
    messages = conversation_manager.get_recent_messages(20)  # 최근 20개
    if not messages:
        print("대화 기록이 없습니다.")
        return
    
    print("\n=== 대화 기록 ===")
    for i, message in enumerate(messages, 1):
        role = "사용자" if message["role"] == "user" else "봇"
        timestamp = message["timestamp"][:19]  # 초까지 표시
        source = f"({message['source']})" if message.get("source") else ""
        
        print(f"{i}. [{timestamp}] {role}{source}: {message['content']}")
        
        if message.get("response_time"):
            print(f"   응답시간: {message['response_time']:.2f}초")
        print()

def print_conversation_summary(conversation_manager):
    """대화 요약 출력"""
    summary = conversation_manager.get_conversation_summary()
    
    print("\n=== 대화 요약 ===")
    print(f"세션 ID: {summary['session_id']}")
    print(f"총 메시지 수: {summary['total_messages']}")
    print(f"사용자 메시지: {summary['user_messages']}")
    print(f"봇 메시지: {summary['assistant_messages']}")
    print(f"대화 시간: {summary['duration_seconds']:.1f}초")
    print(f"평균 응답 시간: {summary['avg_response_time']:.2f}초")
    print(f"시작 시간: {summary['start_time']}")
    print(f"종료 시간: {summary['end_time']}")

def search_messages(conversation_manager, keyword):
    """메시지 검색"""
    results = conversation_manager.search_messages(keyword)
    
    if not results:
        print(f"'{keyword}'와 관련된 메시지를 찾을 수 없습니다.")
        return
    
    print(f"\n=== '{keyword}' 검색 결과 ===")
    for i, message in enumerate(results, 1):
        role = "사용자" if message["role"] == "user" else "봇"
        timestamp = message["timestamp"][:19]
        print(f"{i}. [{timestamp}] {role}: {message['content']}")

def show_available_sessions(conversation_manager):
    """사용 가능한 세션 목록 표시"""
    sessions = conversation_manager.get_available_sessions()
    
    if not sessions:
        print("저장된 세션이 없습니다.")
        return
    
    print("\n=== 사용 가능한 세션 ===")
    for i, session_id in enumerate(sessions[:10], 1):  # 최근 10개만 표시
        print(f"{i}. {session_id}")

def chatbot():
    print("챗봇을 시작합니다. '종료'를 입력하면 끝납니다.")
    print("특별 명령어: '히스토리', '요약', '검색 [키워드]', '초기화', '도움말'")
    
    # 대화 히스토리 관리자 초기화
    conversation_manager = ConversationManager(max_history=100, save_to_file=True)
    
    while True:
        user_input = input("You: ")
        
        if user_input == "종료":
            print("대화를 종료합니다. 대화 기록이 저장되었습니다.")
            break
        
        # 특별 명령어 처리
        if user_input == "히스토리":
            print_conversation_history(conversation_manager)
            continue
        elif user_input == "요약":
            print_conversation_summary(conversation_manager)
            continue
        elif user_input.startswith("검색 "):
            keyword = user_input[3:].strip()
            if keyword:
                search_messages(conversation_manager, keyword)
            else:
                print("검색할 키워드를 입력해주세요. 예: '검색 안녕'")
            continue
        elif user_input == "초기화":
            conversation_manager.clear_history()
            print("대화 기록이 초기화되었습니다.")
            continue
        elif user_input == "도움말":
            print("사용 가능한 명령어:")
            print("- '히스토리': 대화 기록 보기")
            print("- '요약': 대화 요약 보기")
            print("- '검색 [키워드]': 메시지 검색")
            print("- '초기화': 대화 기록 삭제")
            print("- '종료': 프로그램 종료")
            continue
        
        # 1단계: 룰 엔진 먼저 시도
        response = get_rule_response(user_input, conversation_manager)
        
        # 2단계: 룰이 없으면 LLM 호출
        if not response:
            response = get_llm_response(user_input, conversation_manager)
        
        print("Bot:", response)

if __name__ == "__main__":
    chatbot()
