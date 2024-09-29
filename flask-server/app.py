from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

import functions_for_endpoint as ffe
import os
from graphdatascience import GraphDataScience


NEO4J_URI = os.environ['NEO4J_URI']
NEO4J_USER = os.environ['NEO4J_USER']
NEO4J_PASSWORD = os.environ['NEO4J_PASSWORD']

app = Flask(__name__)
CORS(app)  # Enable CORS to allow the frontend to communicate with the backend

@app.route("/start-round", methods=['GET'])
def get_path():
    #print("endpoint triggered")
    wiki_domain = 'mariokart.fandom.com'
    path_res = []
    pages = ffe.get_two_random_pages(gds=gds, domain=wiki_domain)
    p1 = {'name':pages['p1'][0].get('name'), 'url':pages['p1'][0].get('url'), 'wiki_id':pages['p1'][0].get('wiki_id')}
    p2 = {'name':pages['p2'][0].get('name'), 'url':pages['p2'][0].get('url'), 'wiki_id':pages['p2'][0].get('wiki_id')}

    if ffe.does_path_exist(gds=gds, domain=wiki_domain, wiki_id_1=p1['wiki_id'], wiki_id_2=p2['wiki_id'])['pathExists'][0] == True:
        path_res = ffe.get_shortest_path(gds=gds, domain=wiki_domain, wiki_id_1=p1['wiki_id'], wiki_id_2=p2['wiki_id'])
    else:
        exit()
    
    # clean p1
    p1_res = {'name':p1['name'],'url':p1['url']}

    # clean p2
    p2_res = {'name':p2['name'],'url':p2['url']}


    ans = {'start':p1_res,
            'end':p2_res,
           'path':path_res,
           }
    
    return ans
    

if __name__ == '__main__':
    gds = GraphDataScience(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    app.run(port=5051, debug=True)