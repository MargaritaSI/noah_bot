import os
import logging
from datetime import date, datetime
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, URLInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, ADMIN_ID, DEFAULT_PROPERTIES, MENU_IMAGES, DELIVERY_URL, WELCOME_IMAGE, SPECIAL_IMAGE
from keyboards import main_menu_kb, calendar_kb, people_kb, time_kb, confirm_kb, menu_kb
from states import BookingStates, SpecialBookingStates

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота
bot = Bot(token=BOT_TOKEN, default=DEFAULT_PROPERTIES)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# ==========================
# Команды
# ==========================
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()

    text = (
        "Добро пожаловать в ресторан Noah! 🍽\n\n"
        "Для начала работы используйте команды в меню или введите /start"
    )

    try:
        # Отправляем приветственное изображение
        photo = URLInputFile(WELCOME_IMAGE)
        await message.answer_photo(photo=photo, caption=text, reply_markup=main_menu_kb)
    except Exception as e:
        logger.error(f"Ошибка загрузки приветственного изображения: {e}")
        await message.answer(text, reply_markup=main_menu_kb)


@dp.message(Command("info"))
async def info(message: Message):
    text = (
        "<b>📍 Наша информация</b>\n\n"
        "<b>График работы:</b>\n"
        "Пн – выходной \n"
        "Вт–Чт: 17:00–22:00\n"
        "Пт–Сб: 12:00–24:00\n"
        "Вс: 14:00–21:00\n\n"
        "<b>Адрес:</b> Rodenrijsstraat 150, 1062 JA Amsterdam\n"
        "<b>Телефон:</b> 020 896 0586\n"
        "<b>Почта:</b> info@noah.restaurant\n\n"
        "<b>Мы в соцсетях:</b>\n"
        "<a href='https://www.instagram.com/restaurantnoahlieven/'>Instagram</a> | <a href='https://www.facebook.com/profile.php?id=100088519935223'>Facebook</a>"
    )
    await message.answer(text, reply_markup=main_menu_kb)


@dp.message(Command("menu"))
async def menu_command(message: Message):
    await message.answer("🍽 <b>Наше меню:</b>", reply_markup=menu_kb())


@dp.callback_query(F.data.startswith("menu:"))
async def menu_callback(callback: CallbackQuery):
    menu_type = callback.data.split(":")[1]

    try:
        captions = {
            "drinks": "🍹 <b>Напитки</b>",
            "food": "🍽 <b>Еда</b>",
            "wine": "🍷 <b>Винная карта</b>"
        }

        images = MENU_IMAGES[menu_type]

        # Отправляем первое изображение с подписью
        photo = URLInputFile(images[0])
        await callback.message.answer_photo(
            photo=photo,
            caption=captions.get(menu_type, "Меню")
        )

        # Отправляем остальные изображения без подписи
        for img_url in images[1:]:
            photo = URLInputFile(img_url)
            await callback.message.answer_photo(photo=photo)

        await callback.answer()
    except Exception as e:
        logger.error(f"Ошибка загрузки изображения меню {menu_type}: {e}")
        await callback.answer("Не удалось загрузить изображение", show_alert=True)


@dp.message(Command("delivery"))
async def delivery(message: Message):
    text = (
        "🚚 <b>Доставка</b>\n\n"
        "Не успеваете зайти? Можно заказать доставку:\n"
        "мы на <a href='https://www.ubereats.com/nl-en/store/noah-lieven/D_L7W1XOTfyuEyQqmyQJmQ?diningMode=DELIVERY&pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMjNlJTIwS2VrZXJzdHJhYXQlMjIlMkMlMjJyZWZlcmVuY2UlMjIlM0ElMjJFaXN6WlNCTFpXdGxjbk4wY21GaGRDd2dNVEV3TkNCQmJYTjBaWEprWVcwc0lFNWxkR2hsY214aGJtUnpJaTRxTEFvVUNoSUo3WkdzT0c0TXhrY1JpWmcxWlZ2bVRFNFNGQW9TQ1ZWM21wUzFQOFpIRVkydndMZE1fUUJtJTIyJTJDJTIycmVmZXJlbmNlVHlwZSUyMiUzQSUyMmdvb2dsZV9wbGFjZXMlMjIlMkMlMjJsYXRpdHVkZSUyMiUzQTUyLjMxMzQyMyUyQyUyMmxvbmdpdHVkZSUyMiUzQTQuOTc5Mjg4JTdE'>Uber Eats</a> и "
        "<a href='https://www.thuisbezorgd.nl/menu/noah-lieven#pre-order'>Thuisbezorgd</a>"
    )

    try:
        photo = URLInputFile(DELIVERY_URL)
        await message.answer_photo(photo=photo, caption=text, reply_markup=main_menu_kb)
    except Exception as e:
        logger.error(f"Ошибка загрузки изображения доставки: {e}")
        await message.answer(text, reply_markup=main_menu_kb)


