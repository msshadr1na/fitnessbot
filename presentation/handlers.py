from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import inline_keyboard_button, reply_markup_union, users_shared, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from app.models import User
from app.services import OrganizationMemberRepository, UserService, OrganizationService
from infrastructure.database import get_db_pool
from infrastructure.repositories import UserRepository, SettingsRepository, OrganizationRepository
import presentation.keyboards

router = Router()

waiting_for_name = set()
waiting_for_org_num = set()
waiting_for_delete_confirm = set()

# Команды
@router.message(CommandStart())
async def handle_start(message: types.Message):
    pool = await get_db_pool()

    userRepo = UserRepository(pool)
    settingsRepos = SettingsRepository(pool)

    user_service = UserService(userRepo,settingsRepos)

    user_id = message.from_user.id
    user = await user_service.find_by_tgid(user_id)
    if (user == None):
        if message.from_user.last_name == None:
            last_name = "Фамилия"
        else:
            last_name = message.from_user.last_name
        user = await user_service.registration(user_id, None, message.from_user.first_name, last_name, None)

    keyboard = presentation.keyboards.build_start_keyboard()
    await message.answer(f"Добро пожаловать, {user.first_name}!\nВойти как:", reply_markup=keyboard)

@router.message(Command("create"))
async def start_create_note(message: types.Message):
    waiting_for_name.add(message.from_user.id)
    
    await message.answer("Введите название для будущей организации:")

@router.message(Command("delete"))
async def start_create_note(message: types.Message):
    pool = await get_db_pool()

    user_service = UserService(UserRepository(pool),SettingsRepository(pool))
    org_service = OrganizationService(OrganizationRepository(pool),OrganizationMemberRepository(pool))


    user = await user_service.find_by_tgid(message.from_user.id)
    if not user:
        await message.answer("Пользователь не найден. Пройдите регистрацию используя команду /start для дальнейшего использования бота")
        return

    ids, orgs = await org_service.show_owned_orgs(user.id)

    if len(orgs) < 1:
        await message.answer("У вас нет организаций для удаления")
    else:
        keyboard = presentation.keyboards.build_delete_org_keyboard(ids,orgs)

        await message.answer("Выберите организацию для удаления:", reply_markup=keyboard)

# Обработчики кнопок

@router.callback_query(F.data.startswith("start"))
async def cancel_delete_org(callback: CallbackQuery):
    keyboard = presentation.keyboards.build_start_keyboard()
    await callback.message.answer("Войти как:", reply_markup=keyboard)


@router.callback_query(F.data.startswith("del_org_"))
async def confirm_delete(callback: CallbackQuery):
    org_id = int(callback.data.split("_")[-1])
    keyboard = presentation.keyboards.build_confirm_delete_org(org_id)
    
    await callback.message.edit_text(
        f"Вы уверены, что хотите удалить организацию?", reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data.startswith("confirm_del_"))
async def confirm_delete_org(callback: CallbackQuery):
    org_id = int(callback.data.split("_")[-1])
    
    pool = await get_db_pool()
    user_repo = UserRepository(pool)
    org_repo = OrganizationRepository(pool)
    org_member_repo = OrganizationMemberRepository(pool)
    user_service = UserService(user_repo, SettingsRepository(pool))
    org_service = OrganizationService(org_repo, org_member_repo)

    user = await user_service.find_by_tgid(callback.from_user.id)
    org = await org_service.get_by_id(org_id)

    await org_service.delete_organization(user.id, org_id)
    await callback.message.edit_text(f"Организация {org.name} успешно удалена.")

    await callback.answer()

@router.callback_query(F.data.startswith("cancel_del"))
async def cancel_delete_org(callback: CallbackQuery):
    await callback.message.edit_text(f"Организация не была удалена.")
    await callback.answer()

@router.callback_query(F.data.startswith("owner"))
async def as_org(callback: CallbackQuery):
    pool = await get_db_pool()
    user_service = UserService(UserRepository(pool), SettingsRepository(pool))
    user = await user_service.find_by_tgid(callback.from_user.id)

    keyboard = await presentation.keyboards.build_org_keyboard()
    await callback.message.edit_text("Вы вошли как организатор",reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data.startswith("orgs"))
async def choose_org(callback):

    pool = await get_db_pool()
    user_service = UserService(UserRepository(pool), SettingsRepository(pool))
    org_service = OrganizationService(OrganizationRepository(pool),OrganizationMemberRepository(pool))

    user = await user_service.find_by_tgid(callback.from_user.id)
    ids, names = await org_service.show_owned_orgs(user.id)

    if len(names) < 1:
        keyboard = presentation.keyboards.build_zero_orgs_keyboard()
        await callback.message.edit_text("У вас нет организаций", reply_markup=keyboard)
    else:
        keyboard = presentation.keyboards.build_choose_org_keyboard(ids,names)
        await callback.message.edit_text("Выберите организацию:", reply_markup=keyboard)

@router.callback_query(F.data == "create_org")
async def start_create_org(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    waiting_for_name.add(user_id)
    await callback.message.answer("Введите название для будущей организации:")
    await callback.answer()

   



# Текстовые сообщения
@router.message()
async def handle_text_messages(message: types.Message):
    user_id = message.from_user.id    

    if user_id in waiting_for_name:
        await handle_create_organization(message)
        return
    
    await message.answer("Неизвестная команда. Используйте /create или /delete.")


# Вспомогательные функции
async def handle_create_organization(message: types.Message):
    user_id = message.from_user.id
    name = message.text

    pool = await get_db_pool()
    organizationRepo = OrganizationRepository(pool)
    organizationMemberRepo = OrganizationMemberRepository(pool)
    userRepo = UserRepository(pool)
    settingsRepos = SettingsRepository(pool)
    user_service = UserService(userRepo, settingsRepos)
    organization_service = OrganizationService(organizationRepo, organizationMemberRepo)

    user = await user_service.find_by_tgid(user_id)
    is_created = await organization_service.find_by_name(name)

    if is_created is None:
        organization = await organization_service.create_organization(user, name)
        waiting_for_name.remove(user_id)
        keyboard = await presentation.keyboards.build_org_keyboard()
        await message.answer(f"Организация {name} успешно создана")
        await message.answer("Вы вошли как организатор", reply_markup=keyboard)
    else:
        await message.answer(
            f"Организация с названием {name} уже существует.\n"
            "Введите другое название:"
        )

