from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from auth.database import SessionLocal
from auth.model import User
from auth.security import hash_password, verify_password
from auth.session_redis import store_token, get_username_from_token, delete_token
from auth.validate import UserCreate, UserOut
from config import TEMPLATES
router = APIRouter()


# --- Зависимость ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/login", response_class=HTMLResponse)
def show_login(request: Request):
    return TEMPLATES.TemplateResponse("login.html", {"request": request})


# --- Регистрация ---
@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.username == user_in.username) | (User.email == user_in.email)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    hashed_pw = hash_password(user_in.password)
    user = User(username=user_in.username, email=user_in.email, hashed_password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# --- Вход ---
@router.post("/login/")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверные учётные данные")

    token = str(uuid4())
    store_token(token, user.username)

    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(key="auth_token", value=token, httponly=True)
    return response


# --- Выход ---
@router.get("/logout/")
def logout(request: Request):
    token = request.cookies.get("auth_token")
    if token:
        delete_token(token)
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("auth_token")
    return response


# --- Пример защищённой страницы ---
@router.get("/secure/")
def secure_page(request: Request):
    token = request.cookies.get("auth_token")
    username = get_username_from_token(token) if token else None
    if not username:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {"msg": f"Добро пожаловать, {username}!"}


@router.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return TEMPLATES.TemplateResponse("register.html", {"request": request})


@router.post("/register/")
def register_user(
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
