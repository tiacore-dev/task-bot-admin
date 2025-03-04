import os
from dotenv import load_dotenv
from app.database.models import AdminUser, set_password
from app import create_app

load_dotenv()

# Порт и биндинг
PORT = os.getenv('ADMIN_PORT', "8001")

# 📌 Автоматическое создание супер-админа


async def create_admin_user():
    admin = await AdminUser.get_or_none(username="admin")
    if not admin:
        print("🔹 Создаю администратора...")
        password_hash = await set_password("qweasdzxc")
        admin = await AdminUser.create(username="admin", password_hash=password_hash)

        await admin.save()
        print("✅ Администратор создан: admin / qweasdzxc")
    else:
        print("✅ Админ уже существует.")

# 📌 Подключение к базе и запуск создания админа при старте

app = create_app()


# @app.on_event("startup")
# async def startup_event():
#     await create_admin_user()

# 📌 Запуск Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(PORT), reload=True)
