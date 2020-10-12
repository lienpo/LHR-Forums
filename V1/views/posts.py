import json
from flask import Blueprint, render_template, request, redirect, url_for, session

from models.post import Post
from models.topic import Topic
from models.user import User
from models.user import requires_login

post_blueprint = Blueprint('posts', __name__)

@requires_login
@post_blueprint.route('/topics/<string:topic_name>/new_post', methods=['GET', 'POST'])
def new_post(topic_name):
    if request.method == 'POST':
        content = request.form['content']
        topic_name = topic_name
        creator = session['username']

        Topic.add_post(content, topic_name, creator)
    return('/topics/<string:topic_name>')