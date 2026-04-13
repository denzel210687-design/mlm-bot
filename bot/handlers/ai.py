from telegram import Update
from telegram.ext import ContextTypes
from bot.services.ai import create_ai_answer

async def ai_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user:
        return
    prompt = ' '.join(context.args or [])
    if not prompt:
        await update.message.reply_text('Напишите /ai <вопрос>, чтобы получить ответ от AI.')
        return
    await update.message.reply_text('💬 Обрабатываю запрос...')
    try:
        answer = await create_ai_answer(user.id, prompt)
        await update.message.reply_text(answer)
    except Exception as exc:
        await update.message.reply_text('Ошибка AI. Попробуйте позже.')
