# DOCKERFILE: TODO - Change the Python Version

# Change once we know what python version we will use
FROM python:3.6-slim-buster

# Create a directory that the app runs inside for the container
# This creates a folder for us to use in docker
WORKDIR /app

# Copy the requirements into the workdir
COPY requirements.txt ./

# install all the packages from the requirements.txt file
RUN pip install -r requirements.txt

# Copy all to the workdir
COPY . .

# Expose the port that the docker container will run on
EXPOSE 4000

# Prompts CMD to run the flask app
CMD [ "flask", "run", "--host=0.0.0.0", "--port=4000"]