import logging
from datetime import datetime
from telegram import Bot
from config import BOT_TOKEN
from db.connection import init_db

logger = logging.getLogger(__name__)

async def schedule_welcome_series():
    pool = await init_db()
    bot = Bot(BOT_TOKEN)
    rows = await pool.fetch(
        """
        SELECT w.*, u.id AS user_id, u.first_name, u.username
        FROM welcome_series w
        JOIN users u ON u.is_banned = FALSE
        LEFT JOIN welcome_series_log l ON l.user_id = u.id AND l.series_id = w.id
        WHERE w.is_active = TRUE AND l.id IS NULL
          AND NOW() >= u.joined_at + (w.delay_hours || ' hours')::interval
        ORDER BY w.sort_order
        """
    )
    for row in rows:
        try:
            text = row['content'] or row['title'] or 'Привет!'
            await bot.send_message(row['user_id'], text)
            await pool.execute(
                'INSERT INTO welcome_series_log (user_id, series_id) VALUES ($1, $2)',
                row['user_id'], row['id'],
            )
        except Exception as exc:
            logger.exception('Ошибка отправки welcome-сообщения: %s', exc)
