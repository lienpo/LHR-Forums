from flask import Blueprint, request, session,  render_template

from models.post import Post
from models.user import User
from models.reply import Reply
from models.user import requires_login

reply_blueprint = Blueprint('replies', __name__)


@requires_login
@reply_blueprint.route('reply/<int:post_id>', methods=['GET', 'POST'])
def new_reply(post_id: int):
    if request.method == 'POST':
        content = request.form['content']
        creator_name = session["username"]

        creator = User.get_by_username(creator_name)

        reply = Reply(content, post_id, creator.id)
        reply.save()

        replies = Post.all_replies(post_id)
        repliers = User.all()
        # topic=topic, posts=posts, users=users
        return render_template('replies/view_replies.html', replies=replies, repliers=repliers)

    return render_template('replies/new_reply.html', post_id=post_id)


@reply_blueprint.route('reply/<int:post_id>')
def view_replies(post_id: int):
    replies = Post.all_replies(post_id)
    repliers = Post.replying_users(post_id)
    return render_template('replies/view_replies.html', replies=replies, repliers=repliers)
