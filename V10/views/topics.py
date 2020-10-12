from flask import Blueprint, request, session,  render_template

from models.topic import Topic
from models.post import Post
from models.user import User
from models.user import requires_login
from models.section import Section

topic_blueprint = Blueprint('topics', __name__)


@topic_blueprint.route('/topics')
def index():
    topics = Topic.all()
    return render_template('topics/index.html', topics=topics)


@topic_blueprint.route('/new_topic/<string:section_title>', methods=['GET', 'POST'])
@requires_login
def new_topic(section_title):
    section = Section.get_by_title(section_title)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        creator_name = session['username']

        topic = Topic(title, content, creator_name, section.id)
        topic.save()
        topics = Topic.all_in_section(section.id)
        creator = User.get_by_username(topic.creator_name)
        return render_template('sections/view_section.html', section=section, topics=topics, creator=creator)

    return render_template('topics/new_topic.html', section=section)


@topic_blueprint.route('/view_topic/<string:topic_title>')
def view_topic(topic_title):
    topic = Topic.get_by_title(topic_title)
    posts = Post.all_in_topic(topic.id)
    return render_template('topics/view_topic.html', topic=topic, posts=posts)
