import os
from flask import Blueprint, request, session, url_for, render_template, redirect, Flask

from models.section import Section
from models.user import User
from models.private_message import Private_Message
import common.database as Database
from common.connection_pool import get_connection

with get_connection() as connection:
    Database.create_tables(connection)


user_to = User.get_by_username("friendlyel")
my_messages = Private_Message.all_my_messages(user_to.id)
users_from = Private_Message.all_my_senders(user_to.id)

for message in my_messages:
    for sender in users_from:
        if sender.id == message.user_from:
            print(sender.username + " --- " + message.subject)