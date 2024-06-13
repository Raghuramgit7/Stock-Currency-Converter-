from flask import Flask
import os
from index import index_bp
from conversion import conversion_bp

app = Flask(__name__)  # Initialize the Flask app

# Register the blueprints

app.register_blueprint(index_bp, url_prefix='/')
app.register_blueprint(conversion_bp, url_prefix='/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
