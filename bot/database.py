#bot/database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from admin import app, db

# Загружаем переменные окружения из .env
load_dotenv()

# Используем SQLite для базы данных
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./quotes.db')  # путь к файлу SQLite базы данных

# Создаем подключение к базе данных
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # параметр для работы с SQLite
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    print("Инициализация базы данных...")  # Отладочная информация
    with app.app_context():  # Создаем контекст приложения
        db.create_all() # Создание таблиц
    print("Таблицы созданы")  # Еще одна отладочная информация

