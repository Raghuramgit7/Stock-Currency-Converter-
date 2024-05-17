from flask import render_template, request, url_for, redirect
from flask.views import MethodView
import gbmodel

class Get(MethodView):
    def post(self):
        model = gbmodel.get_model()
        id = request.form.get('id') 
        row = model.get(id)
        entry = [dict(id=row[0], quote=row[1], name=row[2], dateofquote=row[3], sourcetype=row[4], sourcequote=row[5], rating=row[6] )]
        print('entry: ',entry[0])
        return render_template('update_entry.html', entry=entry[0])
