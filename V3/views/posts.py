import json
from flask import Blueprint, render_template, request, url_for, session

from models.topic import Topic
from models.post import Post
from models.user import User
from models.user import requires_login

post_blueprint = Blueprint('posts', __name__)


@post_blueprint.route('/topics/<string:topic_title>/new_post', methods=['GET', 'POST'])
@requires_login
def new_post(topic_title):
    topic = Topic.get_by_title(topic_title)

    if request.method == 'POST':
        content = request.form['content']
        creator_name = session['username']

        creator = User.get_by_username(creator_name)

        post = Post(content, topic.id, creator.id)
        post.save()

    return render_template('/topics/view_topic.html', topic=topic)


