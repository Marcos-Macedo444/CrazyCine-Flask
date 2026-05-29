from functools import wraps
from flask import session, flash, redirect, url_for
from .models import User


def current_user():
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None


def login_required(route):
    @wraps(route)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Faça login para acessar esta página.', 'warning')
            return redirect(url_for('auth.login'))
        return route(*args, **kwargs)
    return wrapper