# ==========================
# Бронирование столика
# ==========================
@dp.message(Command("book"))
async def book_start(message: Message, state: FSMContext):
    await state.set_state(BookingStates.choosing_date)

    today = date.today()
    await message.answer(
        "📅 <b>Выберите дату бронирования:</b>",
        reply_markup=calendar_kb(today.year, today.month, offset=0)
    )


@dp.callback_query(F.data.startswith("cal_nav:"))
async def calendar_navigation(callback: CallbackQuery, state: FSMContext):
    offset = int(callback.data.split(":")[1])
    today = date.today()

    await callback.message.edit_reply_markup(
        reply_markup=calendar_kb(today.year, today.month, offset=offset)
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("date:"), BookingStates.choosing_date)
async def date_selected(callback: CallbackQuery, state: FSMContext):
    _, year, month, day = callback.data.split(":")
    selected_date = date(int(year), int(month), int(day))

    await state.update_data(date=selected_date)
    await state.set_state(BookingStates.choosing_people)

    await callback.message.edit_text(
        f"✅ Вы выбрали дату: <b>{selected_date.strftime('%d.%m.%Y')}</b>\n\n"
        "👥 <b>Выберите количество гостей:</b>",
        reply_markup=people_kb()
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("people:"), BookingStates.choosing_people)
async def people_selected(callback: CallbackQuery, state: FSMContext):
    people_count = callback.data.split(":")[1]

    if people_count == "more":
        await callback.answer(
            "Для бронирования на больше 9 человек, пожалуйста, свяжитесь с нами по телефону: 020 896 0586",
            show_alert=True
        )
        return

    data = await state.get_data()
    selected_date = data['date']

    await state.update_data(people=int(people_count))
    await state.set_state(BookingStates.choosing_time)

    await callback.message.edit_text(
        f"✅ Дата: <b>{selected_date.strftime('%d.%m.%Y')}</b>\n"
        f"✅ Гостей: <b>{people_count}</b>\n\n"
        "🕐 <b>Выберите время:</b>",
        reply_markup=time_kb(selected_date)
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("time:"), BookingStates.choosing_time)
async def time_selected(callback: CallbackQuery, state: FSMContext):
    hour = int(callback.data.split(":")[1])

    data = await state.get_data()
    selected_date = data['date']
    people = data['people']

    await state.update_data(time=hour)
    await state.set_state(BookingStates.confirming)

    await callback.message.edit_text(
        "📋 <b>Проверьте данные бронирования:</b>\n\n"
        f"📅 Дата: <b>{selected_date.strftime('%d.%m.%Y')}</b>\n"
        f"👥 Гостей: <b>{people}</b>\n"
        f"🕐 Время: <b>{hour:02d}:00</b>\n\n"
        "Вы можете изменить любой параметр или подтвердить бронирование:",
        reply_markup=confirm_kb()
    )
    await callback.answer()


# Изменение параметров
@dp.callback_query(F.data.startswith("change:"))
async def change_parameter(callback: CallbackQuery, state: FSMContext):
    param = callback.data.split(":")[1]
    data = await state.get_data()

    if param == "date":
        await state.set_state(BookingStates.choosing_date)
        today = date.today()
        await callback.message.edit_text(
            "📅 <b>Выберите новую дату:</b>",
            reply_markup=calendar_kb(today.year, today.month, offset=0)
        )
    elif param == "people":
        await state.set_state(BookingStates.choosing_people)
        await callback.message.edit_text(
            "👥 <b>Выберите количество гостей:</b>",
            reply_markup=people_kb()
        )
    elif param == "time":
        await state.set_state(BookingStates.choosing_time)
        selected_date = data['date']
        await callback.message.edit_text(
            "🕐 <b>Выберите время:</b>",
            reply_markup=time_kb(selected_date)
        )

    await callback.answer()


