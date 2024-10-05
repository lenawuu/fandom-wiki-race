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
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def json(self):
        return {'id':self.id, 'name':self.name, 'email':self.email}
    
class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.String(100), unique=False, nullable=False)
    end = db.Column(db.String(100), unique=False, nullable=False)
    route = db.Column(db.String(200), unique=True, nullable=False)

    def json(self):
        return {'id':self.id, 'start':self.start, 'end':self.end, 'route':self.route}

db.create_all()

########################################################################################################################
# GAME CRUD ROUTES::
# - We Need...
#   - Get Game By ID (for pulling the game of the day)
#   - Get All Games (to have a list of routes/races from previous days)
#   - Create Game (make a new game with the graph database) -> Not totally sure how to put this together rn...
#     - Start Here: https://stackoverflow.com/questions/68151318/make-an-api-call-from-one-container-to-another
#   - Update Game (to change a route if the wiki is updated)
#   - Delete Game
########################################################################################################################

# CREATE GAME(S)::

@app.route('/api/game')
def create_game():
    try:
        data = request.get_json()
        new_game = Game(start=data['start'], end=data['end'], route=data['route'])
        db.session.add(new_game)
        db.session.commit()

        return jsonify({
            'id':new_game.id,
            'start':new_game.start,
            'end':new_game.end,
            'route':new_game.route,
        }), 201

    except Exception as e:
        return make_response(jsonify({'message':'error creating game', 'error':str(e)}), 500)


# READ GAME(S)::

@app.route('/api/game', methods=['GET'])
def get_all_games():
    try:
        games = Game.query.all()
        games_data = [{'id': game.id, 'start': game.start, 'end': game.end, 'route': game.route} for game in games] # put everything in a json
        return jsonify(games_data), 200
    except Exception as e:
        return make_response(jsonify({'message':'error getting games', 'error':str(e)}), 500)


@app.route('/api/game/<id>', methods=['GET'])
def get_game_by_id(id):
    try:
        game = Game.query.filter_by(id=id).first() # pull the first Game with a matching ID from the db

        if game: #if the game exists
            return make_response(jsonify({'game':game.json()}), 200)

        return make_response(jsonify({'message':f'game {id} not found'}), 404)

    except Exception as e:
        return make_response(jsonify({'message':f'error getting game {id}', 'error':str(e)}), 500)
    
# UPDATE GAME(S)::

@app.route('/api/game/<id>', methods=['PUT'])
def update_game_by_id(id):
    try:
        game = Game.query.filter_by(id=id).first()

        if game:
            data = request.get_json()
            game.start = data['start']
            game.end = data['end']
            game.route = data['route']
            db.session.commit()
            return make_response(jsonify({'message':f'game {id} updated'}), 200)
        
        return make_response(jsonify({'message':f'game {id} not found'}), 404)

    except Exception as e:
        return make_response(jsonify({'message':f'error getting game {id}', 'error':str(e)}), 500)

# DELETE GAME(S)::

@app.route('/api/game/<id>', methods=['DELETE'])
def delete_game_by_id(id):
    try:
        game = Game.query.filter_by(id=id).first()

        if game:
            db.session.delete(game)
            db.session.commit
            return make_response(jsonify({'message':f'game {id} was deleted'}), 200)
        
        return make_response(jsonify({'message':f'game {id} does not exit'}), 404)

    except Exception as e:
        return make_response(jsonify({'message':f'error deleting game {id}', 'error':str(e)}), 500)

########################################################################################################################
# SAMPLE CRUD ROUTES::
########################################################################################################################

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message':'The Server is Running!'})

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
