import asyncio
import logging
import sys
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

from Data import lecturers, courses, auditorium

TOKEN = "7168890234:AAGwl3pcVp-UAVx5ySoElaPIuAMm9QUZBME" #  5667733135:AAHOkpMzf7x2bhoFeyOUsLku0ogAX-Ka-CI
ADMIN_ID = 1134942813

bot = Bot(token=TOKEN)
dp = Dispatcher()

blocked_users = {737513135, 1518031594, 1365443499, 911414947, 1402667653, 6500022364, 1617787180}

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

alphabet = [chr(i) for i in range(ord('А'), ord('Я') + 1) if chr(i) not in ['Ъ', 'Ь', 'Ё', 'Ы', 'Й']]

active_users_file = "active_users.txt"

def save_user_id(user_id):
    try:
        if os.path.exists(active_users_file):
            with open(active_users_file, "r") as file:
                ids = file.read().splitlines()
        else:
            ids = []

        if str(user_id) not in ids:
            with open(active_users_file, "a") as file:
                file.write(f"{user_id}\n")
            logging.info(f"Добавлен новый пользователь: {user_id}")
        else:
            logging.info(f"Пользователь {user_id} уже существует в базе данных.")
    except Exception as e:
        logging.error(f"Ошибка при сохранении пользователя {user_id}: {e}")

def load_active_users():
    try:
        if os.path.exists(active_users_file):
            with open(active_users_file, "r") as file:
                return {int(line.strip()) for line in file}
        return set()
    except Exception as e:
        logging.error(f"Ошибка при загрузке активных пользователей: {e}")
        return set()

def create_letter_markup():
    
    keyboard = []
    for letter in alphabet:
        button = InlineKeyboardButton(text=letter, callback_data=f"letter_{letter}")
        keyboard.append(button)

    markup = InlineKeyboardMarkup(inline_keyboard=[keyboard[i:i + 5] for i in range(0, len(keyboard), 5)])
    return markup

def create_lecturer_markup(letter):
    keyboard = []
    for name, url in lecturers.items():
        if name.startswith(letter):
            web_app_info = WebAppInfo(url=url)
            button = InlineKeyboardButton(text=name, web_app=web_app_info)
            keyboard.append(button)

    if keyboard:
        markup = InlineKeyboardMarkup(inline_keyboard=[keyboard[i:i + 1] for i in range(0, len(keyboard), 1)])
    else:
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Нет преподавателей на эту букву", callback_data="no_lecturer")]
        ])
    return markup

def create_auditorium_markup(floor):
    keyboard = []
    for room, url in auditorium[floor].items():
        button = InlineKeyboardButton(text=room, web_app=WebAppInfo(url=url))
        keyboard.append(button)

    markup = InlineKeyboardMarkup(inline_keyboard=[keyboard[i:i + 2] for i in range(0, len(keyboard), 2)])
    return markup

def create_markup(course):
    keyboard = []
    for group, url in courses[course].items():
        button = InlineKeyboardButton(text=group, web_app=WebAppInfo(url=url))
        keyboard.append(button)

    markup = InlineKeyboardMarkup(inline_keyboard=[keyboard[i:i + 2] for i in range(0, len(keyboard), 2)])
    return markup

def create_main_menu():
    buttons = [
        [KeyboardButton(text='📚 Выбрать преподавателя'), KeyboardButton(text='🏫 Выбрать аудиторию')],
        [KeyboardButton(text='1️⃣ Курс 1'), KeyboardButton(text='2️⃣ Курс 2')],
        [KeyboardButton(text='3️⃣ Курс 3'), KeyboardButton(text='4️⃣ Курс 4')],
        [KeyboardButton(text='🌐 СДО', web_app=WebAppInfo(url="https://eluniver.ugrasu.ru/login/index.php")),
         KeyboardButton(text='👨‍💻 Связь с разработчиком', web_app=WebAppInfo(url="https://forms.gle/2L1MHuK7G7zApePPA"))],
        [KeyboardButton(text='⏰ Расписание звонков')]
    ]
    markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return markup


def log_user_activity(message: Message):
    try:
        user_id = message.from_user.id
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name if message.from_user.last_name else ''
        username = message.from_user.username if message.from_user.username else ''
        
        full_name = f"{first_name} {last_name}".strip() or username or f"ID {user_id}"
        logging.info(f"Пользователь с ID: {user_id}, Имя: {full_name}, отправил сообщение: '{message.text}'")

        save_user_id(user_id)
    except Exception as e:
        logging.error(f"Ошибка при логировании пользователя {user_id}: {e}")

