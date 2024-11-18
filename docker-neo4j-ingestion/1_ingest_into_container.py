# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 16:06:23 2024

@author: abhi-
"""

from python_on_whales import docker
import time

# so you may have to delete the data folder each run (in the likely case the overwrite doesnt work properly)

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

# Neo4j import command
import_command = [
    "bin/neo4j-admin", "database", "import", "full",
    "--nodes=import/nodes-header.csv,import/nodes-part.*",
    "--relationships=import/edges-header.csv,import/edges-part.*",
    "--overwrite-destination=true", "neo4j"
]
tmp = "bin/neo4j-admin database import full --verbose --overwrite-destination=true --nodes=import/nodes-header.csv,import/nodes-part.* --relationships=import/edges-header.csv,import/edges-part.* neo4j"

# import_command = ["bin/neo4j-admin", " database", "import", "incremental", 
#     "--nodes=import/nodes-header.csv,import/nodes-part.*",
#     "--relationships=import/edges-header.csv,import/edges-part.*","neo4j"]

# tmp = "bin/neo4j-admin database import incremental --nodes=import/nodes-header.csv,import/nodes-part.* --relationships=import/edges-header.csv,import/edges-part.* neo4j"

if __name__ == "__main__":
    try:
        # delete existing container
        docker.container.remove('neo4j_container_test', force=True)
        time.sleep(10)
    except:
        pass
    
    # running in detached mode
    docker.run(
        neo4j_image,
        command=import_command,
        publish=publish,
        volumes=volumes,
        envs=environment,
        detach=True,
        name=container_name,
    )
    
    print("finished ingestion into container")
    
    # so this does succesfully do the import but then closes the container (starting back up the container also shuts down momentarily (unclear if it tries reimport))
    # for now this is ok because the /data bind mount created on the host OS has the ingested dbms files needed for recreating the container