from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from api.auth import get_current_user
from db.connection import get_pool

router = APIRouter()
templates = Jinja2Templates(directory='api/templates')

@router.get('/users', response_class=HTMLResponse)
async def users_list(request: Request, user: dict = Depends(get_current_user)):
    pool = await get_pool()
    rows = await pool.fetch('SELECT * FROM users ORDER BY joined_at DESC LIMIT 100')
    return templates.TemplateResponse('users.html', {'request': request, 'users': rows, 'user': user})

@router.get('/users/{user_id}', response_class=HTMLResponse)
async def user_profile(request: Request, user_id: int, user: dict = Depends(get_current_user)):
    pool = await get_pool()
    row = await pool.fetchrow('SELECT * FROM users WHERE id = $1', user_id)
    return templates.TemplateResponse('user_profile.html', {'request': request, 'target': row, 'user': user})
