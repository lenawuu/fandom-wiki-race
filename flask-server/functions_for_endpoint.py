# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 00:31:54 2024

@author: abhi-
"""

from graphdatascience import GraphDataScience
import os 
os.environ['NEO4J_URI'] = 'bolt://localhost:7687'
os.environ['NEO4J_USER'] = 'neo4j'
os.environ['NEO4J_PASSWORD'] = 'letmeinplease'




# returns dataframe of two page's info
def get_two_random_pages(gds, domain):
    query = """
        MATCH(p:Page{domain:'""" + domain + """'})
        WITH min(p.wiki_id) as minId, max(p.wiki_id) as maxId
        WITH maxId, minId, floor(rand() * (maxId - minId + 1) + minId) AS randId1, floor(rand() * (maxId - minId + 1) + minId) AS randId2
        WHERE randId1 <> randId2
        MATCH (p1:Page {wiki_id: randId1,domain:'mariokart.fandom.com'}), (p2:Page {wiki_id: randId2,domain:'mariokart.fandom.com'})
        RETURN p1, p2
        LIMIT 1
        """
    result = gds.run_cypher(query)
    return(result)

# returns dataframe of true/false
def does_path_exist(gds, domain, wiki_id_1, wiki_id_2):
    query = """
        MATCH(p1:Page{wiki_id:toInteger("""+str(wiki_id_1)+""") ,domain:'"""+domain+"""'}),
        (p2:Page{wiki_id:toInteger("""+str(wiki_id_2)+""") , domain:'"""+domain+"""'})
        RETURN exists((p1)-[:HAS_LINK_TO*]-(p2)) AS pathExists
        """
    result = gds.run_cypher(query)
    return(result)

# returns complicated dataframe that had the correct path from start to end somewhere 
def get_shortest_path(gds, domain, wiki_id_1, wiki_id_2):
    query = """
        MATCH(p1:Page{wiki_id:toInteger("""+str(wiki_id_1)+""") ,domain:'"""+domain+"""'}),
        (p2:Page{wiki_id:toInteger("""+str(wiki_id_2)+""") , domain:'"""+domain+"""'})
        MATCH path=shortestPath((p1)-[:HAS_LINK_TO*..10]-(p2))
        RETURN path
        LIMIT 1
        """
    result = gds.run_cypher(query)
    return(result)
    

#hardcoded 
DOMAIN = 'mariokart.fandom.com'

if __name__=="__main__": 
    try: 
        gds = GraphDataScience(os.environ['NEO4J_URI'], auth=(os.environ['NEO4J_USER'], os.environ['NEO4J_PASSWORD']))
        
        # function 1 used
        result = get_two_random_pages(gds=gds, domain=DOMAIN).to_dict()
        p1 = {'name':result['p1'][0].get('name'), 'url':result['p1'][0].get('url'), 'wiki_id':result['p1'][0].get('wiki_id')}
        p2 = {'name':result['p2'][0].get('name'), 'url':result['p2'][0].get('url'), 'wiki_id':result['p2'][0].get('wiki_id')}
        
        # function 2 used
        are_pages_valid = does_path_exist(gds=gds, domain=DOMAIN, wiki_id_1=p1['wiki_id'], wiki_id_2=p2['wiki_id'])
        print(are_pages_valid)
        print(type(are_pages_valid))
        
        # function 3 used
        right_answer = get_shortest_path(gds=gds, domain=DOMAIN, wiki_id_1=p1['wiki_id'], wiki_id_2=p2['wiki_id'])
        
    finally:
        gds.close()