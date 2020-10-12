from common.connection_pool import get_connection
import common.database as Database
import views.users as users
import views.topics as topics
import views.posts as posts


DATABASE_PROMPT = "Enter the DATABASE_URI value or leave empty to load from .env file:"
MENU_PROMPT = """---MENU ---

1) CREATE NEW USER
2) CREATE NEW TOPIC
3) CREATE NEW POST
4) SEE ALL USERS
5) SEE ALL TOPICS
6) SEE ALL TOPICS BY USER
7) SEE ALL POSTS BY USER
8) SEE ALL POSTS IN TOPIC
9) EXIT

ENTER YOUR CHOICE:
"""
NEW_OPTION_PROMPT = "ENTER NEW OPTION TEXT (OR LEAVE EMPTY TO STOP ADDING OPTIONS): "

MENU_OPTIONS = {
    "1": users.prompt_new_user,
    "2": topics.prompt_new_topic,
    "3": posts.prompt_new_post,
    "4": users.list_all_users,
    "5": topics.list_all_topics,
    "6": users.list_all_topics_by_user,
    "7": users.list_all_posts_by_user,
    "8": topics.list_posts_in_topic
}


def menu():
    with get_connection() as connection:
        Database.create_tables(connection)

    while(selection := input(MENU_PROMPT)) != "9":
        try:
            MENU_OPTIONS[selection]()
        except KeyError:
            print("Invalid input selected. Please try again.")


menu()
