import os
from aiogram.client.bot import DefaultBotProperties

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

DEFAULT_PROPERTIES = DefaultBotProperties(parse_mode="HTML")

WORK_HOURS = {
    "Tue-Thu": (17, 22),
    "Fri-Sat": (12, 24),
    "Sun": (14, 21)
}

DISABLED_WEEKDAYS = [0]  # Понедельники
DISABLED_DATES = ["12-30", "12-31"]

MENU_IMAGES = {
    "drinks": ["https://noah.restaurant/gallery_gen/1a289eb3de5be339938d7bc787125e05_fit.png?ts=1759702499"],
    "food": [
        "https://noah.restaurant/gallery_gen/dfbf30aaeb714b24c7154b9b0e5cc94c_fit.png?ts=1759702499",
        "https://noah.restaurant/gallery_gen/00fb7298434206f6c51ac398cec1fdf2_fit.png?ts=1759702499"
    ],
    "wine": ["https://noah.restaurant/gallery_gen/3fcbc262a17e81f9cf8cdb5fe858af7e_1190x1686_fit.png?ts=1759702500"]
}

DELIVERY_URL = "https://noah.restaurant/gallery_gen/3bf9a752abdd58a44a5558d0f7a7a2c1_520x693.22055953155_fill.jpeg"
WELCOME_IMAGE = "https://noah.restaurant/gallery_gen/472c2c8e08a077627a5cd409e6e533e3_520x693.671875_fill.jpeg"
SPECIAL_IMAGE = "https://noah.restaurant/gallery_gen/f8092ec44f3c1b4dbcefd714dc03232b_669.66015625x502_fill.jpg"