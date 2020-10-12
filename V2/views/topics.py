from models.user.user import User
from models.topic import Topic
from models.post import Post

import views.users as users


def list_all_topics():
    print("___TOPICS ___")
    for topic in Topic.all():
        topic_creator = User.get_by_id(topic.user_id)
        print(f"{topic.id}. {topic.title}: Started by {topic_creator.username} on {topic.origin}")


def list_posts_in_topic(topic_id):
    topic_name = Topic.get_by_id(topic_id).title
    print(topic_name)
    print("----------------------------------------------------------")
    for post in Post.all_in_topic(topic_id):
        post_creator = User.get_by_id(post.user_id)
        print(f"Created by {post_creator.username} in {post.origin}")
        print(f"{post.content}")
    print("-----------------------------------------------------------")


def prompt_new_topic():
    title = input("Enter title: ")
    content = input("Enter content: ")

    users.list_all_users()
    creator_name = input("Enter your username")
    if User.does_user_exist(creator_name):
        creator = User.get_by_username(creator_name)
        creator_id = creator.id
        topic = Topic(title, content, creator_id)
        topic.save()
    else:
        print("Sorry, that is not username is not valid.")