# Подтверждение и запрос контактов
@dp.callback_query(F.data == "confirm:booking", BookingStates.confirming)
async def confirm_booking(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BookingStates.entering_name)
    await callback.message.edit_text(
        "✅ <b>Отлично! Осталось заполнить контактные данные.</b>\n\n"
        "Пожалуйста, введите ваше имя:"
    )
    await callback.answer()


@dp.message(BookingStates.entering_name)
async def enter_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(BookingStates.entering_email)
    await message.answer("📧 Введите вашу почту:")


@dp.message(BookingStates.entering_email)
async def enter_email(message: Message, state: FSMContext):
    email = message.text

    # Простая валидация email
    if "@" not in email or "." not in email:
        await message.answer("❌ Пожалуйста, введите корректный email адрес:")
        return

    await state.update_data(email=email)
    await state.set_state(BookingStates.entering_phone)
    await message.answer("📱 Введите ваш телефон (с кодом страны, например +31...):")


@dp.message(BookingStates.entering_phone)
async def enter_phone(message: Message, state: FSMContext):
    phone = message.text

    # Простая валидация телефона
    if not phone.startswith("+") or len(phone) < 10:
        await message.answer("❌ Пожалуйста, введите телефон в формате +31...")
        return

    await state.update_data(phone=phone)
    await state.set_state(BookingStates.entering_telegram)

    # Получаем username пользователя
    user_telegram = message.from_user.username

    if user_telegram:
        # Если у пользователя есть username
        await message.answer(
            f"💬 Ваш Telegram: @{user_telegram}\n\n"
            "Телеграм контакт для подтверждения\n\n"
            f"Укажите свой '@{user_telegram}' или другой в подобном формате, если не хотите оставлять Telegram для подтверждения - напишите 'нет':"
        )
    else:
        # Если username нет
        await message.answer(
            "💬 Пожалуйста, укажите ваш Telegram никнейм для связи (например: @username):\n\n"
            "Или напишите 'нет', если не хотите оставлять Telegram."
        )


@dp.message(BookingStates.entering_telegram)
async def enter_telegram(message: Message, state: FSMContext):
    telegram_contact = message.text.strip()

    # Если пользователь не хочет оставлять telegram
    if telegram_contact.lower() in ['нет', 'no', '-']:
        telegram_contact = "Не указан"
    # Добавляем @ если забыли
    elif telegram_contact and not telegram_contact.startswith('@'):
        telegram_contact = f"@{telegram_contact}"

    await state.update_data(telegram=telegram_contact)

    # Получаем все данные
    data = await state.get_data()

    # Отправляем подтверждение пользователю
    user_message = (
        "✅ <b>Спасибо! Ваше бронирование отправлено.</b>\n\n"
        f"📅 Дата: {data['date'].strftime('%d.%m.%Y')}\n"
        f"🕐 Время: {data['time']:02d}:00\n"
        f"👥 Гостей: {data['people']}\n\n"
        "С вами свяжется администратор для подтверждения."
    )
    await message.answer(user_message, reply_markup=main_menu_kb)

    # Отправляем данные админу
    user_id = message.from_user.id
    user_username = message.from_user.username
    user_link = f"<a href='tg://user?id={user_id}'>Написать пользователю</a>"

    telegram_display = data.get('telegram', 'Не указан')
    if telegram_display != "Не указан" and telegram_display.startswith('@'):
        telegram_display = f"<a href='https://t.me/{telegram_display[1:]}'>{telegram_display}</a>"

    admin_message = (
        "🔔 <b>НОВОЕ БРОНИРОВАНИЕ!</b>\n\n"
        f"📅 Дата: {data['date'].strftime('%d.%m.%Y')}\n"
        f"🕐 Время: {data['time']:02d}:00\n"
        f"👥 Гостей: {data['people']}\n\n"
        f"👤 Имя: {data['name']}\n"
        f"📧 Email: {data['email']}\n"
        f"📱 Телефон: {data['phone']}\n"
        f"💬 Telegram: {telegram_display}\n\n"
        f"🔗 {user_link}\n"
        f"User ID: <code>{user_id}</code>"
    )
    if user_username:
        admin_message += f"\nUsername: @{user_username}"

    try:
        await bot.send_message(ADMIN_ID, admin_message)
    except Exception as e:
        logger.error(f"Ошибка отправки админу: {e}")

    await state.clear()


