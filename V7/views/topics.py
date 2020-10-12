from flask import Blueprint, request, session, url_for, render_template, redirect

from models.topic import Topic
from models.post import Post
from models.user import User
from models.user import requires_login
from models.section import Section

topic_blueprint = Blueprint('topics', __name__)


@topic_blueprint.route('/topics')
def index():
    topics = Topic.all()
    users = User.all()
    return render_template('topics/index.html', topics=topics, users=users)


@topic_blueprint.route('/new_topic', methods=['GET', 'POST'])
@requires_login
def new_topic(section):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        creator_name = session['username']

        creator = User.get_by_username(creator_name)

        topic = Topic(title, content, creator.id, section.id)
        topic.save()
        topics = Topic.all()

        creator = User.get_by_id(section.user_id)
        topics = Topic.all_in_section(section.id)
        users = User.all()
        return render_template('sections/view.html', topics=topics)

    return render_template('topics/new_topic.html', section=section)


@topic_blueprint.route('/view_topic/<string:topic_title>')
def view_topic(topic_title):
    topic = Topic.get_by_title(topic_title)
    posts = Post.all_in_topic(topic.id)
    users = User.all()
    return render_template('topics/view_topic.html', topic=topic, posts=posts, users=users)
