from openai import AsyncOpenAI
from config import OPENAI_API_KEY

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

MLM_SYSTEM_PROMPT = """Ты — ИИ-наставник в MLM. Твоя задача:
- Помогать партнёрам разобраться в системе FulEnergy
- Отвечать на вопросы о продукте, регистрации, реферальной системе
- Помогать с возражениями и рекрутингом
- Мотивировать и поддерживать команду
- Отвечать кратко, дружелюбно и по делу
- Всегда предлагать следующий шаг

Если не знаешь ответа — предложи обратиться к куратору."""

async def create_ai_answer(user_id: int, prompt: str) -> str:
    response = await client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': MLM_SYSTEM_PROMPT},
            {'role': 'user', 'content': prompt},
        ],
        max_tokens=500,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()