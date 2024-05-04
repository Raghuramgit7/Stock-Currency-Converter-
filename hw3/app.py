"""
A simple guestbook flask app.
"""
import flask
from flask.views import MethodView
from index import Index
from get import Get
from sign import Sign
from entries import Entries
from update import Update

from delete import Delete
 

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

app.add_url_rule('/get',
                 view_func=Get.as_view('get'),
                 methods=['POST'])
app.add_url_rule('/update',
                 view_func=Update.as_view('update'),
                 methods=['GET', 'POST'])

app.add_url_rule('/delete',
                 view_func=Delete.as_view('delete'),
                 methods=['POST'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
