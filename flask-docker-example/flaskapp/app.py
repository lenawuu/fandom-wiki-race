# TODO: Write Dummy Endpoints to test with Frontend
# TODO: Change DB to match new schema
# We need...
#   - Get Game By ID
#   - Get All Games

from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_cors import CORS
from os import environ

app = Flask(__name__)
CORS(app) # Enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://test.db'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def json(self):
        return {'id':self.id, 'name':self.name, 'email':self.email}

# REDO: CHANGE SCHEMA TO MATCH NEW VALS
''' THIS IS THE OLD VERSION, NEW VERSION IS BELOW
class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.String(100), unique=False, nullable=False)
    end = db.Column(db.String(100), unique=False, nullable=False)
    route = db.Column(db.String(200), unique=True, nullable=False)


    def json(self):
        return {'id':self.id, 'start':self.start, 'end':self.end, 'route':self.route}
'''

# NEW SCHEMA
#   - Uses a 3NF Form to store arrays (Location is for start and end)

class Game(db.Model):
    __tablenameA__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    fandom_domain = db.Column(db.String(100), nullable=False)
    route_length = db.Column(db.Integer, nullable=False)

    # Connected to the Locations Table via foreign Key
    start_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    end_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    start = relationship("Location", foreign_keys=[start_id], backref="games_start")
    end = relationship("Location", foreign_keys=[end_id], backref="games_end")

    # Connect to the Route via a SQLAlchemy.orm.relationship method
    route = relationship("Route", back_populates="game", cascade="all, delete-orphan")

    # Return the new version of the Tables as a JSON:
    def json(self):
        return {
            "id": self.id,
            "start": {"title": self.start.title, "url": self.start.url},
            "end": {"title": self.end.title, "url": self.end.url},
            "route": {
                "titles": [route.title for route in self.route],
                "urls": [route.url for route in self.route]
            },
            "fandom_domain": self.fandom_domain,
            "route_length": self.route_length
        }

# Locations Store the Start and Endpoints of a Game
class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500), nullable=False)

# Routes Store a single route and are stored as a series of ID's in the Game Table,
#   and a Route row in this table is just a URL used in the route
class Route(db.Model):
    __tablename__ = 'routes'
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500), nullable=False)

    game = relationship("Game", back_populates="route")

with app.app_context():
    db.create_all()

########################################################################################################################
# TESTING CRUD ROUTES::
# - We Need...
#   - Get Game By ID (for pulling the game of the day, id will be 1)
#   - Get All Games (for listing all previous games on the frontend)

            ################################################################################################

# HARD-CODED OUTPUTS FOR FRONTEND TESTING:
test_game_1 = {
    "id": 1,
    "start": {
        "title": "Item",
        "url": "https://mariokart.fandom.com/wiki/Item"
    },
    "end": {
        "title": "Pianta",
        "url": "https://mariokart.fandom.com/wiki/Pianta"
    },
    "route": {
        "titles": [
            "Item",
            "Mario Kart 8 Deluxe",
            "Pianta"
        ],
        "urls": [
            "https://mariokart.fandom.com/wiki/Item",
            "https://mariokart.fandom.com/wiki/Mario_Kart_8_Deluxe",
            "https://mariokart.fandom.com/wiki/Pianta"
        ]
    },
    "fandom_domain": "mariokart.fandom.com",
    "route_length": 2
}

test_game_2 = {
    "id": 2,
    "start": {
        "title": "ATV",
        "url": "https://mariokart.fandom.com/wiki/ATV"
    },
    "end": {
        "title": "Mario Kart Arcade GP VR",
        "url": "https://mariokart.fandom.com/wiki/Mario_Kart_Arcade_GP_VR"
    },
    "route": {
        "titles": [
            "ATV",
            "Princess Peach",
            "Mario Kart Arcade GP VR"
        ],
        "urls": [
            "https://mariokart.fandom.com/wiki/ATV",
            "https://mariokart.fandom.com/wiki/Princess_Peach",
            "https://mariokart.fandom.com/wiki/Mario_Kart_Arcade_GP_VR"
        ]
    },
    "fandom_domain": "mariokart.fandom.com",
    "route_length": 2
}

games = list()
games.append(test_game_1)
games.append(test_game_2)

            ################################################################################################

