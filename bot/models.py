#bot/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from admin import db


class Quote(db.Model):
    __tablename__ = 'quotes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    author = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)

class Log(db.Model):
    __tablename__ = 'logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(Integer, nullable=False)
    action = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)

class User(db.Model, UserMixin):
    __tablename__ = 'users'  # Убедитесь, что имя таблицы указано правильно
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)