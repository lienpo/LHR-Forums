from flask import Blueprint, render_template, request, redirect, url_for, session

from models.topic import Topic
from models.post import Post
from models.user import User
from models.user import requires_login

topic_blueprint = Blueprint('topics', __name__)


@topic_blueprint.route('/')
def index():
    topics = Topic.all()
    return render_template('topics/index.html', topics=topics)


@topic_blueprint.route('/new', methods=['GET', 'POST'])
@requires_login
def new_topic():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        creator_name = session['username']

        creator = User.get_by_username(creator_name)

        topic = Topic(title, content, creator.id)
        topic.save()
    return render_template('topics/new_topic.html')


@topic_blueprint.route('/view_topic/<string:topic_title>')
def view_topic(topic_title):
    topic = Topic.get_by_title(topic_title)
    posts = Post.all_in_topic(topic.id)
    users = Topic.users_in_topic(topic.id)
    return render_template('topics/view_topic.html', topic=topic, posts=posts, users=users)
