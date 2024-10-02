# routes/page_routes.py

from flask import Blueprint, render_template

bp = Blueprint('page_routes', __name__)

@bp.route('/')
def homepage():
    # Render an HTML template (index.html) located in the templates folder
    return "Hello World!"
