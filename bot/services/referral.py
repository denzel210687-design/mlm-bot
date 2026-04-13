from db.connection import get_pool

async def register_referral(user_id: int, referrer_id: int, pool):
    ancestors = await get_ancestors(referrer_id, pool)
    await pool.execute(
        "INSERT INTO referrals (user_id, referrer_id, depth) VALUES ($1, $2, $3) ON CONFLICT DO NOTHING",
        user_id,
        referrer_id,
        1,
    )
    for ancestor_id, depth in ancestors:
        await pool.execute(
            "INSERT INTO referrals (user_id, referrer_id, depth) VALUES ($1, $2, $3) ON CONFLICT DO NOTHING",
            user_id,
            ancestor_id,
            depth + 1,
        )

async def get_ancestors(user_id: int, pool, depth: int = 1):
    row = await pool.fetchrow("SELECT referrer_id FROM users WHERE id = $1", user_id)
    if not row or not row['referrer_id']:
        return []
    referrer_id = row['referrer_id']
    result = [(referrer_id, depth)]
    result += await get_ancestors(referrer_id, pool, depth + 1)
    return result

async def get_tree(user_id: int, pool):
    rows = await pool.fetch(
        """
        SELECT u.id, u.first_name, u.username, u.project_link,
               r.depth, u.joined_at
        FROM referrals r
        JOIN users u ON u.id = r.user_id
        WHERE r.referrer_id = $1
        ORDER BY r.depth, u.joined_at
        """,
        user_id,
    )
    tree = {}
    for row in rows:
        depth = row['depth']
        tree.setdefault(depth, []).append(dict(row))
    return tree

async def get_stats(user_id: int, pool):
    return await pool.fetchrow(
        """
        SELECT
            COUNT(*) as total,
            COUNT(*) FILTER (WHERE depth = 1) as level_1,
            COUNT(*) FILTER (WHERE depth = 2) as level_2,
            COUNT(*) FILTER (WHERE depth = 3) as level_3,
            COUNT(*) FILTER (WHERE depth > 3) as deeper,
            COUNT(*) FILTER (WHERE created_at > NOW() - INTERVAL '7 days') as week,
            COUNT(*) FILTER (WHERE created_at > NOW() - INTERVAL '1 day') as today
        FROM referrals
        WHERE referrer_id = $1
        """,
        user_id,
    )

async def get_referrals_count(user_id: int, pool):
    row = await pool.fetchrow("SELECT COUNT(*) AS total FROM referrals WHERE referrer_id = $1", user_id)
    return row['total'] if row else 0
