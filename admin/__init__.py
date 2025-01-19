#admin/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

# Загружаем переменные окружения из .env
load_dotenv()

# Инициализация приложений
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:////{os.path.abspath('./quotes.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from bot.models import User

@login_manager.user_loader
def load_user(user_id):
    """Загружает пользователя по ID"""
    return User.query.get(int(user_id))

from . import routes

