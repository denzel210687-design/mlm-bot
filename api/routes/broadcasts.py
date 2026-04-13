from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from api.auth import get_current_user
from db.connection import get_pool

router = APIRouter()
templates = Jinja2Templates(directory='api/templates')

@router.get('/broadcasts', response_class=HTMLResponse)
async def broadcasts(request: Request, user: dict = Depends(get_current_user)):
    pool = await get_pool()
    rows = await pool.fetch('SELECT * FROM broadcasts ORDER BY created_at DESC LIMIT 100')
    return templates.TemplateResponse('broadcasts.html', {'request': request, 'broadcasts': rows, 'user': user})

@router.post('/broadcasts/add')
async def add_broadcast(
    request: Request,
    name: str = Form(...),
    content: str = Form(...),
    user: dict = Depends(get_current_user)
):
    pool = await get_pool()
    await pool.execute(
        'INSERT INTO broadcasts (name, content, status) VALUES ($1, $2, $3)',
        name, content, 'draft'
    )
    return RedirectResponse(url='/broadcasts', status_code=303)
