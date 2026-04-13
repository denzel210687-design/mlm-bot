from datetime import datetime, timedelta
from fastapi import HTTPException, Request, status
from jose import JWTError, jwt
from config import SECRET_KEY, PANEL_PASSWORD

def create_access_token(data: dict, expires_delta: int = 3600):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=expires_delta)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm='HS256')
    return encoded_jwt

async def get_current_user(request: Request):
    token = request.cookies.get('access_token')
    if token and token.startswith('Bearer '):
        token = token.split(' ', 1)[1]
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Необходима авторизация')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        username: str = payload.get('sub')
        if username is None or username != 'admin':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверный токен авторизации')
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверный токен авторизации')
    return {'username': 'admin'}

def verify_panel_password(password: str) -> bool:
    return password == PANEL_PASSWORD
