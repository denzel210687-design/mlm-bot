import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from db.connection import get_pool
from bot.middleware.register import register_user
from bot.services.variables import render_text
from config import BOT_USERNAME

START_TEXT = (
    "👋 Привет! Добро пожаловать в MLM Bot Manager.\n\n"
    "Используй меню, чтобы изучить возможности проекта, добавить ссылку и посмотреть команду."
)

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user:
        return
    referrer_id = None
    if context.args:
        raw = context.args[0]
        match = re.match(r"^(\d+)$", raw)
        if match:
            referrer_id = int(match.group(1))
    await register_user(user, referrer_id)
    welcome_text = await render_text(START_TEXT, {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'project_link': None,
        'points': 0,
        'level': 1,
        'joined_at': user.first_name,
    })
    buttons = [
        [InlineKeyboardButton('📋 Меню', callback_data='MENU|root')],
        [InlineKeyboardButton('👤 Профиль', callback_data='ACTION|profile')],
        [InlineKeyboardButton('🧭 Рефералы', callback_data='ACTION|refs')],
    ]
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(buttons))
