from fastapi import APIRouter,  HTTPException, Form
from app.database.models import AdminUser
from app.handlers.auth import create_access_token

auth_router = APIRouter(prefix="/auth", tags=["auth"])


# 📌 Регистрация администратора


@auth_router.post("/register")
async def register_admin(username: str = Form(...), password: str = Form(...)):
    existing_admin = await AdminUser.filter(username=username).first()
    if existing_admin:
        raise HTTPException(status_code=400, detail="Admin already exists")

    admin = await AdminUser.create(username=username)
    await admin.set_password(password)
    await admin.save()
    return {"message": "Admin registered successfully"}

# 📌 Авторизация администратора


@auth_router.post("/token")
async def login_admin(username: str = Form(...), password: str = Form(...)):
    admin = await AdminUser.filter(username=username).first()
    if not admin or not admin.verify_password(password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": admin.username})
    return {"access_token": token, "token_type": "bearer"}

# 📌 Получение текущего администратора
