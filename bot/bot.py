#bot/bot.py
from sqlalchemy import func
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from .database import SessionLocal
from .models import Quote, Log

# Функция для отправки приветственного сообщения с клавиатурой
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    keyboard = [
        [KeyboardButton("/quote")]  # Кнопка, которая отправляет команду /quote
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)

    await update.message.reply_text('Привет! Я бот для отправки случайных цитат.', reply_markup=reply_markup)

# Функция для отправки случайной цитаты
async def random_quote(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /quote"""
    
    # Создаем сессию для работы с БД
    session = SessionLocal()

    # Получаем случайную цитату из базы данных
    quote = session.query(Quote).order_by(func.random()).first()  # выбираем случайную цитату

    if quote:
        await update.message.reply_text(f'"{quote.text}" — {quote.author}')
        
        # Логируем исходящее сообщение
        log = Log(tg_id=update.effective_user.id, action='OUTGOING')
        session.add(log)
        session.commit()

    else:
        # Если цитат нет в базе данных, отправляем сообщение
        await update.message.reply_text("Извините, цитаты пока нет в базе данных.")
        
    # Логируем входящее сообщение
    incoming_log = Log(tg_id=update.effective_user.id, action='INCOMING')
    session.add(incoming_log)
    session.commit()

    session.close()  # Закрываем сессию