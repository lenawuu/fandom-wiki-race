# Running the Docker Container

To run the docker container on your machine, you will need to have `postgres`, `docker` and `docker-compose` installed (and maybethe Docker Desktop App and `docker-machine`, I'm not 100% sure).

Once the container is ready to test, run the following commands:

- `docker-compose build flaskapp`: This builds the app. You must be in the parent directory (for now this is `/flask-docker-example`)
- `docker compose up -d flaskapp`: This starts the app and runs the container while allowing you to have access to the current shell.
- `docker ps -a` shows current docker instances that are running. You should see one labeled `flaskapp` and one labeled `postgres` or `postgresql`.

To test the Postgres Database instance:

- Running `docker exec -it db psql -U postgres` will open the PostgreSQL instance and you can use SQL commands like `select * from games;` to view data in each table. To view the top level of the database, use `\dt` to list all the tables.
