from fastapi import APIRouter, Body, HTTPException
from jose import JWTError, jwt
from loguru import logger
from app.handlers.auth import login_handler, create_refresh_token, create_access_token
from app.handlers.auth import SECRET_KEY, ALGORITHM
from app.pydantic_models.auth_schemas import TokenResponse, LoginRequest

auth_router = APIRouter(prefix="/auth", tags=["auth"])


# 📌 Регистрация администратора


# @auth_router.post("/register", response_model=TokenResponse, summary="Регистрация")
# async def register_admin(data: LoginRequest):
#     existing_admin = await AdminUser.filter(username=username).first()
#     if existing_admin:
#         raise HTTPException(status_code=400, detail="Admin already exists")

#     admin = await AdminUser.create(username=username)
#     await admin.set_password(password)
#     await admin.save()
#     return {"message": "Admin registered successfully"}

# 📌 Авторизация администратора


@auth_router.post("/token", response_model=TokenResponse, summary="Авторизация пользователя")
async def login(data: LoginRequest):
    tokens = await login_handler(data.username, data.password)
    if not tokens:
        raise HTTPException(status_code=401, detail="Неверные учетные данные")

    return TokenResponse(
        **tokens
    )


@auth_router.post("/refresh", response_model=TokenResponse, summary="Обновление Access Token")
async def refresh_access_token(data: dict = Body(...)):
    try:
        refresh_token = data.get("refresh_token")
        if not refresh_token:
            raise HTTPException(
                status_code=400, detail="Refresh token is required")

        logger.info(f"🔄 Проверяем refresh_token: {refresh_token}")
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        admin_id: str = payload.get("admin_id")  # 🛠️ Добавляем admin_id

        if not username or not admin_id:
            raise HTTPException(status_code=401, detail="Неверный токен")

        # Создаём новые токены с username и admin_id
        new_access_token = create_access_token(username, admin_id)
        new_refresh_token = create_refresh_token(username, admin_id)

        logger.info(
            f"✅ Новый access_token создан для {username} (admin_id={admin_id})")

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )

    except JWTError as exc:
        logger.error(
            "❌ Ошибка декодирования refresh_token: Неверный или просроченный токен")
        raise HTTPException(
            status_code=401, detail="Неверный или просроченный токен") from exc
