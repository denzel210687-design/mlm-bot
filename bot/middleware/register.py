from db.connection import get_pool
from bot.services.referral import register_referral

async def register_user(telegram_user, referrer_id: int = None):
    pool = await get_pool()
    await pool.execute(
        """
        INSERT INTO users (id, username, first_name, last_name, referrer_id)
        VALUES ($1, $2, $3, $4, $5)
        ON CONFLICT (id) DO UPDATE SET
            username = EXCLUDED.username,
            first_name = EXCLUDED.first_name,
            last_name = EXCLUDED.last_name,
            last_active = NOW()
        """,
        telegram_user.id,
        telegram_user.username,
        telegram_user.first_name,
        telegram_user.last_name,
        referrer_id,
    )
    if referrer_id:
        await register_referral(telegram_user.id, referrer_id, pool)
    return telegram_user.id
