from telegram import Update
from telegram.ext import ContextTypes
from db.connection import get_pool
from bot.services.referral import get_referrals_count

async def profile_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user:
        return
    pool = await get_pool()
    row = await pool.fetchrow('SELECT * FROM users WHERE id = $1', user.id)
    if not row:
        await update.message.reply_text('Вы ещё не зарегистрированы. Отправьте /start.')
        return
    referrals = await get_referrals_count(user.id, pool)
    text = (
        f'👤 Профиль\n'
        f'ID: {row["id"]}\n'
        f'Имя: {row["first_name"] or "-"} {row["last_name"] or ""}\n'
        f'Юзернейм: @{row["username"] if row["username"] else "-"}\n'
        f'\nУровень: {row["level"]}\n'
        f'Очки: {row["points"]}\n'
        f'Рефералов: {referrals}\n'
        f'Ссылка проекта: {row["project_link"] or "не указана"}\n'
    )
    await update.message.reply_text(text)
