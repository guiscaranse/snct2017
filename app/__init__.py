from flask import Flask
from flask_compress import Compress
# Initialize the app
app = Flask(
    __name__,
    template_folder='./templates',
    static_folder='./static/vendor',
    static_url_path='/vendor',
    instance_relative_config=True
)

# Views
from app import views
from app import gerencia
# Load the config file
app.config.from_object('config')
Compress(app)
