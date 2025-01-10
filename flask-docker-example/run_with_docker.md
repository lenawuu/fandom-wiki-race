# Running the Docker Container

To run the docker container on your machine, you will need to have `postgres`, `docker` and `docker-compose` installed (and maybethe Docker Desktop App and `docker-machine`, I'm not 100% sure).

Once the container is ready to test, run the following commands:

- `docker-compose build flaskapp`: This builds the app. You must be in the parent directory (for now this is `/flask-docker-example`)
- `docker compose up -d flaskapp`: This starts the app and runs the container while allowing you to have access to the current shell.
- `docker ps -a` shows current docker instances that are running. You should see one labeled `flaskapp` and one labeled `postgres` or `postgresql`.

To test the Postgres Database instance:

- Running `docker exec -it db psql -U postgres` will open the PostgreSQL instance and you can use SQL commands like `select * from games;` to view data in each table. To view the top level of the database, use `\dt` to list all the tables.

## Testing the Backend with React Frontend

- After running the `docker compose up -d flaskapp`, the container will start and the backend is live. The ports that the backend is using are found in `/flask-docker-example/flaskapp/flask.dockerfile`.

- I have created 2 dummy endpoints with hardcoded games to access. These are found in `/flask-docker-example/flaskapp/app.py`, and are `test_get_game_by_id` and `test_get_all_games`. `get_game_by_id` is how we pull the game for the player, and takes an ID as an argument(test ID's are 1 and 2), and `get_all_games` is to display a list of games, similar to how you can access old wordles/connections/daily games. They will return a hardcoded game or games in the schema the database will spit out.
