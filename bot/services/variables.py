from config import BOT_USERNAME

VARIABLES = {
    "{user_id}": lambda u, _: str(u['id']),
    "{username}": lambda u, _: f"@{u['username']}" if u['username'] else u['first_name'],
    "{first_name}": lambda u, _: u['first_name'] or "",
    "{last_name}": lambda u, _: u['last_name'] or "",
    "{full_name}": lambda u, _: f"{u['first_name']} {u['last_name'] or ''}".strip(),
    "{referral_link}": lambda u, _: f"https://t.me/{BOT_USERNAME}?start={u['id']}" if BOT_USERNAME else str(u['id']),
    "{user_project_link}": lambda u, _: u['project_link'] or "не указана",
    "{referrer_project_link}": lambda u, ref: ref['project_link'] if ref else "",
    "{referrals_count}": lambda u, _: str(u.get('ref_count', 0)),
    "{level}": lambda u, _: str(u['level']),
    "{level_name}": lambda u, _: '',
    "{points}": lambda u, _: str(u['points']),
    "{join_date}": lambda u, _: u['joined_at'].strftime("%d.%m.%Y"),
}

async def render_text(text: str, user: dict, referrer: dict = None) -> str:
    for var, fn in VARIABLES.items():
        if var in text:
            text = text.replace(var, fn(user, referrer))
    return text
