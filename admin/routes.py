# admin/routes.py
from flask import render_template, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from . import app, db
from bot.models import User, Quote, Log
from .forms import LoginForm
from datetime import datetime
from sqlalchemy import func, case
import matplotlib.pyplot as plt
import io
import base64

@app.route('/')
@login_required
def index():
    return render_template('index.html', current_user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/quotes')
@login_required
def quotes():
    if current_user.role != 'manager' and current_user.role != 'director':
        return redirect(url_for('index'))
    
    quotes = Quote.query.all()
    return render_template('quotes.html', quotes=quotes)

@app.route('/add_quote', methods=['POST'])
@login_required
def add_quote():
    if current_user.role != 'manager' and current_user.role != 'director':
        return redirect(url_for('quotes'))
    
    text = request.form['text']
    author = request.form['author']
    
    new_quote = Quote(text=text, author=author)
    db.session.add(new_quote)
    db.session.commit()
    
    return redirect(url_for('quotes'))

@app.route('/delete_quote/<int:id>', methods=['POST'])
@login_required
def delete_quote(id):
    if current_user.role != 'manager' and current_user.role != 'director':
        return redirect(url_for('quotes'))
    
    quote = Quote.query.get(id)
    db.session.delete(quote)
    db.session.commit()
    
    return redirect(url_for('quotes'))

@app.route('/stats')
@login_required
def stats():
    if current_user.role != 'director':
        return redirect(url_for('index'))

    # Статистика по отправленным и полученным сообщениям
    logs = db.session.query(
        func.date(Log.created_date).label('date'),
        func.sum(case((Log.action == 'OUTGOING', 1), else_=0)).label('sent_count'),
        func.sum(case((Log.action == 'INCOMING', 1), else_=0)).label('received_count')
    ).group_by(func.date(Log.created_date)).all()

    dates = [str(log.date) for log in logs]  # Изменено здесь
    sent_counts = [int(log.sent_count) for log in logs]  # Добавлено приведение к int
    received_counts = [int(log.received_count) for log in logs]  # Добавлено приведение к int

    # Статистика сообщений по пользователям
    user_stats = db.session.query(
        Log.tg_id,
        func.count(Log.id).label('message_count')
    ).group_by(Log.tg_id).order_by(func.count(Log.id).desc()).limit(10).all()

    user_ids = [str(stat.tg_id) for stat in user_stats]  # Приведение к строке
    user_message_counts = [int(stat.message_count) for stat in user_stats]  # Приведение к int

    return render_template('stats.html', 
                           dates=dates, 
                           sent_counts=sent_counts, 
                           received_counts=received_counts,
                           user_ids=user_ids,
                           user_message_counts=user_message_counts)