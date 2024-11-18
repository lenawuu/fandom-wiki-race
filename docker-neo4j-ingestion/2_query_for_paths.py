# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 16:09:28 2024

@author: abhi-
"""
from python_on_whales import docker
import time
from graphdatascience import GraphDataScience

NEO4J_URI = 'bolt://localhost:7687'
NEO4J_USER = 'neo4j'
NEO4J_PASSWORD = '12345678'

# grabbing latest version for simplicity
neo4j_image = "neo4j:latest"
container_name = "neo4j_container_test"
publish = [(7474, 7474), (7687, 7687)]

# mapping the windows paths to the container database paths (specifically for where to store import data and graphdb data)
volumes = {
    (r"D:\Users\abhi-\VH_Neo4jContainer\data", "/data"),
    (r"D:\Users\abhi-\VH_Neo4jContainer\import", "/var/lib/neo4j/import"),
}

environment = {
    "NEO4JLABS_PLUGINS": '["apoc", "graph-data-science"]', 
    "apoc.import.file.enabled": "true",
    "NEO4J_AUTH": "neo4j/12345678",  # basic password of 12345678
}

if __name__=="__main__":
    try:
        # delete existing container
        docker.container.remove('neo4j_container_test', force=True)
        time.sleep(10)
    except:
        pass
    
    # running in detached mode without an exec command
    docker.run(
        neo4j_image,
        publish=publish,
        volumes=volumes,
        envs=environment,
        detach=True,
        name=container_name,
    )
    
    time.sleep(60)
    container = docker.container.inspect(container_name)
    if container.state.running:
        print("container is running. attempting gds query")
        try:
            gds = GraphDataScience(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
            result = gds.run_cypher("MATCH (n) RETURN count(n) as totalNodes")
        finally:
            gds.close()