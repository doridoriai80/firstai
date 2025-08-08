from openai import OpenAI
import time
from config import OPENAI_API_KEY
from conversation_manager import ConversationManager

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=OPENAI_API_KEY)

def get_llm_response(prompt, conversation_manager: ConversationManager = None):
    """
    LLM API를 통해 응답 생성
    
    Args:
        prompt: 사용자 입력
        conversation_manager: 대화 히스토리 관리자 (선택사항)
    """
    start_time = time.time()
    
    try:
        # 대화 히스토리가 있으면 컨텍스트로 사용
        if conversation_manager:
            context_messages = conversation_manager.get_context_for_llm()
            messages = context_messages + [{"role": "user", "content": prompt}]
        else:
            messages = [{"role": "user", "content": prompt}]
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # 또는 gpt-4
            messages=messages
        )
        
        response_content = response.choices[0].message.content
        response_time = time.time() - start_time
        
        # 대화 히스토리에 추가
        if conversation_manager:
            conversation_manager.add_message("user", prompt, response_time, "llm_api")
            conversation_manager.add_message("assistant", response_content, response_time, "llm_api")
        
        return response_content
        
    except Exception as e:
        print(f"LLM API 호출 중 오류 발생: {e}")
        return f"죄송합니다. 오류가 발생했습니다: {str(e)}"