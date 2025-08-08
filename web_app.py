from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import json
import os
from datetime import datetime
from rule_engine import get_rule_response
from llm_api import get_llm_response
from conversation_manager import ConversationManager

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # 실제 운영시에는 환경변수로 설정
CORS(app)

# 전역 대화 히스토리 관리자 (실제 운영시에는 데이터베이스 사용 권장)
conversation_managers = {}

@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """챗봇 API 엔드포인트"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        # 세션별 대화 히스토리 관리자 생성
        if session_id not in conversation_managers:
            conversation_managers[session_id] = ConversationManager(max_history=100, save_to_file=True)
        
        conversation_manager = conversation_managers[session_id]
        
        # 특별 명령어 처리
        if user_message == "히스토리":
            messages = conversation_manager.get_recent_messages(20)
            return jsonify({
                'response': '대화 기록을 보여드리겠습니다.',
                'history': messages,
                'type': 'history'
            })
        elif user_message == "요약":
            summary = conversation_manager.get_conversation_summary()
            return jsonify({
                'response': '대화 요약을 보여드리겠습니다.',
                'summary': summary,
                'type': 'summary'
            })
        elif user_message.startswith("검색 "):
            keyword = user_message[3:].strip()
            if keyword:
                results = conversation_manager.search_messages(keyword)
                return jsonify({
                    'response': f"'{keyword}' 검색 결과입니다.",
                    'search_results': results,
                    'type': 'search'
                })
            else:
                return jsonify({
                    'response': '검색할 키워드를 입력해주세요. 예: "검색 안녕"',
                    'type': 'error'
                })
        elif user_message == "초기화":
            conversation_manager.clear_history()
            return jsonify({
                'response': '대화 기록이 초기화되었습니다.',
                'type': 'clear'
            })
        elif user_message == "도움말":
            help_text = """사용 가능한 명령어:
• '히스토리': 대화 기록 보기
• '요약': 대화 요약 보기  
• '검색 [키워드]': 메시지 검색
• '초기화': 대화 기록 삭제"""
            return jsonify({
                'response': help_text,
                'type': 'help'
            })
        
        # 일반 대화 처리
        # 1단계: 룰 엔진 먼저 시도
        response = get_rule_response(user_message, conversation_manager)
        
        # 2단계: 룰이 없으면 LLM 호출
        if not response:
            response = get_llm_response(user_message, conversation_manager)
        
        return jsonify({
            'response': response,
            'type': 'normal'
        })
        
    except Exception as e:
        return jsonify({
            'response': f'오류가 발생했습니다: {str(e)}',
            'type': 'error'
        }), 500

@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    """사용 가능한 세션 목록 반환"""
    try:
        # 기본 세션 관리자에서 사용 가능한 세션 가져오기
        default_manager = ConversationManager()
        sessions = default_manager.get_available_sessions()
        return jsonify({'sessions': sessions})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/load-session', methods=['POST'])
def load_session():
    """특정 세션 로드"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        
        if not session_id:
            return jsonify({'error': '세션 ID가 필요합니다.'}), 400
        
        # 새 대화 히스토리 관리자 생성
        conversation_manager = ConversationManager()
        if conversation_manager.load_from_file(session_id):
            conversation_managers[session_id] = conversation_manager
            messages = conversation_manager.get_recent_messages(50)
            return jsonify({
                'success': True,
                'messages': messages,
                'session_id': session_id
            })
        else:
            return jsonify({'error': '세션을 찾을 수 없습니다.'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # templates 폴더가 없으면 생성
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    app.run(debug=True, host='0.0.0.0', port=8080)
