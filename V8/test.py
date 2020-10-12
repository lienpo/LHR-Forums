import os
from flask import  session,  render_template,  Flask

from common.connection_pool import get_connection

with get_connection() as connection:
    database.create_tables(connection)

app = Flask(__name__)
app.secret_key = "zd7FfDE4kzswDB9@nA85KAkaBSpgzxS"
app.config.update(
    ADMIN=os.environ.get('ADMIN')
)

@app.route('/')
def home():
    if not session.get('is_login'):
        session["username"] = "guest"
    if not session.get('is_login'):
        switch = "0"
    else:
        switch = "1"
    return render_template('test.html', switch=switch)


if __name__ == '__main__':
    app.run(debug=True)