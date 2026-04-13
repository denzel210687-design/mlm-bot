LEVELS = {
    1: {"name": "Новичок",  "icon": "🌱", "min_points": 0},
    2: {"name": "Партнёр",  "icon": "🤝", "min_points": 100},
    3: {"name": "Лидер",    "icon": "⭐", "min_points": 300},
    4: {"name": "Мастер",   "icon": "🔥", "min_points": 700},
    5: {"name": "Эксперт",  "icon": "💎", "min_points": 1500},
}

POINTS_RULES = {
    "registration": 10,
    "add_project_link": 25,
    "referral_level_1": 50,
    "referral_level_2": 25,
    "referral_level_3": 10,
    "referral_deeper": 5,
    "referral_added_link": 30,
    "active_7_days": 20,
    "active_30_days": 100,
}

DEFAULT_ACHIEVEMENTS = [
    {"code": "first_referral", "title": "Первый партнёр",  "icon": "🎉", "points": 100, "condition_type": "referrals_count", "condition_value": 1},
    {"code": "team_5",         "title": "Команда 5",       "icon": "💪", "points": 300, "condition_type": "referrals_count", "condition_value": 5},
    {"code": "team_10",        "title": "Команда 10",      "icon": "🔥", "points": 500, "condition_type": "referrals_count", "condition_value": 10},
    {"code": "team_50",        "title": "Лидер 50",        "icon": "⭐", "points": 2000, "condition_type": "referrals_count", "condition_value": 50},
    {"code": "team_100",       "title": "Топ 100",         "icon": "👑", "points": 5000, "condition_type": "referrals_count", "condition_value": 100},
    {"code": "link_added",     "title": "Система запущена","icon": "🚀", "points": 50,  "condition_type": "has_project_link", "condition_value": 1},
    {"code": "level_3",        "title": "Достиг Лидера",   "icon": "🌟", "points": 200, "condition_type": "level_reached",   "condition_value": 3},
    {"code": "level_5",        "title": "Достиг Эксперта", "icon": "💎", "points": 1000, "condition_type": "level_reached",   "condition_value": 5},
]

async def get_level_by_points(points: int) -> int:
    level = 1
    for key, info in sorted(LEVELS.items()):
        if points >= info['min_points']:
            level = key
    return level

async def award_points(user_id: int, amount: int, pool):
    if amount <= 0:
        return
    await pool.execute(
        "UPDATE users SET points = points + $1 WHERE id = $2",
        amount,
        user_id,
    )
    row = await pool.fetchrow("SELECT points FROM users WHERE id = $1", user_id)
    if not row:
        return
    level = await get_level_by_points(row['points'])
    await pool.execute("UPDATE users SET level = $1 WHERE id = $2", level, user_id)

async def ensure_achievement_configs(pool):
    for achievement in DEFAULT_ACHIEVEMENTS:
        await pool.execute(
            "INSERT INTO achievements_config (code, title, icon, points_reward, condition_type, condition_value) VALUES ($1,$2,$3,$4,$5,$6) ON CONFLICT (code) DO NOTHING",
            achievement['code'],
            achievement['title'],
            achievement['icon'],
            achievement['points'],
            achievement['condition_type'],
            achievement['condition_value'],
        )
