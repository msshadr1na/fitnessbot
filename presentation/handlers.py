from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import users_shared
from app.models import User
from app.services import OrganizationMemberRepository, UserService, OrganiationService
from infrastructure.database import get_db_pool
from infrastructure.repositories import UserRepository, SettingsRepository, OrganizationRepository


router = Router()

waiting_for_name = set()

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

@router.message(Command("create"))
async def start_create_note(message: types.Message):
    waiting_for_name.add(message.from_user.id)
    
    await message.answer("Введите название для будущей организации:")


@router.message()
async def handle_note_text(message: types.Message):
    if message.from_user.id in waiting_for_name:
        name = message.text
        waiting_for_name.remove(message.from_user.id)

        pool = await get_db_pool()
        organizationRepo = OrganizationRepository(pool)
        organizationMemberRepo = OrganizationMemberRepository(pool)
        userRepo = UserRepository(pool)
        settingsRepos = SettingsRepository(pool)
        user_service = UserService(userRepo,settingsRepos)
        organization_service = OrganiationService(organizationRepo,organizationMemberRepo)

        user_id = message.from_user.id
        user = await user_service.find_by_tgid(user_id)
        organization = await organization_service.create_organization(user,name)
        
        await message.answer(f"Организация {name} успешно создана")