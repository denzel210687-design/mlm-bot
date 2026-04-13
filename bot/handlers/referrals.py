from telegram import Update
from telegram.ext import ContextTypes
from db.connection import get_pool
from bot.services.referral import get_tree, get_stats

async def referrals_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user:
        return
    pool = await get_pool()
    stats = await get_stats(user.id, pool)
    tree = await get_tree(user.id, pool)
    text = [
        f'🌱 Статистика рефералов:',
        f'Всего: {stats["total"]}',
        f'Уровень 1: {stats["level_1"]}',
        f'Уровень 2: {stats["level_2"]}',
        f'Уровень 3: {stats["level_3"]}',
        f'Глубже: {stats["deeper"]}',
        f'За 7 дней: {stats["week"]}',
        f'За 24 часа: {stats["today"]}',
        '\n👥 Дерево рефералов:',
    ]
    for depth, nodes in tree.items():
        text.append(f'Уровень {depth} ({len(nodes)}):')
        for item in nodes[:10]:
            text.append(f'- {item["first_name"] or "-"} @{item["username"] or "-"}')
    if not tree:
        text.append('Пока нет рефералов.')
    await update.message.reply_text('\n'.join(text))
