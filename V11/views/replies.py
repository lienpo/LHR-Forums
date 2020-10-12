from flask import Blueprint, request, session,  render_template
from models.post import Post
from models.user import User
from models.reply import Reply
from models.user import requires_login

# pm_blueprint = Blueprint('pms', __name__)
reply_blueprint = Blueprint('replies', __name__)


@requires_login
@reply_blueprint.route('/new_reply/<int:post_id>', methods=['GET', 'POST'])
def new_reply(post_id: int):
    if request.method == 'POST':
        content = request.form['content']

        reply = Reply(content, session['username'], post_id)
        reply.save()

        post = Post.get_by_id(post_id)
        replies = Reply.all_in_post(post_id)

        return render_template('replies/view_replies.html', post=post, replies=replies)

    return render_template('replies/new_reply.html', post_id=post_id)


@reply_blueprint.route('/reply/<int:post_id>')
def view_replies(post_id: int):
    post = Post.get_by_id(post_id)
    replies = Reply.all_in_post(post_id)

    return render_template('replies/view_replies.html', post=post, replies=replies)
