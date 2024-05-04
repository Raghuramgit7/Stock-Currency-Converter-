from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import gbmodel
import uuid

class Sign(MethodView):
    def get(self):
        return render_template('sign.html')

    def post(self):
        """
        Accepts POST requests, and processes the form;
        Redirect to index when completed.
        """
        
        row_id = str(uuid.uuid4())
        print(row_id)
        model = gbmodel.get_model()
        model.insert(row_id, request.form['quote'], request.form['name'], request.form['dateofquote'], request.form['sourcetype'], request.form['sourcequote'], request.form['rating'])
        return redirect(url_for('index'))
