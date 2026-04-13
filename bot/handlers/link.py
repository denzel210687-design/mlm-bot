from telegram import Update
from telegram.ext import ContextTypes
from config import PROJECT_LINK_MASK
from db.connection import get_pool
from bot.services.gamification import award_points

async def link_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user:
        return
    pool = await get_pool()
    if not context.args:
        row = await pool.fetchrow('SELECT project_link FROM users WHERE id = $1', user.id)
        link = row['project_link'] if row else None
        await update.message.reply_text(f'Ваша проектная ссылка: {link or "не указана"}')
        return
    project_link = context.args[0].strip()
    if PROJECT_LINK_MASK and not project_link.startswith(PROJECT_LINK_MASK):
        await update.message.reply_text(f'Ссылка должна начинаться с {PROJECT_LINK_MASK}')
        return
    await pool.execute('UPDATE users SET project_link = $1 WHERE id = $2', project_link, user.id)
    await pool.execute('INSERT INTO project_links (user_id, link, is_active) VALUES ($1, $2, true)', user.id, project_link)
    await award_points(user.id, 25, pool)
    await update.message.reply_text('Проектная ссылка сохранена и вы получили +25 очков!')
