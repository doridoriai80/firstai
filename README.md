# Rule + LLM 기반 AI Chatbot

## 소개
이 프로젝트는 간단한 규칙 기반 응답과 LLM API(OpenAI GPT)를 결합한 AI 챗봇입니다.

## 구성
- 규칙 기반 응답 (`rule_engine.py`)
- OpenAI API를 통한 LLM 연동 (`llm_api.py`)
- 메인 실행 (`main.py`)

## 환경설정 및 의존성 설치
1. (선택) 가상환경 생성 및 활성화
   ```bash
   python -m venv chatbot-env
   source chatbot-env/bin/activate
   ```
2. 필수 패키지 설치
   ```bash
   pip install openai
   ```
3. OpenAI API 키 설정
   - `config.py` 파일의 `OPENAI_API_KEY`에 본인의 OpenAI API 키를 입력하세요.
   - 예시:
     ```python
     OPENAI_API_KEY = "sk-..."
     ```
4. 가상환경 종료
   ```bash
    deactivate
   ```

## 실행 방법
1. `config.py`에 OpenAI API 키 입력
2. `python main.py` 실행

## 향후 개선 아이디어
- GUI 인터페이스 추가
- 사용자 입력 로그 저장
- 챗봇 성능 평가

