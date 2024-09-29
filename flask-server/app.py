from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS to allow the frontend to communicate with the backend



if __name__ == '__main__':
    app.run(port=5000, debug=True)