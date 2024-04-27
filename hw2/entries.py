from flask import render_template
from flask.views import MethodView
import gbmodel

class Entries(MethodView):
    def get(self):
        model = gbmodel.get_model()
        entries = [dict(id=row[0], quote=row[1], name=row[2], dateofquote=row[3], sourcetype=row[4], sourcequote=row[5], rating=row[6] ) for row in model.select()]
        return render_template('entries.html',entries=entries)