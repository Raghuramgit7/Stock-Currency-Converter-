"""
A simple guestbook flask app.
"""
import flask
from flask.views import MethodView
from index import Index
from sign import Sign
from entries import Entries

app = flask.Flask(__name__)       # our Flask app

app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods=["GET"])

app.add_url_rule('/sign',
                 view_func=Sign.as_view('sign'),
                 methods=['GET', 'POST'])
app.add_url_rule('/entries',
                 view_func=Entries.as_view('entries'),
                 methods=['GET', 'POST'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
