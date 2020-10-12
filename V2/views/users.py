from models.user.user import User
from models.topic import Topic
from models.post import Post


def list_all_users():
    print("___ USERS ___")
    for user in User.all():
        print(f"{user.id}: {user.username}, (Member since {user.origin}")


def list_all_topics_by_user():
    list_all_users()
    username = input("Which user's topics are you wanting to look at?")
    if username in User.all_usernames():
        user = User.get_by_username(username)
        user_id = user.id
        all_topics = Topic.all_by_user(user_id)
        for topic in all_topics:
            print(f"{topic.id}. {topic.title}: Started on {topic.origin}")
    else:
        print("Sorry. That is not a valid username")


def list_all_posts_by_user():
    list_all_users()
    username = input("Which user's topics are you wanting to look at?")
    if username in User.all_usernames():
        user = User.get_by_username(username)
        user_id = user.id
        all_posts = Post.all_by_user(user_id)
        for post in all_posts:
            topic = Topic.get_by_id(post.topic_id)
            print(f"In {topic.title}: Written in {topic.origin}")
            print({post.content})
    else:
        print("Sorry. That is not a valid username")


def prompt_new_user():
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")

    user = User(username, email, password)
    user.save()