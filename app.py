# coding=utf-8
from flask import Flask
from flask.ext.jsonpify import jsonify
import csv

app = Flask(__name__)

def getGraphData():
    elements = {"nodes": [], "edges": []}

    with open('inventory.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')

        eNBs = []
        teams = []
        for row in spamreader:
            team,type,rrh_name,rrh_id,rrh_sn,rrh_model,enb_name,enb_id = row

            elements["nodes"].append({"data": {"id": rrh_id, "name": type + rrh_name, "faveColor":"#EDA1ED"}})
            elements["edges"].append({"data": {"source": enb_id, "target": rrh_id}}) 

            if team not in teams:
                elements["nodes"].append({"data": {"id": team, "name": team, "faveColor":"black"}})
                teams.append(team)

            if enb_id not in eNBs:
                elements["nodes"].append({"data": {"id": enb_id, "name": enb_name, "faveColor":"#6FB1FC"}})
                elements["edges"].append({"data": {"source": team, "target": enb_id}})
                eNBs.append(enb_id)

    return elements

@app.route('/')
def index():
    return 'Hello, world!'

@app.route('/haha', methods=['GET', 'POST'])
def haha():
    elements = getGraphData()

    style = [
        {
          "selector": 'node',
          "css": {
            'content': 'data(name)',
            'text-valign': 'center',
            'color': 'white',
            'background-color': 'data(faveColor)',
            "min-zoomed-font-size": 10,
            'text-outline-width': 1,
            'text-outline-color': '#888'
          }
        },
        {
          "selector": 'edge',
          "css": {
              'curve-style': 'haystack',
              # 'target-arrow-shape': 'triangle',
              'width': 2    
          }      
        },
        {
          "selector": ':selected',
          "css": {
              'background-color': 'black',
              'line-color': 'black',
              'target-arrow-color': 'black',
              'source-arrow-color': 'black'
          }      
        },    
        {
          "selector": '.faded',
          "css": {
              'opacity': 0.25,
              'text-opacity': 0
          }      
        },    
      ]

    return jsonify(elements = elements, style = style)    

if __name__ == '__main__':
    app.debug = True
    app.run(port=8899)