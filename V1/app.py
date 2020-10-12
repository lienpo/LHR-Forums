import os
from flask import Flask, render_template

from views.posts import post_blueprint
from views.topics import topic_blueprint
from views.users import user_blueprint

app = Flask(__name__)
app.secret_key = "zd7FfDE4kzswDB9@nA85KAkaBSpgzxS"
app.config.update(
    ADMIN=os.environ.get('ADMIN')
)

app.register_blueprint(post_blueprint, url_prefix="/posts")
app.register_blueprint(topic_blueprint, url_prefix="/topics")
app.register_blueprint(user_blueprint, url_prefix="/user")


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)

