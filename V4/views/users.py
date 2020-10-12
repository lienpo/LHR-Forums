from flask import Blueprint, request, session, url_for, render_template, redirect


user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/register')
def register_user():
    return render_template('users/register.html')


@user_blueprint.route('/login')
def login():
    return render_template('users/login.html')


@user_blueprint.route('/profile')
def profile():
    return render_template('users/profile.html')