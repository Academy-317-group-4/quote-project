import os
import threading
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler
from bot.bot import start, random_quote  # Импортируем функции из bot.py
from bot.database import init_db  # Импортируем функцию инициализации базы данных
from admin import app

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение токена из переменных окружения
token = os.getenv("TELEGRAM_TOKEN")

def run_flask():
    """Запуск Flask-приложения"""
    app.run(host='0.0.0.0', port=5002)

def run_telegram_bot():
    """Запуск Telegram-бота"""
    if token is None:
        raise ValueError("Token not found. Please check your .env file.")
    
    # Инициализация базы данных, если она еще не была инициализирована
    init_db()

    # Создаем объект Application с токеном
    application = Application.builder().token(token).build()

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("quote", random_quote))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    # Запуск Flask-приложения в отдельном потоке
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Запуск Telegram-бота
    run_telegram_bot()