# TEST ROUTES - REPLACE IN FRONTEND
@app.route('/api/test_game', methods=['GET'])
def test_get_all_games():
    try:
        return make_response(jsonify(games), 200)
    except Exception as e:
        return make_response(jsonify({'message':'error getting games', 'error':str(e)}), 500)


@app.route('/api/test_game/<id>', methods=['GET'])
def test_get_game_by_id(id):
    try:
        if (id==0 or id=='0'):
            game = games[0]
        elif (id==1 or id=='1'):
            game=games[1]
        else:
            return make_response(jsonify({'message':f'game {id} not found'}), 404)

        return make_response(jsonify({'game':dict(game)}), 200)

    except Exception as e:
        return make_response(jsonify({'message':f'error getting game {id}', 'error':str(e)}), 500)

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

# New Version of Game Creation to Match the New Schema
#   - This version checks if a Location or Route row exists in the db before creating it in the tables.
@app.route('/api/game', methods=['POST'])
def create_game():
    try:
        data = request.get_json(force=True)

        # Extract start and end locations
        start_data = data['start']
        end_data = data['end']

        # Check if start and end locations exist; otherwise, create them
        start = Location.query.filter_by(title=start_data['title'], url=start_data['url']).first()
        if not start:
            start = Location(title=start_data['title'], url=start_data['url'])
            db.session.add(start)

        end = Location.query.filter_by(title=end_data['title'], url=end_data['url']).first()
        if not end:
            end = Location(title=end_data['title'], url=end_data['url'])
            db.session.add(end)

        # Commit to get start and end IDs
        db.session.flush()

        # Create the game
        new_game = Game(
            start=start,
            end=end,
            fandom_domain=data['fandom_domain'],
            route_length=data['route_length']
        )
        db.session.add(new_game)
        db.session.flush()

        # Add route entries
        for title, url in zip(data['route']['titles'], data['route']['urls']):
            route_entry = Route(game_id=new_game.id, title=title, url=url)
            db.session.add(route_entry)

        # Commit everything
        db.session.commit()

        return jsonify(new_game.json()), 201

    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return make_response(jsonify({'message': 'error creating game', 'error': str(e)}), 500)



# READ GAME(S)::

# READ ALL GAMES
@app.route('/api/game', methods=['GET'])
def get_all_games():
    try:
        games = Game.query.all()
        games_data = [game.json() for game in games] # 12/20/24 - updated to just create a list of the json() method
        return jsonify(games_data), 200
    except Exception as e:
        return make_response(jsonify({'message':'error getting games', 'error':str(e)}), 500)

# READ GAME BY ID
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

        if not game:
            return make_response(jsonify({'message': f'game {id} not found'}), 404)

        data = request.get_json()

        # Update or create start location
        start_data = data['start']
        start = Location.query.filter_by(title=start_data['title'], url=start_data['url']).first()
        if not start:
            start = Location(title=start_data['title'], url=start_data['url'])
            db.session.add(start)
        game.start = start

        # Update or create end location
        end_data = data['end']
        end = Location.query.filter_by(title=end_data['title'], url=end_data['url']).first()
        if not end:
            end = Location(title=end_data['title'], url=end_data['url'])
            db.session.add(end)
        game.end = end

        # Update route: delete old entries and add new ones
        Route.query.filter_by(game_id=game.id).delete()  # Clear existing route entries
        for title, url in zip(data['route']['titles'], data['route']['urls']):
            new_route_entry = Route(game_id=game.id, title=title, url=url)
            db.session.add(new_route_entry)

        # Update other fields
        game.fandom_domain = data['fandom_domain']
        game.route_length = data['route_length']

        # Commit changes
        db.session.commit()
        return make_response(jsonify({'message': f'game {id} updated'}), 200)

    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return make_response(jsonify({'message': f'error updating game {id}', 'error': str(e)}), 500)


# DELETE GAME(S)::
@app.route('/api/game/<id>', methods=['DELETE'])
def delete_game_by_id(id):
    try:
        game = Game.query.filter_by(id=id).first()

        if not game:
            return make_response(jsonify({'message': f'game {id} does not exist'}), 404)

        # Delete the game (cascades to route entries)
        db.session.delete(game)
        db.session.commit()
        return make_response(jsonify({'message': f'game {id} was deleted'}), 200)

    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return make_response(jsonify({'message': f'error deleting game {id}', 'error': str(e)}), 500)


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
