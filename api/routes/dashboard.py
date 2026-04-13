from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from api.auth import get_current_user
from db.connection import get_pool

router = APIRouter()
templates = Jinja2Templates(directory='api/templates')

@router.get('/dashboard', response_class=HTMLResponse)
async def dashboard(request: Request, user: dict = Depends(get_current_user)):
    pool = await get_pool()
    total_users = await pool.fetchval('SELECT COUNT(*) FROM users')
    total_referrals = await pool.fetchval('SELECT COUNT(*) FROM referrals')
    total_broadcasts = await pool.fetchval('SELECT COUNT(*) FROM broadcasts')
    return templates.TemplateResponse('dashboard.html', {
        'request': request,
        'user': user,
        'stats': {
            'total_users': total_users,
            'total_referrals': total_referrals,
            'total_broadcasts': total_broadcasts,
        },
    })
