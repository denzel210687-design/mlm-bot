from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from api.auth import get_current_user
from db.connection import get_pool

router = APIRouter()
templates = Jinja2Templates(directory='api/templates')

@router.get('/welcome', response_class=HTMLResponse)
async def welcome_series(request: Request, user: dict = Depends(get_current_user)):
    pool = await get_pool()
    rows = await pool.fetch('SELECT * FROM welcome_series ORDER BY sort_order')
    return templates.TemplateResponse('welcome_series.html', {'request': request, 'series': rows, 'user': user})

@router.post('/welcome/add')
async def add_welcome_step(
    request: Request,
    day_number: int = Form(...),
    delay_hours: int = Form(0),
    title: str = Form(''),
    content: str = Form(...),
    sort_order: int = Form(0),
    user: dict = Depends(get_current_user)
):
    pool = await get_pool()
    await pool.execute(
        'INSERT INTO welcome_series (day_number, delay_hours, title, content, sort_order) VALUES ($1, $2, $3, $4, $5)',
        day_number, delay_hours, title, content, sort_order
    )
    return RedirectResponse(url='/welcome', status_code=303)
