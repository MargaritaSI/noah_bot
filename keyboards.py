from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import date, timedelta

# Главное меню
main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/info"), KeyboardButton(text="/book")],
        [KeyboardButton(text="/menu"), KeyboardButton(text="/delivery")],
        [KeyboardButton(text="/special_booking")]
    ],
    resize_keyboard=True
)


# Календарь с навигацией
def calendar_kb(year: int, month: int, offset: int = 0):
    """Генерирует календарь на месяц с учетом offset"""
    buttons = []

    # Вычисляем целевой месяц
    first_day = date(year, month, 1)
    target_date = first_day + timedelta(days=30 * offset)
    target_year = target_date.year
    target_month = target_date.month

    # ДОБАВИТЬ: Название месяца
    month_names = [
        "", "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
        "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
    ]
    month_year_text = f"{month_names[target_month]} {target_year}"

    # ДОБАВИТЬ: Строка с названием месяца
    buttons.append([InlineKeyboardButton(text=month_year_text, callback_data="ignore")])

    # Дни недели
    weekdays = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    buttons.append([InlineKeyboardButton(text=w, callback_data="ignore") for w in weekdays])

    # Первый и последний день месяца
    first = date(target_year, target_month, 1)
    if target_month == 12:
        last = date(target_year + 1, 1, 1) - timedelta(days=1)
    else:
        last = date(target_year, target_month + 1, 1) - timedelta(days=1)

    # Пустые кнопки до первого дня недели
    empty_days = first.weekday()
    current_row = [InlineKeyboardButton(text=" ", callback_data="ignore") for _ in range(empty_days)]

    # Заполняем календарь
    for day in range(1, last.day + 1):
        current = date(target_year, target_month, day)

        # Проверка на неактивные даты
        is_disabled = (
                current.weekday() == 0 or  # Понедельники
                (current.month == 12 and current.day in [30, 31]) or  # 30-31 декабря
                current < date.today()  # Прошедшие даты
        )

        if is_disabled:
            btn = InlineKeyboardButton(text=f"❌{day}", callback_data="ignore")
        else:
            btn = InlineKeyboardButton(
                text=str(day),
                callback_data=f"date:{target_year}:{target_month}:{day}"
            )

        current_row.append(btn)

        # Переход на новую строку после воскресенья
        if len(current_row) == 7:
            buttons.append(current_row)
            current_row = []

    # Добавляем последнюю строку, если не заполнена
    if current_row:
        while len(current_row) < 7:
            current_row.append(InlineKeyboardButton(text=" ", callback_data="ignore"))
        buttons.append(current_row)

    # Кнопки навигации
    nav_buttons = []
    if offset < 3:
        if offset == 0:
            nav_buttons.append(InlineKeyboardButton(text="Следующий месяц ▶️", callback_data=f"cal_nav:{offset + 1}"))
        elif offset == 1:
            nav_buttons.append(InlineKeyboardButton(text="◀️ Текущий", callback_data=f"cal_nav:{offset - 1}"))
            nav_buttons.append(InlineKeyboardButton(text="Через месяц ▶️", callback_data=f"cal_nav:{offset + 1}"))
        else:
            nav_buttons.append(InlineKeyboardButton(text="◀️ Назад", callback_data=f"cal_nav:{offset - 1}"))
            if offset < 3:
                nav_buttons.append(InlineKeyboardButton(text="Дальше ▶️", callback_data=f"cal_nav:{offset + 1}"))
    else:
        nav_buttons.append(InlineKeyboardButton(text="◀️ Назад", callback_data=f"cal_nav:{offset - 1}"))

    if nav_buttons:
        buttons.append(nav_buttons)

    return InlineKeyboardMarkup(inline_keyboard=buttons)


# Выбор количества людей
def people_kb():
    buttons = []
    row = []
    for i in range(1, 10):
        row.append(InlineKeyboardButton(text=str(i), callback_data=f"people:{i}"))
        if i % 3 == 0:
            buttons.append(row)
            row = []

    # Кнопка для больших групп
    buttons.append([InlineKeyboardButton(text="Больше 9 человек?", callback_data="people:more")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


# Время слоты в зависимости от дня недели
def time_kb(selected_date: date):
    """
    Генерирует слоты времени в зависимости от дня недели
    Вт–Чт: 17:00–22:00
    Пт–Сб: 12:00–24:00
    Вс: 14:00–21:00
    """
    weekday = selected_date.weekday()
    buttons = []

    if weekday in [1, 2, 3]:  # Вт-Чт
        hours = range(17, 23)  # 17:00-22:00
    elif weekday in [4, 5]:  # Пт-Сб
        hours = range(12, 25)  # 12:00-24:00
    elif weekday == 6:  # Вс
        hours = range(14, 22)  # 14:00-21:00
    else:
        hours = []  # Понедельник - не должно попасть сюда

    row = []
    for hour in hours:
        time_str = f"{hour:02d}:00"
        row.append(InlineKeyboardButton(text=time_str, callback_data=f"time:{hour}"))
        if len(row) == 4:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    return InlineKeyboardMarkup(inline_keyboard=buttons)


# Кнопка подтверждения бронирования
def confirm_kb():
    buttons = [
        [
            InlineKeyboardButton(text="✏️ Изменить дату", callback_data="change:date"),
            InlineKeyboardButton(text="✏️ Изменить людей", callback_data="change:people"),
        ],
        [
            InlineKeyboardButton(text="✏️ Изменить время", callback_data="change:time"),
        ],
        [
            InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm:booking")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# Меню (напитки, еда, вино)
def menu_kb():
    buttons = [
        [InlineKeyboardButton(text="🍹 Напитки", callback_data="menu:drinks")],
        [InlineKeyboardButton(text="🍽 Еда", callback_data="menu:food")],
        [InlineKeyboardButton(text="🍷 Винная карта", callback_data="menu:wine")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Выбор пола
def gender_kb():
    buttons = [
        [
            InlineKeyboardButton(text="👨 Мужской", callback_data="gender:male"),
            InlineKeyboardButton(text="👩 Женский", callback_data="gender:female")
        ],
        [InlineKeyboardButton(text="🧑 Другое", callback_data="gender:other")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)