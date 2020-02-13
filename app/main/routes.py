import os

from flask import flash, render_template, redirect, url_for
from flask import send_from_directory, request, current_app
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import db
from app.models.auth import User
from app.main.forms import LoginForm, RegistrationForm, NewBookForm
from app.main.controller import UserInterface

from app.main import bp


@bp.route('/index')
@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@bp.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    form = NewBookForm()
    if form.validate_on_submit():
        ui = UserInterface(current_user)
        ui.add_book(title=form.data['title'])
        return redirect('/')
    return render_template('quickform.html', form=form)
    

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash(f'Logging out')
    return redirect(url_for('main.index'))
    

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

    
@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'), 'favicon.png')