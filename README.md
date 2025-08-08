# Rule + LLM 기반 AI Chatbot

## 소개
이 프로젝트는 간단한 규칙 기반 응답과 LLM API(OpenAI GPT)를 결합한 AI 챗봇입니다.

## 구성
- 규칙 기반 응답 (`rule_engine.py`)
- OpenAI API를 통한 LLM 연동 (`llm_api.py`)
- 대화 히스토리 관리 (`conversation_manager.py`)
- 메인 실행 (`main.py`)

## 주요 기능
- **하이브리드 응답 시스템**: 규칙 기반 + LLM API
- **대화 히스토리 관리**: 모든 대화를 자동으로 저장하고 관리
- **대화 컨텍스트**: 이전 대화를 바탕으로 더 자연스러운 응답
- **대화 검색**: 키워드로 이전 대화 검색
- **대화 요약**: 대화 통계 및 요약 정보 제공
- **파일 저장**: 대화 기록을 JSON 파일로 자동 저장

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
4. 실행
   ```bash
   python main.py
   ```     
5. 가상환경 종료
   ```bash
   deactivate
   ```

## 실행 방법
1. `config.py`에 OpenAI API 키 입력
2. `python main.py` 실행

## 사용법

### 기본 대화
```
You: 안녕
Bot: 안녕하세요! 무엇을 도와드릴까요?

You: 날씨는 어때?
Bot: 오늘의 날씨는 맑음입니다.
```

### 특별 명령어
- `히스토리`: 최근 20개의 대화 기록을 보여줍니다
- `요약`: 현재 대화의 통계 정보를 보여줍니다
- `검색 [키워드]`: 키워드로 이전 대화를 검색합니다
- `초기화`: 현재 대화 기록을 삭제합니다
- `도움말`: 사용 가능한 명령어를 보여줍니다
- `종료`: 프로그램을 종료합니다

### 예시
```
You: 히스토리
=== 대화 기록 ===
1. [2024-01-15 14:30:25] 사용자: 안녕
2. [2024-01-15 14:30:25] 봇(rule_engine): 안녕하세요! 무엇을 도와드릴까요?

You: 요약
=== 대화 요약 ===
세션 ID: 20240115_143025
총 메시지 수: 2
사용자 메시지: 1
봇 메시지: 1
대화 시간: 0.0초
평균 응답 시간: 0.00초
```

## 파일 구조
```
firstai/
├── main.py                    # 메인 실행 파일
├── rule_engine.py            # 규칙 기반 응답 엔진
├── llm_api.py               # OpenAI API 연동
├── conversation_manager.py   # 대화 히스토리 관리
├── config.py                # 설정 파일
├── conversation_history/     # 대화 기록 저장 폴더
│   └── conversation_*.json  # 대화 기록 파일들
└── README.md               # 프로젝트 문서
```

## 향후 개선 아이디어
- GUI 인터페이스 추가
- 사용자 프로필 관리
- 감정 분석 기능
- 파일 업로드 및 분석
- 멀티모달 지원 (이미지, 음성)
- 실시간 협업 기능
- 성능 모니터링 및 로깅
