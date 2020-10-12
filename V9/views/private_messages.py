
from flask import Blueprint, request, session,  render_template

from models.user import User
from models.private_message import Private_Message
from models.user import requires_login

pm_blueprint = Blueprint('pms', __name__)


@pm_blueprint.route('/private_messages/<string:receiver>/<string:sender>', methods=['GET', 'POST'])
@requires_login
def send_a_pm(receiver: str, sender: str):
    receiver_object = User.get_by_username(receiver)
    sender_object = User.get_by_username(sender)

    if request.method == 'POST':
        subject = request.form['subject']
        content = request.form['content']

        message = Private_Message(subject, content, sender_object.id, receiver_object.id)
        message.save()

        return render_template('private_messages/confirmation_of_message.html', receiver=receiver_object)
    return render_template('private_messages/send_message.html', receiver=receiver_object)


@pm_blueprint.route('/mailbox/<string:username>', methods=['GET', 'POST'])
@requires_login
def my_mailbox(username):
    user_to = User.get_by_username(username)
    if user_to.i_have_mail(user_to.id):
        my_messages = Private_Message.all_my_messages(user_to.id)
        users_from = Private_Message.all_my_senders(user_to.id)
        return render_template('private_messages/my_mailbox.html', messages=my_messages, users_from=users_from)
    return render_template('private_messages/no_mail.html', you=user_to)


@pm_blueprint.route('/mailbox/<string:sender_name>/<int:message_id>')
@requires_login
def read_message(sender_name, message_id):
    message = Private_Message.get_message_by_id(message_id)
    sender = User.get_by_username(sender_name)
    Private_Message.set_as_saved(message_id)
    return render_template('/private_messages/read_message.html', sender=sender, message=message)


@pm_blueprint.route('/mailbox/<int:message_id>/<int:orig_sender_id>', methods=['GET', 'POST'])
@requires_login
def reply_to_message(message_id: int, orig_sender_id: int):
    sender = User.get_by_id(orig_sender_id)
    receiver = User.get_by_username(session['username'])
    original_message = Private_Message.get_message_by_id(message_id)
    if request.method == 'POST':
        # content = request.form['content']
        new_part_of_content = request.form['new_content_part']
        new_subject = "Re: " + original_message.subject
        full_content = """______________________________________________________________________________________________________ \n
        %s \n
        ______________________________________________________________________________________________________ \n
        %s
        """ % (original_message.content, new_part_of_content)

        message_to = receiver.id
        message_from = sender.id

        new_message = Private_Message(new_subject, full_content, message_to, message_from)
        new_message.save()

        return render_template('private_messages/confirmation_of_message.html', receiver=sender)
    return render_template('private_messages/reply.html', current_sender=sender, current_receiver=receiver, original_message=original_message)


@pm_blueprint.route('/delete_message/<int:message_id>/<int:orig_sender_id>')
@requires_login
def delete_mail(message_id, orig_sender_id):
    user_to = User.get_by_id(orig_sender_id)

    that_message = Private_Message.get_message_by_id(message_id)
    me = User.get_by_id(that_message.user_to)

    Private_Message.delete_message(message_id)

    my_messages = Private_Message.all_my_messages(me.id)
    users_from = Private_Message.all_my_senders(me.id)
    return render_template('private_messages/my_mailbox.html', user_to=me, messages=my_messages, users_from=users_from)
