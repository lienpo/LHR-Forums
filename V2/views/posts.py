from models.user.user import User
from models.topic import Topic
from models.post import Post

import views.topics as topics
import views.users as users


def list_all_posts():
    print("___POSTS___")
    for post in Post.all():
        post_creator = User.get_by_id(post.user_id)
        post_topic = Topic.get_by_id(post.topic_id)
        print(f"Created by {post_creator.username} in {post_topic.title} on {post.origin}")
        print(f"{post.content}")


def prompt_new_post():
    content = input("Enter content: ")

    users.list_all_users()
    creator_name = input("Enter your username: ")
    topics.list_all_topics()
    topic_name = input("Enter the topic you want to reply in: ")

    if User.does_user_exist(creator_name) and Topic.does_topic_exist(topic_name):
        creator = User.get_by_username(creator_name)
        creator_id = creator.id

        containing = Topic.get_by_title(topic_name)
        containing_id = containing.id

        post = Post(content, containing_id, creator_id)
        post.save()
    elif not(creator_name in User.all_usernames()):
        print("Sorry, that is not username is not valid.")
    elif not(topic_name in Topic.give_all_topicnames()):
        print("Sorry, that topic does not exist.")