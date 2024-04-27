from flask import render_template, request, url_for, redirect
from flask.views import MethodView
import gbmodel

class Update(MethodView):
    def post(self):
        model = gbmodel.get_model()
        # id = request.form.get('id') 

        updated_entry = {
            'id' : request.form['id'],
            'quote' : request.form['quote'],
            'name' : request.form['name'],
            'dateofquote' : request.form['dateofquote'],
            'sourcetype' : request.form['sourcetype'],
            'sourcequote' : request.form['sourcequote'],
            'rating' : request.form['rating']
        }
            


        model = gbmodel.get_model()
        model.update(updated_entry)
        
        entries = [dict(id=row[0], quote=row[1], name=row[2], dateofquote=row[3], sourcetype=row[4], sourcequote=row[5], rating=row[6] ) for row in model.select()]
        
        render_template('entries.html',entries=entries)
        return redirect(url_for('entries'))
