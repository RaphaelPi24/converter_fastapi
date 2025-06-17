from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from auth.database import SessionLocal
from auth.model import User
from auth.security import hash_password, verify_password
from auth.session_redis import TokenManager
from config import TEMPLATES, MAX_AGE_COOKIE

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/login/", response_class=HTMLResponse)
async def show_login(request: Request):
    return TEMPLATES.TemplateResponse("login.html", {"request": request})


@router.post("/login/", dependencies=[Depends(RateLimiter(times=3, minutes=1))])
async def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверные учётные данные")

    clear_token = str(uuid4())
    token = TokenManager(clear_token)
    token.store_token(user.username)  # создание и установка

    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(
        key="auth_token",
        value=clear_token,  # мб ошибка
        httponly=True,  # no js, защита от XSS
        secure=False,  # пока False, потом True
        samesite="lax",  # от CSRF
        max_age=MAX_AGE_COOKIE
    )
    return response


# --- Выход ---
@router.get("/logout/")
async def logout(request: Request):
    token = request.cookies.get("auth_token")
    if token:
        token = TokenManager(token)
        token.delete_token()

    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("auth_token")
    return response


@router.get("/register/", response_class=HTMLResponse)
async def register_form(request: Request):
    return TEMPLATES.TemplateResponse("register.html", {"request": request})


@router.post("/register/", dependencies=[Depends(RateLimiter(times=3, minutes=1))])
async def register_user(
        request: Request,
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    existing = db.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()
    if existing:
        return TEMPLATES.TemplateResponse("register.html", {
            "request": request,
            "error": "Пользователь с таким именем или email уже существует"
        })

    hashed_pw = hash_password(password)
    user = User(username=username, email=email, hashed_password=hashed_pw)
    db.add(user)
    db.commit()

    return RedirectResponse(url="/login", status_code=302)
