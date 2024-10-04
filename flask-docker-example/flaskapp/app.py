from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

app = Flask(__name__)
CORS(app) # Enable CORS for all routes
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL') REPLACE WHEN DB IS SET UP
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://test.db'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.column(db.String(80), unique=True, nullable=False)
    email = db.column(db.String(120), unique=True, nullable=False)

    def json(self):
        return {'id':self.id, 'name':self.name, 'email':self.email}

db.create_all()

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message':'The Server is Running!'})

# SAMPLE CRUD ROUTES::

# CREATE
@app.route('/api/flask/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = User(name=data['name'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'id':new_user.id,
            'name':new_user.name,
            'email':new_user.email
        }), 201

    except Exception as e:
        return make_response(jsonify({'message':'error creating user', 'error':str(e)}), 500)

# READ
@app.route('/api/flask/users', methods=['GET'])
def get_all_users():
    try:
        users = User.query.all() # SQLAlchemy magic to get all Users from the DB
        users_data = [{'id': user.id, 'name': user.name, 'email': user.email} for user in users] # put everything in a json
        return jsonify(users_data), 200

    except Exception as e:
        return make_response(jsonify({'message':'error getting users', 'error':str(e)}), 500)

# READ (all)
@app.route('/api/flask/users/<id>', methods=['GET'])
def get_user_by_id(id):
    try:
        user = User.query.filter_by(id=id).first() # pull the first User with a matching ID

        if user: #if the user is not null
            return make_response(jsonify({'user':user.json()}), 200)

        return make_response(jsonify({'message':f'user {id} not found'}), 404)

    except Exception as e:
        return make_response(jsonify({'message':f'error getting user {id}', 'error':str(e)}), 500)

# UPDATE
@app.route('/api/flask/users/<id>', methods=['PUT'])
def update_user_by_id(id):
    try:
        user = User.query.filter_by(id=id).first()

        if user:
            data = request.get_json()
            user.name = data['name']
            user.email = data['email']
            db.session.commit()
            return make_response(jsonify({'message':f'user {id} updated'}), 200)
        
        return make_response(jsonify({'message':f'user {id} not found'}), 404)

    except Exception as e:
        return make_response(jsonify({'message':f'error getting user {id}', 'error':str(e)}), 500)

# DELETE
@app.route('/api/flask/users/<id>', methods=['DELETE'])
def delete_user_by_id(id):
    try:
        user = User.query.filter_by(id=id).first()

        if user:
            db.session.delete(user)
            db.session.commit
            return make_response(jsonify({'message':f'user {id} was deleted'}), 200)
        
        return make_response(jsonify({'message':f'user {id} does not exit'}), 404)

    except Exception as e:
        return make_response(jsonify({'message':f'error deleting user {id}', 'error':str(e)}), 500)
