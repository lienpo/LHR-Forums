from flask import Blueprint, request, session, url_for, render_template, redirect

post_blueprint = Blueprint('posts', __name__)


@post_blueprint.route('/new_post')
def new_post():
    return render_template('posts/new_post.html')