def is_user_blocked(user_id):
    return user_id in blocked_users

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    try:
        user_id = message.from_user.id
        if is_user_blocked(user_id):
            await message.answer("Вы заблокированы и не можете использовать бота.")
            return

        markup = create_main_menu()
        log_user_activity(message)
        await message.answer("Привет! Выберите действие:", reply_markup=markup)
    except Exception as e:
        logging.error(f"Ошибка в command_start_handler: {e}")
        await message.answer("Произошла ошибка при запуске. Попробуйте снова.")

@dp.message()
async def handle_text_commands(message: Message) -> None:
    try:
        user_id = message.from_user.id
        if is_user_blocked(user_id):
            await message.answer("Вы заблокированы и не можете использовать бота.")
            return

        log_user_activity(message)
        text = message.text

        if text == '📚 Выбрать преподавателя':
            markup = create_letter_markup()
            await message.answer("Выберите первую букву фамилии преподавателя:", reply_markup=markup)
        elif text == '🏫 Выбрать аудиторию':
            floors_markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=floor, callback_data=f"floor_{floor}")] for floor in auditorium
            ])
            await message.answer("Выберите этаж:", reply_markup=floors_markup)
        elif text in ['4️⃣ Курс 4', '3️⃣ Курс 3', '2️⃣ Курс 2', '1️⃣ Курс 1']:
            course = text.split()[2]
            markup = create_markup(f"Курс{course}")
            await message.answer(f"Выберите группу {course} курса:", reply_markup=markup)
        elif text == '⏰ Расписание звонков':
            await bot.send_photo(chat_id=message.chat.id, photo=types.FSInputFile("sched.jpg"), caption="Вот ваше расписание звонков.")
        else:
            await message.answer("Извините, я не понимаю эту команду. Пожалуйста, выберите действие из меню. /start")

        if user_id == ADMIN_ID and text.startswith('/broadcast'):
            parts = text.split('/broadcast ', 1)
            if len(parts) == 2:
                message_text = parts[1]
                asyncio.create_task(broadcast_message(load_active_users(), message_text))
            else:
                await message.answer("Команда /broadcast должна содержать текст сообщения.")
    except Exception as e:
        logging.error(f"Ошибка в handle_text_commands: {e}")
        await message.answer("Произошла ошибка, попробуйте снова.")


async def broadcast_message(active_users, message_text):
    for user in active_users:
        try:
            await bot.send_message(user, f"Сообщение от администратора: {message_text}")
        except Exception as e:
            logging.error(f"Ошибка отправки сообщения пользователю {user}: {e}")

@dp.callback_query()
async def handle_callback_query(callback_query: types.CallbackQuery):
    try:
        user_id = callback_query.from_user.id
        if is_user_blocked(user_id):
            await callback_query.message.answer("Вы заблокированы и не можете использовать бота.")
            return

        data = callback_query.data
        if data.startswith("letter_"):
            letter = data.split("_")[1]
            markup = create_lecturer_markup(letter)
            await callback_query.message.answer(f"Преподаватели на букву {letter}:", reply_markup=markup)
        elif data.startswith("floor_"):
            floor = data.split("_")[1]
            markup = create_auditorium_markup(floor)
            await callback_query.message.answer(f"Аудитории на {floor} этаже:", reply_markup=markup)
        elif data == "no_lecturer":
            await callback_query.message.answer("Преподавателей на выбранную букву не найдено.")
    except Exception as e:
        logging.error(f"Ошибка в handle_callback_query: {e}")
        await callback_query.message.answer("Произошла ошибка, попробуйте снова.")

async def restart_bot():
    """Функция для автоматической перезагрузки бота каждые 2 минуты."""
    while True:
        await asyncio.sleep(300)
        logging.info("Перезагрузка бота...")
        try:
            os.execv(sys.executable, [sys.executable] + sys.argv)
        except Exception as e:
            logging.error(f"Ошибка при перезапуске бота: {e}")

async def main():
    try:
        await bot.delete_webhook(drop_pending_updates=True)

        asyncio.create_task(restart_bot())

        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Ошибка в main: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"Ошибка в основном блоке: {e}")
