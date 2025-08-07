from openai import OpenAI
from config import OPENAI_API_KEY
import os

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=OPENAI_API_KEY)

def get_llm_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"API 호출 중 오류 발생: {e}")
        return "죄송합니다. 응답을 생성하는 중 오류가 발생했습니다."