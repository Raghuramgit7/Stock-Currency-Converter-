from flask import render_template
from flask.views import MethodView
import gbmodel

class Index(MethodView):
    def get(self):
        model = gbmodel.get_model()
        entries = [dict(quote=row[0], name=row[1], dateofquote=row[2], sourcetype=row[3], sourcequote=row[4], rating=row[5] ) for row in model.select()]
        return render_template('index.html',entries=entries)
