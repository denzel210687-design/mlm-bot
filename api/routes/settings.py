from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from api.auth import get_current_user
from db.connection import get_pool

router = APIRouter()
templates = Jinja2Templates(directory='api/templates')

@router.get('/settings', response_class=HTMLResponse)
async def settings_page(request: Request, user: dict = Depends(get_current_user)):
    pool = await get_pool()
    rows = await pool.fetch('SELECT * FROM settings ORDER BY key')
    return templates.TemplateResponse('settings.html', {'request': request, 'settings': rows, 'user': user})

@router.post('/settings/update')
async def update_setting(
    request: Request,
    key: str = Form(...),
    value: str = Form(...),
    user: dict = Depends(get_current_user)
):
    pool = await get_pool()
    await pool.execute(
        'UPDATE settings SET value = $1, updated_at = NOW() WHERE key = $2',
        value, key
    )
    return RedirectResponse(url='/settings', status_code=303)
