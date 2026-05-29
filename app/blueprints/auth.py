from flask import Blueprint, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.forms import RegisterForm, LoginForm
from app.models import User, MovieList
from app.utils import login_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data.lower()).first():
            flash('E-mail já cadastrado.', 'danger')
            return redirect(url_for('auth.register'))
        user = User(name=form.name.data.strip(), email=form.email.data.lower(), password_hash=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        for list_name in ['Assistir depois', 'Favoritos']:
            db.session.add(MovieList(name=list_name, user_id=user.id))
        db.session.commit()
        flash('Cadastro realizado com sucesso. Faça login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if not user or not check_password_hash(user.password_hash, form.password.data):
            flash('E-mail ou senha inválidos.', 'danger')
            return redirect(url_for('auth.login'))
        session['user_id'] = user.id
        flash('Login realizado com sucesso.', 'success')
        return redirect(url_for('movies.dashboard'))
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    session.clear()
    flash('Você saiu da conta.', 'info')
    return redirect(url_for('main.index'))
