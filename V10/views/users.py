from flask import Blueprint, request, session,  render_template

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


@user_blueprint.route('/profile/<string:viewer_name>/<string:viewee_name>')
def profile(viewer_name, viewee_name):
    try:
        if session['username'] != None:
            viewee = User.get_by_username(viewee_name)
            viewer = User.get_by_username(viewer_name)
            return render_template('users/profile.html', viewer=viewer, viewee=viewee)
    except UserErrors.NoUserRegistered as e:
        return e.message('You need to be logged in to view this page.')
    return render_template('home.html')

@user_blueprint.route('/logout')
def logout():
    session['username'] = "guest"
    return render_template('home.html')
