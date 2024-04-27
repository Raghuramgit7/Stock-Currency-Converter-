from flask import render_template,request,url_for,redirect
from flask.views import MethodView
import gbmodel

class Delete(MethodView):
    def post(self):
        """
        Delete the record when the delete button is pressed
        """
        id = request.form.get('id') 
        model = gbmodel.get_model()
        model.delete(id)
        
        entries = [dict(id=row[0], quote=row[1], name=row[2], dateofquote=row[3], sourcetype=row[4], sourcequote=row[5], rating=row[6] ) for row in model.select()]
        render_template('entries.html',entries=entries)
        return redirect(url_for('entries'))

