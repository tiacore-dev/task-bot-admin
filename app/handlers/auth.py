from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials
from loguru import logger
from app.config import Settings
from app.database.models import AdminUser
from app.auth_schemas import bearer_scheme

# Конфигурация JWT
settings = Settings()
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
REFRESH_TOKEN_EXPIRE_DAYS = int(settings.REFRESH_TOKEN_EXPIRE_DAYS)


# Создание токенов
def create_access_token(username: str, admin_id: str, expires_delta: timedelta = None):
    expire = datetime.utcnow() + \
        (expires_delta if expires_delta else timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode = {
        "sub": username,  # Логин
        "admin_id": admin_id,  # ID администратора
        "exp": expire
    }

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.info(f"✅ Создан Access JWT для {username} (admin_id={admin_id})")
    return encoded_jwt


def create_refresh_token(username: str, admin_id: str):
    return create_access_token(username, admin_id, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))


# Проверка токена
def get_current_user(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)) -> dict:
    """
    Проверяет токен из заголовка Authorization и возвращает словарь с admin_id и username.
    """
    if credentials is None:
        logger.warning("❌ Запрос без токена! Отправляем 401")
        raise HTTPException(status_code=401, detail="Missing token")

    if not credentials.credentials:
        logger.warning("❌ Пустой токен! Отправляем 401")
        raise HTTPException(status_code=401, detail="Empty token")

    token = credentials.credentials
    return verify_token(token)


def verify_token(token: str) -> dict:
    logger.info(f"Проверка токена: {token}")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        admin_id: str = payload.get("admin_id")

        if username is None or admin_id is None:
            logger.warning("Некорректный токен: отсутствуют sub или admin_id")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        logger.success(
            f"Токен валиден, username: {username}, admin_id: {admin_id}")
        return {"username": username, "admin_id": admin_id}
    except JWTError as exc:
        logger.error("Ошибка JWT-декодирования")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        ) from exc


async def login_handler(username: str, password: str):
    """
    Проверяет логин и пароль, если верно — возвращает access и refresh токены.
    """
    user = await AdminUser.filter(username=username).first()

    if not user:
        return None  # Возвращаем None, если пользователь не найден

    check_password = user.check_password(password)
    if check_password:
        # Принудительно приводим admin_id к строке (UUID не всегда правильно кодируется)
        admin_id_str = str(user.admin_id)

        access_token = create_access_token(
            username, admin_id_str, expires_delta=timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        refresh_token = create_refresh_token(
            username, admin_id_str)

        return {"access_token": access_token, "refresh_token": refresh_token}

    return None  # Возвращаем None, если пароль неверный
