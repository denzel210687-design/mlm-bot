async def create_tables(pool):
    await pool.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id BIGINT PRIMARY KEY,
        username VARCHAR(255),
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        referrer_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
        project_link TEXT,
        joined_at TIMESTAMP DEFAULT NOW(),
        last_active TIMESTAMP DEFAULT NOW(),
        points INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1,
        achievements JSONB DEFAULT '[]',
        crm_stage VARCHAR(50) DEFAULT 'new',
        crm_notes TEXT,
        crm_tags TEXT[] DEFAULT '{}',
        ai_context JSONB DEFAULT '[]',
        is_banned BOOLEAN DEFAULT FALSE
    );
    """)

    await pool.execute("""
    CREATE TABLE IF NOT EXISTS referrals (
        id SERIAL PRIMARY KEY,
        user_id BIGINT REFERENCES users(id),
        referrer_id BIGINT REFERENCES users(id),
        depth INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT NOW()
    );
    """)

    await pool.execute("""
    CREATE TABLE IF NOT EXISTS project_links (
        id SERIAL PRIMARY KEY,
        user_id BIGINT REFERENCES users(id),
        link TEXT NOT NULL,
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT NOW(),
        deactivated_at TIMESTAMP
    );
    """)

    await pool.execute("""
    CREATE TABLE IF NOT EXISTS menu_items (
        id SERIAL PRIMARY KEY,
        key VARCHAR(100) UNIQUE NOT NULL,
        parent_key VARCHAR(100),
        title VARCHAR(255) NOT NULL,
        content_type VARCHAR(50) DEFAULT 'text',
        content TEXT,
        media_file_id TEXT,
        buttons JSONB DEFAULT '[]',
        is_active BOOLEAN DEFAULT TRUE,
        sort_order INTEGER DEFAULT 0,
        protect_content BOOLEAN DEFAULT FALSE,
        disable_preview BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT NOW()
    );
    """)

    await pool.execute("""
    CREATE TABLE IF NOT EXISTS broadcasts (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        content TEXT,
        media_file_id TEXT,
        buttons JSONB DEFAULT '[]',
        target JSONB DEFAULT '{"all": true}',
        status VARCHAR(50) DEFAULT 'draft',
        scheduled_at TIMESTAMP,
        started_at TIMESTAMP,
        finished_at TIMESTAMP,
        total INTEGER DEFAULT 0,
        sent INTEGER DEFAULT 0,
        failed INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT NOW()
    );
    """)

    await pool.execute("""
    CREATE TABLE IF NOT EXISTS welcome_series (
        id SERIAL PRIMARY KEY,
        day_number INTEGER NOT NULL,
        delay_hours INTEGER DEFAULT 0,
        title VARCHAR(255),
        content TEXT,
        media_file_id TEXT,
        buttons JSONB DEFAULT '[]',
        is_active BOOLEAN DEFAULT TRUE,
        sort_order INTEGER DEFAULT 0
    );
    """)

    await pool.execute("""
    CREATE TABLE IF NOT EXISTS welcome_series_log (
        id SERIAL PRIMARY KEY,
        user_id BIGINT REFERENCES users(id),
        series_id INTEGER REFERENCES welcome_series(id),
        sent_at TIMESTAMP DEFAULT NOW()
    );
    """)

    await pool.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        key VARCHAR(100) PRIMARY KEY,
        value TEXT,
        updated_at TIMESTAMP DEFAULT NOW()
    );
    """)

    await pool.execute("""
    CREATE TABLE IF NOT EXISTS achievements_config (
        id SERIAL PRIMARY KEY,
        code VARCHAR(100) UNIQUE,
        title VARCHAR(255),
        icon VARCHAR(10),
        points_reward INTEGER DEFAULT 0,
        condition_type VARCHAR(50),
        condition_value INTEGER
    );
    """)

async def ensure_defaults(pool):
    defaults = [
        ('panel_password', 'admin123'),
        ('panel_secret_key', ''),
        ('bot_token', ''),
        ('project_link_mask', 'https://'),
        ('ai_enabled', 'true'),
        ('ai_system_prompt', 'Ты помощник MLM-команды. Отвечай кратко и дружелюбно. Если не знаешь — предложи связаться с куратором.'),
        ('ai_model', 'gpt-4o-mini'),
        ('gamification_enabled', 'true'),
        ('welcome_message', '👋 Привет, {first_name}! Добро пожаловать в систему.'),
        ('delete_join_message', 'true'),
        ('notify_admin_on_join', 'true'),
        ('admin_notify_text', '🆕 Новый партнёр: {full_name} (@{username})\nПригласил: уровень 1')
    ]
    for key, value in defaults:
        await pool.execute(
            "INSERT INTO settings (key, value) VALUES ($1, $2) ON CONFLICT (key) DO NOTHING",
            key,
            value,
        )
