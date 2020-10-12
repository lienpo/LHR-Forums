import os
from flask import     render_template,  Flask

import common.database as Database
from common.connection_pool import get_connection

with get_connection() as connection:
    Database.create_tables(connection)

app = Flask(__name__)
app.secret_key = "zd7FfDE4kzswDB9@nA85KAkaBSpgzxS"
app.config.update(
    ADMIN=os.environ.get('ADMIN')
)

@app.route('/')
def home():
    return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True)