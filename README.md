# Noah Lieven Telegram Bot

Telegram бот для ресторана Noah Lieven с функциями бронирования столиков, просмотра меню и доставки.

## Возможности

- 🤖 Приветствие с изображением
- 📅 Система бронирования столиков с календарем
- 📋 Просмотр меню (напитки, еда, винная карта)
- 🚚 Информация о доставке
- 🎉 Специальные бронирования для мероприятий
- 📞 Контактная форма с отправкой данных администратору
- 🔗 Webhook поддержка для продакшена

## Технологии

- **Python 3.11** - основной язык
- **aiogram 3.22.0** - Telegram Bot API
- **FastAPI 0.118.0** - веб-фреймворк для webhook
- **uvicorn** - ASGI сервер
- **Docker** - контейнеризация
- **Docker Compose** - оркестрация

## Быстрый старт

### 1. Клонирование и настройка

```bash
git clone <repository-url>
cd noach
cp .env .env
```

### 2. Настройка переменных окружения

Создайте файл `.env` на основе примера:

```bash
cp .env .env
```

Отредактируйте файл `.env` и укажите ваши данные:

```env
BOT_TOKEN=your_telegram_bot_token_here
ADMIN_CHAT_ID=123456789
WEBHOOK_URL=https://yourdomain.com
```

**⚠️ Важно:** Файл `.env` содержит секретные данные и не должен попадать в Git репозиторий!

### 3. Запуск в режиме разработки

```bash
# С Docker Compose
docker-compose -f docker-compose.dev.yml up --build

# Или локально
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python main.py
```

### 4. Запуск в продакшене

```bash
# С Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# Или с помощью скрипта
./deploy.sh prod
```

## Структура проекта

```
noach/
├── main.py                 # Основной файл бота
├── requirements.txt        # Python зависимости
├── Dockerfile             # Docker образ
├── docker-compose.dev.yml # Docker Compose для разработки
├── docker-compose.prod.yml# Docker Compose для продакшена
├── nginx.conf            # Nginx конфигурация
├── .dockerignore         # Исключения для Docker
├── .gitignore           # Исключения для Git
├── env.example           # Пример переменных окружения
├── deploy.sh            # Скрипт развертывания
└── README.md             # Документация
```

## Git и безопасность

### Файлы, которые НЕ попадают в репозиторий:
- `.env` - содержит секретные токены и пароли
- `venv/` - виртуальное окружение Python
- `__pycache__/` - кэш Python
- `.DS_Store` - системные файлы macOS
- `*.log` - файлы логов
- `ssl/` - SSL сертификаты

### Файлы для настройки после клонирования:
1. Скопируйте `env.example` в `.env`
2. Заполните секретные данные в `.env`
3. Создайте виртуальное окружение: `python -m venv venv`

## Переменные окружения

| Переменная | Описание | Обязательная |
|------------|----------|--------------|
| `BOT_TOKEN` | Токен Telegram бота | ✅ |
| `ADMIN_CHAT_ID` | ID чата администратора | ✅ |
| `WEBHOOK_URL` | URL для webhook | ✅ |
| `HOST` | Хост сервера (по умолчанию: 0.0.0.0) | ❌ |
| `PORT` | Порт сервера (по умолчанию: 8080) | ❌ |
| `START_IMAGE_URL` | URL изображения приветствия | ❌ |
| `MENU_*_URL` | URL изображений меню | ❌ |
| `DELIVERY_IMAGE_URL` | URL изображения доставки | ❌ |
| `SPECIAL_IMAGE_URL` | URL изображения специальных бронирований | ❌ |

## Команды бота

- `/start` - Приветствие и основное меню
- `/info` - Информация о ресторане (часы работы, адрес, контакты)
- `/book` - Бронирование столика
- `/menu` - Просмотр меню
- `/delivery` - Информация о доставке
- `/special_booking` - Специальные бронирования

## Развертывание

### Docker

```bash
# Сборка образа
docker build -t noach-bot .

# Запуск контейнера
docker run -d \
  --name noach-bot \
  -p 8080:8080 \
  --env-file .env \
  noach-bot
```

### Docker Compose

```bash
# Разработка
docker-compose -f docker-compose.dev.yml up --build

# Продакшен
docker-compose -f docker-compose.prod.yml up -d

# Или используйте скрипт
./deploy.sh dev    # для разработки
./deploy.sh prod   # для продакшена
```

### Google Cloud Run

1. Соберите Docker образ
2. Загрузите в Google Container Registry
3. Разверните в Cloud Run с переменными окружения

### AWS Lambda (с Mangum)

Бот поддерживает Mangum для совместимости с AWS Lambda.

## Мониторинг

- Health check endpoint: `GET /healthz`
- Логи доступны через `docker logs noach-bot`

## Безопасность

- Использование non-root пользователя в Docker
- Rate limiting через Nginx
- SSL/TLS поддержка
- Security headers
- Валидация входных данных

## Разработка

### Установка зависимостей для разработки

```bash
pip install -r requirements.txt
```

### Линтеры и форматирование

```bash
# Форматирование кода
black main.py

# Сортировка импортов
isort main.py

# Проверка стиля
flake8 main.py
```

### Тестирование

```bash
pytest
```

## Поддержка

Для вопросов и поддержки обращайтесь к администратору бота или создайте issue в репозитории.

## Лицензия

MIT License
