#!/usr/bin/env python3
"""
대화 히스토리 관리 기능 테스트
"""

from conversation_manager import ConversationManager
import time

def test_conversation_manager():
    """대화 히스토리 관리자 테스트"""
    print("=== 대화 히스토리 관리자 테스트 ===\n")
    
    # 대화 히스토리 관리자 초기화
    cm = ConversationManager(max_history=10, save_to_file=True)
    
    # 테스트 대화 추가
    test_conversations = [
        ("안녕하세요", "안녕하세요! 무엇을 도와드릴까요?"),
        ("날씨는 어때요?", "오늘의 날씨는 맑음입니다."),
        ("시간이 궁금해요", "현재 시간은 14:30:25입니다."),
        ("파이썬이 뭔가요?", "파이썬은 프로그래밍 언어입니다."),
        ("감사합니다", "천만에요! 더 도움이 필요하시면 언제든 말씀해주세요.")
    ]
    
    print("테스트 대화를 추가합니다...")
    for user_msg, bot_msg in test_conversations:
        # 사용자 메시지 추가
        cm.add_message("user", user_msg, 0.1, "test")
        time.sleep(0.1)  # 실제 응답 시간 시뮬레이션
        
        # 봇 응답 추가
        cm.add_message("assistant", bot_msg, 0.2, "test")
        time.sleep(0.1)
    
    print(f"총 {len(cm.conversation_history)}개의 메시지가 추가되었습니다.\n")
    
    # 대화 요약 출력
    print("=== 대화 요약 ===")
    summary = cm.get_conversation_summary()
    for key, value in summary.items():
        print(f"{key}: {value}")
    print()
    
    # 최근 메시지 출력
    print("=== 최근 메시지 (최근 5개) ===")
    recent_messages = cm.get_recent_messages(5)
    for i, msg in enumerate(recent_messages, 1):
        role = "사용자" if msg["role"] == "user" else "봇"
        print(f"{i}. [{msg['timestamp'][:19]}] {role}: {msg['content']}")
    print()
    
    # 검색 테스트
    print("=== 검색 테스트 ===")
    search_results = cm.search_messages("날씨")
    print(f"'날씨' 검색 결과: {len(search_results)}개")
    for msg in search_results:
        role = "사용자" if msg["role"] == "user" else "봇"
        print(f"- {role}: {msg['content']}")
    print()
    
    # LLM 컨텍스트 테스트
    print("=== LLM 컨텍스트 테스트 ===")
    context = cm.get_context_for_llm(max_tokens=500)
    print(f"컨텍스트 메시지 수: {len(context)}")
    for i, msg in enumerate(context, 1):
        print(f"{i}. {msg['role']}: {msg['content'][:50]}...")
    print()
    
    print("테스트가 완료되었습니다!")

if __name__ == "__main__":
    test_conversation_manager()
