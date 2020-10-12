
from flask import Blueprint, request, session,  render_template

from models.topic import Topic
from models.post import Post
from models.user import User
from models.user import requires_login

post_blueprint = Blueprint('posts', __name__)


@post_blueprint.route('/posts/<string:topic_title>/new_post', methods=['GET', 'POST'])
@requires_login
def new_post(topic_title):
    topic = Topic.get_by_title(topic_title)

    if request.method == 'POST':
        content = request.form['content']
        creator_name = session['username']

        post = Post(content, topic.id, creator_name)
        post.save()

        posts = Post.all_in_topic(topic.id)

        return render_template('topics/view_topic.html', topic=topic, posts=posts)

    return render_template('posts/new_post.html')


@post_blueprint.route('/posts/<int:post_id>', methods=['GET', 'POST'])
@requires_login
def edit_post(post_id):
    if request.method == 'POST':
        content = request.form['content']

        post = Post.get_by_id(post_id)

        topic = Topic.containing_topic(post.topic_id)

        Post.edit_post(content, post_id)
        posts = Post.all_in_topic(topic.id)

        return render_template('topics/view_topic.html', topic=topic, posts=posts)
    return render_template('posts/edit_post.html', post_id=post_id)


@post_blueprint.route('/topics/<string:topic_title>/<int:post_id>', methods=['GET', 'POST'])
@requires_login
def delete_post(topic_title, post_id):
    topic = Topic.get_by_title(topic_title)

    Post.delete_post(post_id)
    posts = Post.all_in_topic(topic.id)
    return render_template('topics/view_topic.html', topic=topic, posts=posts)