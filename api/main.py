import json
import asyncio
from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from api.auth import create_access_token, verify_panel_password
from api.routes.dashboard import router as dashboard_router
from api.routes.users import router as users_router
from api.routes.menu import router as menu_router
from api.routes.broadcasts import router as broadcasts_router
from api.routes.settings import router as settings_router
from api.routes.welcome import router as welcome_router
from config import PORT
from db.connection import init_db, close_db
from db.migrations import create_tables, ensure_defaults

app = FastAPI()
templates = Jinja2Templates(directory='api/templates')

@app.on_event('startup')
async def startup_event():
    pool = await init_db()
    await create_tables(pool)
    await ensure_defaults(pool)

@app.on_event('shutdown')
async def shutdown_event():
    await close_db()

@app.get('/login', response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse('login.html', {'request': request, 'error': None})

@app.post('/token')
async def login(request: Request, password: str = Form(...)):
    if not verify_panel_password(password):
        return templates.TemplateResponse('login.html', {'request': request, 'error': 'Неверный пароль'} )
    token = create_access_token({'sub': 'admin'})
    response = RedirectResponse(url='/dashboard', status_code=status.HTTP_302_FOUND)
    response.set_cookie('access_token', f'Bearer {token}', httponly=True)
    return response

@app.get('/', response_class=HTMLResponse)
async def index():
    return RedirectResponse(url='/dashboard')

app.include_router(dashboard_router)
app.include_router(users_router)
app.include_router(menu_router)
app.include_router(broadcasts_router)
app.include_router(settings_router)
app.include_router(welcome_router)
