# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 15:11:36 2024

@author: abhi-
"""

# NOTE: script should be run whatever folder main.py is in 
import os
os.chdir("P:/Vandy Hacks 2024/DockerNeo4jTesting/basic_scraping_ingestion_merge")

from graphdatascience import GraphDataScience
from python_on_whales import docker
import time
import os
from os.path import join, dirname
from dotenv import load_dotenv


#https://stackoverflow.com/questions/41546883/what-is-the-use-of-python-dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

neo4j_image = os.getenv("NEO4J_IMAGE")
container_name = os.getenv("CONTAINER_NAME")
publish = [tuple(map(int, port.split(":"))) for port in os.getenv("PUBLISH_PORTS").split(",")]
volumes = {
    tuple(volume.split(":")) for volume in [os.getenv("VOLUME_DATA"), os.getenv("VOLUME_IMPORT")]
}
environment = {
    "NEO4JLABS_PLUGINS": os.getenv("NEO4JLABS_PLUGINS"),
    "apoc.import.file.enabled": os.getenv("APOC_IMPORT_FILE_ENABLED"),
    "NEO4J_AUTH": os.getenv("NEO4J_AUTH")
}
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")



import_command = [
    "bin/neo4j-admin", "database", "import", "full",
    "--nodes=import/nodes-header.csv,import/nodes-part.*",
    "--relationships=import/edges-header.csv,import/edges-part.*",
    "--overwrite-destination=true", "neo4j"
]

from DockerNeo4jTesting.basic_scraping_ingestion_merge.scraping_main import main as scraping
if __name__ == "__main__":
    
    scraping()
    
    
    # Try to remove the container if it already exists
    try:
        docker.container.remove(container_name, force=True)
    except:
        pass    
    
    #Spin up the container with the ingestion import command
    docker.run(
        neo4j_image,
        command=import_command,
        publish=publish,
        volumes=volumes,
        envs=environment,
        detach=True,
        name=container_name,
    )

    # Wait for the container to complete the import (checks every 5 secs)
    while True:
        container = docker.container.inspect(container_name)
        if not container.state.running:
            print("Ingestion complete. Container stopped")
            break
        time.sleep(5)
    
    ### At this point container should have imported and shut down
    try:
        # delete existing container
        docker.container.remove('neo4j_container_test', force=True)
        # TODO : replace with an container extistance check every 5 secs before continuing
        time.sleep(10)
    except:
        pass
    
    # Spin up container in detached mode without an exec command
    docker.run(
        neo4j_image,
        publish=publish,
        volumes=volumes,
        envs=environment,
        detach=True,
        name=container_name,
    )
    
    # Wait until the container is running
    while True:
        container = docker.container.inspect(container_name)
        if container.state.running:
            print("Container is running. Proceeding with GDS query")
            time.sleep(10) #Dont like this but I want to minimize the chance of a max retries for gds client
            break
        time.sleep(5)
        
    # Attempt the placeholder GDS query
    try:
        gds = GraphDataScience(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        result = gds.run_cypher("MATCH (n) RETURN count(n) as totalNodes")
        print(f"found {result['totalNodes'].tolist()[0]} nodes in the container's database")
    finally:
        gds.close()
        
    # TODO : identify the fandoms and create indexes for each (see notes in playground_path_finding_algs)