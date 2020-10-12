import os
from flask import Blueprint, request, session, url_for, render_template, redirect, Flask


from views.users import user_blueprint
from views.topics import topic_blueprint
from views.posts import post_blueprint

app = Flask(__name__)
app.secret_key = "zd7FfDE4kzswDB9@nA85KAkaBSpgzxS"
app.config.update(
    ADMIN=os.environ.get('ADMIN')
)

app.register_blueprint(user_blueprint)
app.register_blueprint(topic_blueprint)
app.register_blueprint(post_blueprint)


@app.route('/')
def index():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
