from flask import Blueprint, session, render_template, request, url_for, redirect

from models.topic import Topic
from models.post import Post
from models.user import requires_admin, requires_login

topic_blueprint = Blueprint('topic', __name__)


@topic_blueprint.route('/')
def index():
    topics = Topic.all_topics()
    return render_template('topics/all_topics', topics=topics)

@topic_blueprint.route('/new', methods=['GET', 'POST'])
@requires_login
def create_topic():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        creator = session['username']

        Topic(title, content, creator)

    return render_template('topics/new_topic.html')

@topic_blueprint.route('edit/<string:original_name>', methods=['GET', 'POST'])
@requires_login
def edit_topic(original_name: str):
    topic = Topic.get_by_name(original_name)

    if request.method == 'POST':
        new_title = request.form['title']
        new_content = request.form['content']

        Topic.edit_topic(original_name, new_title, new_content)

        return render_template(url_for('.index'))

    return render_template('topics/<string:original_name>.html', topic=topic)


@topic_blueprint.route('/<string:topic_name>')
def view_topic(topic_name: str):
    posts = Topic.posts(topic_name)
    return render_template('topics/<string:topic_name>.html', posts=posts)

@requires_login
@topic_blueprint.route('<string:topic_name>/new_post', methods=['GET', 'POST'])
def new_post(topic_name):
    if request.method == 'POST':
        content = request.form['content']
        topic_name = topic_name
        creator = session['username']

        Topic.add_post(content, topic_name, creator)
    return('/topics/<string:topic_name>')

@requires_login
@topic_blueprint.route('<string:topic_name>/<int:post_id>/edit_topic', methods=['GET', 'POST'])
def edit_post(topic_name: str, new_content: str, post_id: int):
    if request.method == 'POST':
        Post.edit_post(new_content, post_id)

    return('/topics/<string:topic_name>')
