from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import users_shared
from app.models import User
from app.services import UserService
from infrastructure.database import get_db_pool
from infrastructure.repositories import UserRepository, SettingsRepository


router = Router()

@router.message(CommandStart())
async def handle_start(message: types.Message):
    pool = await get_db_pool()

    userRepo = UserRepository(pool)
    settingsRepos = SettingsRepository(pool)

    user_service = UserService(userRepo,settingsRepos)

    user_id = message.from_user.id
    user = await user_service.find_by_tgid(user_id)
    if (user == None):
        user = await user_service.registration(user_id, None, message.from_user.first_name, message.from_user.last_name, None)

    await message.answer(f"Добро пожаловать, {user.first_name}!\n")

