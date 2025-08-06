import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def get_llm_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # 또는 gpt-4
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message['content']
