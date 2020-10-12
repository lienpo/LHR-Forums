from flask import Blueprint, request, session, url_for, render_template, redirect

from common.utils import Utils
from models.user import User, UserErrors

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        try:
            if User.register_user(username, email, password):
                session['username'] = username
                return render_template('home.html')
        except UserErrors.UserError as e:
            return e.message
    return render_template('users/register.html')


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            if User.is_login_valid(username, password):
                session['username'] = username
                return render_template('home.html')
        except UserErrors.UserError as e:
            return e.message
    return render_template('users/login.html')


@user_blueprint.route('/profile/<string:username>')
def profile(username: str):
    user = User.get_by_username(username)
    return render_template('users/profile.html', user=user)


@user_blueprint.route('/logout')
def logout():
    session['username'] = None
    return render_template('home.html')