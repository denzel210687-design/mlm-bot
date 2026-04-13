import openai
from config import OPENAI_API_KEY
from db.connection import get_pool

openai.api_key = OPENAI_API_KEY

async def create_ai_answer(user_id: int, prompt: str):
    response = await openai.ChatCompletion.acreate(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': 'Ты помощник MLM-команды. Отвечай кратко и дружелюбно.'},
            {'role': 'user', 'content': prompt},
        ],
        max_tokens=500,
        temperature=0.7,
    )
    return response.choices[0].message['content'].strip()
