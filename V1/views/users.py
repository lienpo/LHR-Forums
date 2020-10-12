from flask import Blueprint, request, session, url_for, render_template, redirect
from models.user import User, UserErrors

user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        try:
            User.register_user(username, email, password)
            session['username'] = username
            return username
        except UserErrors.UserError as e:
            return e.message

    return render_template('users/register.html')


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.user_already_exists(username, password):
            session['username'] = username
            return username
        else:
            session['username'] = None
            return None
    return render_template('users/login.html')


@user_blueprint.route('/logout')
def logout_user():
    session['username'] = None
    return render_template('home.html')

@user_blueprint.route('/profile')
def profile():
    return render_template('users/profile.html')