# ==========================
# Особенное бронирование
# ==========================
@dp.message(Command("special_booking"))
async def special_booking_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(SpecialBookingStates.entering_name)

    text = (
        "🎉 <b>Особенное мероприятие?</b>\n\n"
        "Для дня рождения, корпоративного ужина или группы — заполните форму:\n\n"
        "Пожалуйста, введите ваше имя:"
    )

    try:
        photo = URLInputFile(SPECIAL_IMAGE)
        await message.answer_photo(photo=photo, caption=text)
    except Exception as e:
        logger.error(f"Ошибка загрузки изображения: {e}")
        await message.answer(text)


@dp.message(SpecialBookingStates.entering_name)
async def special_enter_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(SpecialBookingStates.entering_email)
    await message.answer("📧 Введите вашу почту:")


@dp.message(SpecialBookingStates.entering_email)
async def special_enter_email(message: Message, state: FSMContext):
    email = message.text

    if "@" not in email or "." not in email:
        await message.answer("❌ Пожалуйста, введите корректный email адрес:")
        return

    await state.update_data(email=email)
    await state.set_state(SpecialBookingStates.entering_phone)
    await message.answer("📱 Введите ваш телефон (с кодом страны, например +31...):")


@dp.message(SpecialBookingStates.entering_phone)
async def special_enter_phone(message: Message, state: FSMContext):
    phone = message.text

    if not phone.startswith("+") or len(phone) < 10:
        await message.answer("❌ Пожалуйста, введите телефон в формате +31...")
        return

    await state.update_data(phone=phone)
    await state.set_state(SpecialBookingStates.entering_guests)
    await message.answer("👥 Укажите количество гостей:")


@dp.message(SpecialBookingStates.entering_guests)
async def special_enter_guests(message: Message, state: FSMContext):
    await state.update_data(guests=message.text)
    await state.set_state(SpecialBookingStates.entering_info)
    await message.answer("📝 Опишите ваше мероприятие (дата, время, особые пожелания):")


@dp.message(SpecialBookingStates.entering_info)
async def special_enter_info(message: Message, state: FSMContext):
    await state.update_data(info=message.text)

    data = await state.get_data()

    # Подтверждение пользователю
    user_message = (
        "✅ <b>Спасибо! Информация отправлена.</b>\n\n"
        "С вами свяжется администратор для обсуждения деталей."
    )
    await message.answer(user_message, reply_markup=main_menu_kb)

    # Отправка админу
    admin_message = (
        "🎉 <b>ЗАПРОС НА ОСОБЕННОЕ МЕРОПРИЯТИЕ!</b>\n\n"
        f"👤 Имя: {data['name']}\n"
        f"📧 Email: {data['email']}\n"
        f"📱 Телефон: {data['phone']}\n"
        f"👥 Гостей: {data['guests']}\n\n"
        f"📝 Дополнительная информация:\n{data['info']}\n\n"
        f"ID пользователя: {message.from_user.id}"
    )

    try:
        await bot.send_message(ADMIN_ID, admin_message)
    except Exception as e:
        logger.error(f"Ошибка отправки админу: {e}")

    await state.clear()


# Игнорирование кликов по неактивным кнопкам
@dp.callback_query(F.data == "ignore")
async def ignore_callback(callback: CallbackQuery):
    await callback.answer()


# ==========================
# Запуск бота
# ==========================
if __name__ == "__main__":
    import asyncio


    async def main():
        logger.info("Бот запущен...")
        await dp.start_polling(bot)


    asyncio.run(main())