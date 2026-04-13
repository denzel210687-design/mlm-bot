from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from api.auth import get_current_user
from db.connection import get_pool

router = APIRouter()
templates = Jinja2Templates(directory='api/templates')

@router.get('/menu', response_class=HTMLResponse)
async def menu_list(request: Request, user: dict = Depends(get_current_user)):
    pool = await get_pool()
    rows = await pool.fetch('SELECT * FROM menu_items ORDER BY sort_order, id')
    return templates.TemplateResponse('menu.html', {'request': request, 'menu_items': rows, 'user': user})

@router.post('/menu/add')
async def add_menu_item(
    request: Request,
    key: str = Form(...),
    title: str = Form(...),
    content: str = Form(''),
    parent_key: str = Form(''),
    sort_order: int = Form(0),
    user: dict = Depends(get_current_user)
):
    pool = await get_pool()
    await pool.execute(
        'INSERT INTO menu_items (key, title, content, parent_key, sort_order) VALUES ($1, $2, $3, $4, $5)',
        key, title, content, parent_key or None, sort_order
    )
    return RedirectResponse(url='/menu', status_code=303)
