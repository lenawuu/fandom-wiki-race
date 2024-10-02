from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
#from .routes import user_routes, other_routes
from .routes import page_routes
#from .models import user_model

# Initialize the database
db = SQLAlchemy()

def create_app():
    # Create the Flask app instance
    app = Flask(__name__)
    
    # Load configuration settings
    app.config.from_object('app.config.Config')

    # Enable CORS for cross-origin requests
    CORS(app)

    # Initialize the database with the app
    db.init_app(app)

    # Register blueprints for modular routing
    # app.register_blueprint(user_routes.bp)
    # app.register_blueprint(other_routes.bp)
    app.register_blueprint(page_routes.bp)

    return app
