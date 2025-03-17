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


async def create_test_data():
    from app.database.models import TaskStatus, UserRole, TaskType, TaskPlatform
    try:
        await TaskPlatform.create(platform_name="Instagram")
        await TaskPlatform.create(platform_name="IYouTube")
        await TaskStatus.create(status_id="active", status_name="Active")
        await TaskStatus.create(status_id="waiting", status_name="Waiting")
        await UserRole.create(role_id="admin", role_name="Администратор")
        await UserRole.create(role_id="manager", role_name="Менеджер")
        await TaskType.create(task_type_id="active", task_type_name="Активен")
        await TaskType.create(task_type_id="waiting", task_type_name="Ожидание")
    except Exception as e:

        print(f"Exception: {e}")

# 📌 Подключение к базе и запуск создания админа при старте

app = create_app()


@app.on_event("startup")
async def startup_event():
    await create_admin_user()
    await create_test_data()

    # 📌 Запуск Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(PORT), reload=True)
