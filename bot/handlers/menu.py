import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from db.connection import get_pool
from bot.services.variables import render_text

async def build_buttons(buttons, user, referrer):
    keyboard = []
    for item in buttons or []:
        label = item.get('label')
        callback_type = item.get('type', 'menu')
        value = item.get('value', '')
        if callback_type == 'url':
            keyboard.append([InlineKeyboardButton(label, url=value)])
        elif callback_type == 'menu':
            keyboard.append([InlineKeyboardButton(label, callback_data=f'MENU|{value}')])
        else:
            keyboard.append([InlineKeyboardButton(label, callback_data=f'ACTION|{value}')])
    return InlineKeyboardMarkup(keyboard)

async def get_menu_items(parent_key, pool):
    if parent_key == 'root':
        rows = await pool.fetch("SELECT * FROM menu_items WHERE parent_key IS NULL AND is_active ORDER BY sort_order")
    else:
        rows = await pool.fetch("SELECT * FROM menu_items WHERE parent_key = $1 AND is_active ORDER BY sort_order", parent_key)
    return rows

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pool = await get_pool()
    items = await get_menu_items('root', pool)
    if not items:
        await update.message.reply_text('Меню пока пусто. Обратитесь к администратору.')
        return
    buttons = []
    for item in items:
        buttons.append([InlineKeyboardButton(item['title'], callback_data=f'MENU|{item["key"]}')])
    await update.message.reply_text('Выберите раздел:', reply_markup=InlineKeyboardMarkup(buttons))

async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data or ''
    if '|' not in data:
        return
    action, value = data.split('|', 1)
    pool = await get_pool()
    if action == 'MENU':
        row = await pool.fetchrow('SELECT * FROM menu_items WHERE key = $1 AND is_active', value)
        if not row:
            await query.message.reply_text('Раздел не найден.')
            return
        text = row['content'] or row['title']
        rendered = await render_text(text, {'id': query.from_user.id, 'username': query.from_user.username, 'first_name': query.from_user.first_name, 'last_name': query.from_user.last_name, 'project_link': None, 'points': 0, 'level': 1, 'joined_at': query.from_user.first_name}, None)
        buttons = await build_buttons(row['buttons'], None, None)
        await query.message.edit_text(rendered, reply_markup=buttons)
    elif action == 'ACTION':
        if value == 'profile':
            await query.message.reply_text('Используйте команду /profile')
        elif value == 'my_refs':
            await query.message.reply_text('Используйте команду /refs')
        elif value == 'add_link':
            await query.message.reply_text('Используйте команду /link <ваша ссылка>')
        elif value == 'ai_chat':
            await query.message.reply_text('Напишите /ai <вопрос> для общения с AI.')
        else:
            await query.message.reply_text('Действие пока не настроено.')
