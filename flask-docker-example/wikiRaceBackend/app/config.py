import os

class Config:
    # Basic settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')  # Secret key for session management and security
    DEBUG = os.getenv('DEBUG', False)  # Debug mode for development
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///default.db')  # Default to a local SQLite database
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking for performance benefits

    # CORS settings
    CORS_HEADERS = 'Content-Type'

    # Other optional configurations
    JSONIFY_PRETTYPRINT_REGULAR = True  # Prettify JSON responses for readability
