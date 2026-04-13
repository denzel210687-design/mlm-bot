import logging
from telegram import Bot
from config import BOT_TOKEN
from db.connection import init_db

logger = logging.getLogger(__name__)

async def resolve_broadcast_users(broadcast, pool):
    target = broadcast['target'] or {'all': True}
    if target.get('all'):
        rows = await pool.fetch('SELECT id FROM users WHERE is_banned = FALSE')
    elif 'crm_stage' in target:
        rows = await pool.fetch('SELECT id FROM users WHERE crm_stage = ANY($1::text[]) AND is_banned = FALSE', target['crm_stage'])
    elif 'tags' in target:
        rows = await pool.fetch('SELECT id FROM users WHERE crm_tags && $1::text[] AND is_banned = FALSE', target['tags'])
    else:
        rows = await pool.fetch('SELECT id FROM users WHERE is_banned = FALSE')
    return [row['id'] for row in rows]

async def schedule_broadcasts():
    pool = await init_db()
    bot = Bot(BOT_TOKEN)
    broadcasts = await pool.fetch(
        "SELECT * FROM broadcasts WHERE status IN ('draft', 'scheduled') AND (scheduled_at IS NULL OR scheduled_at <= NOW())"
    )
    for broadcast in broadcasts:
        user_ids = await resolve_broadcast_users(broadcast, pool)
        if not user_ids:
            continue
        await pool.execute('UPDATE broadcasts SET status = $1, started_at = NOW(), total = $2 WHERE id = $3', 'started', len(user_ids), broadcast['id'])
        sent = 0
        failed = 0
        for user_id in user_ids:
            try:
                await bot.send_message(user_id, broadcast['content'] or '')
                sent += 1
            except Exception:
                failed += 1
        await pool.execute(
            'UPDATE broadcasts SET status = $1, finished_at = NOW(), sent = $2, failed = $3 WHERE id = $4',
            'finished' if failed == 0 else 'finished',
            sent,
            failed,
            broadcast['id'],
        )
        logger.info('Broadcast %s finished: sent=%s failed=%s', broadcast['id'], sent, failed)
