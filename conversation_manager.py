import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class ConversationManager:
    def __init__(self, max_history: int = 50, save_to_file: bool = True):
        """
        대화 히스토리를 관리하는 클래스
        
        Args:
            max_history: 저장할 최대 대화 개수
            save_to_file: 파일에 저장할지 여부
        """
        self.max_history = max_history
        self.save_to_file = save_to_file
        self.conversation_history: List[Dict] = []
        self.session_id = self._generate_session_id()
        
        # 저장 디렉토리 생성
        self.history_dir = "conversation_history"
        if not os.path.exists(self.history_dir):
            os.makedirs(self.history_dir)
    
    def _generate_session_id(self) -> str:
        """세션 ID 생성"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def add_message(self, role: str, content: str, response_time: float = None, 
                   source: str = "user") -> None:
        """
        대화 메시지 추가
        
        Args:
            role: "user" 또는 "assistant"
            content: 메시지 내용
            response_time: 응답 시간 (초)
            source: 메시지 출처 ("rule_engine", "llm_api" 등)
        """
        message = {
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "content": content,
            "response_time": response_time,
            "source": source
        }
        
        self.conversation_history.append(message)
        
        # 최대 개수 제한
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)
        
        # 파일에 저장
        if self.save_to_file:
            self._save_to_file()
    
    def get_recent_messages(self, count: int = 10) -> List[Dict]:
        """최근 메시지들 반환"""
        return self.conversation_history[-count:]
    
    def get_context_for_llm(self, max_tokens: int = 1000) -> List[Dict]:
        """
        LLM에 전달할 컨텍스트 생성
        OpenAI API 형식에 맞춰 반환
        """
        context_messages = []
        total_tokens = 0
        
        # 최근 메시지부터 역순으로 처리
        for message in reversed(self.conversation_history):
            # 간단한 토큰 계산 (실제로는 tiktoken 라이브러리 사용 권장)
            estimated_tokens = len(message["content"]) // 4
            
            if total_tokens + estimated_tokens > max_tokens:
                break
                
            context_messages.insert(0, {
                "role": message["role"],
                "content": message["content"]
            })
            total_tokens += estimated_tokens
        
        return context_messages
    
    def get_conversation_summary(self) -> Dict:
        """대화 요약 정보 반환"""
        if not self.conversation_history:
            return {"total_messages": 0, "duration": 0}
        
        start_time = datetime.fromisoformat(self.conversation_history[0]["timestamp"])
        end_time = datetime.fromisoformat(self.conversation_history[-1]["timestamp"])
        duration = (end_time - start_time).total_seconds()
        
        user_messages = [msg for msg in self.conversation_history if msg["role"] == "user"]
        assistant_messages = [msg for msg in self.conversation_history if msg["role"] == "assistant"]
        
        avg_response_time = 0
        if assistant_messages:
            response_times = [msg.get("response_time", 0) for msg in assistant_messages if msg.get("response_time")]
            if response_times:
                avg_response_time = sum(response_times) / len(response_times)
        
        return {
            "session_id": self.session_id,
            "total_messages": len(self.conversation_history),
            "user_messages": len(user_messages),
            "assistant_messages": len(assistant_messages),
            "duration_seconds": duration,
            "avg_response_time": avg_response_time,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat()
        }
    
    def search_messages(self, keyword: str) -> List[Dict]:
        """키워드로 메시지 검색"""
        results = []
        for message in self.conversation_history:
            if keyword.lower() in message["content"].lower():
                results.append(message)
        return results
    
    def clear_history(self) -> None:
        """대화 히스토리 초기화"""
        self.conversation_history.clear()
        self.session_id = self._generate_session_id()
    
    def _save_to_file(self) -> None:
        """대화 히스토리를 파일에 저장"""
        filename = f"{self.history_dir}/conversation_{self.session_id}.json"
        
        data = {
            "session_id": self.session_id,
            "conversation_history": self.conversation_history,
            "summary": self.get_conversation_summary()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_from_file(self, session_id: str) -> bool:
        """파일에서 대화 히스토리 로드"""
        filename = f"{self.history_dir}/conversation_{session_id}.json"
        
        if not os.path.exists(filename):
            return False
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.session_id = data["session_id"]
            self.conversation_history = data["conversation_history"]
            return True
        except Exception as e:
            print(f"파일 로드 중 오류 발생: {e}")
            return False
    
    def get_available_sessions(self) -> List[str]:
        """사용 가능한 세션 목록 반환"""
        sessions = []
        for filename in os.listdir(self.history_dir):
            if filename.startswith("conversation_") and filename.endswith(".json"):
                session_id = filename.replace("conversation_", "").replace(".json", "")
                sessions.append(session_id)
        return sorted(sessions, reverse=True)
