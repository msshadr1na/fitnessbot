from aiogram.types import inline_keyboard_button, users_shared, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from app.models import User

def build_start_keyboard():
    buttons =[[InlineKeyboardButton(text="Организатор", callback_data="owner")],
              [InlineKeyboardButton(text="Работник", callback_data="worker")],
              [InlineKeyboardButton(text="Клиент", callback_data="client")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

async def build_org_keyboard():
    buttons = [[InlineKeyboardButton(text="Выбрать организацию", callback_data="orgs")],
               [InlineKeyboardButton(text="Создать организацию",callback_data="create_org")],
               [InlineKeyboardButton(text="Назад", callback_data="start")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def build_zero_orgs_keyboard():
    buttons=[[InlineKeyboardButton(text="Назад", callback_data="owner")]]
    keyboard=InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def build_choose_org_keyboard(orgs,names):
    buttons = [[InlineKeyboardButton(text=name, callback_data=f"choose_org_{org_id}")] for org_id, name in zip(orgs,names)]
    buttons.append([InlineKeyboardButton(text="Назад", callback_data="owner")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def build_delete_org_keyboard(orgs,names):
    buttons = [[InlineKeyboardButton(text=name, callback_data=f"del_org_{org_id}")] for org_id, name in zip(orgs,names)]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def build_confirm_delete_org(org_id):
    buttons = [[InlineKeyboardButton(text="Да, удалить", callback_data=f"confirm_del_{org_id}")],
               [InlineKeyboardButton(text="Отмена", callback_data="cancel_del")]]
    print(buttons)
    keyboard = InlineKeyboardMarkup(inline_keyboard = buttons)
    return keyboard
