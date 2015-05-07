# coding=utf-8
from flask import Flask
from flask.ext.jsonpify import jsonify
import csv

app = Flask(__name__)

def getGraphData():
    elements = {"nodes": [], "edges": []}

    with open('inventory2.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')

        eNBs = []
        teams = []
        locIDs = []
        locEdges = []
        loc2inventory = [] 
        
        # special node: No Location Specified
        elements["nodes"].append({"data": {"id": 'NoLocation', "name": "NoLocation", "faveColor":"red", "weight":80}})

        for row in spamreader:
            team,type,rrh_name,rrh_id,rrh_location,rrh_location_name,rrh_sn,rrh_model,enb_name,enb_id,enb_location,enb_location_name = row

            # enb rrh nodes
            elements["nodes"].append({"data": {"id": rrh_id, "name": type + rrh_name, "faveColor":"#EDA1ED", "weight":30}})
            elements["edges"].append({"data": {"source": enb_id, "target": rrh_id, "weight":5}}) 

            # team
            if team not in teams:
                elements["nodes"].append({"data": {"id": team, "name": team, "faveColor":"black", "weight":60}})
                teams.append(team)

            if enb_id not in eNBs:
                elements["nodes"].append({"data": {"id": enb_id, "name": enb_name, "faveColor":"#6FB1FC", "weight":50}})
                elements["edges"].append({"data": {"source": team, "target": enb_id, "weight":10}})
                eNBs.append(enb_id)

            # enb Locations
            if enb_location_name:
                locationNames = enb_location_name.split('>')
                locationIDs = enb_location.split('_')
                # print('size: {}'.format(len(locationNames)))

                for id, name in zip(locationIDs, locationNames):
                    if id not in locIDs:                        
                        locIDs.append(id)
                        elements["nodes"].append({"data": {"id": id, "name": name, "faveColor":"yellow", "weight":85}})

                for i in xrange(len(locationNames) - 1):
                    if (locationIDs[i] + locationIDs[i + 1]) not in locEdges:
                        locEdges.append(locationIDs[i] + locationIDs[i + 1])
                        elements["edges"].append({"data": {"source": locationIDs[i], "target": locationIDs[i + 1], "weight":10}})

                # last location node should point to eNB
                if (locationIDs[-1] + enb_id) not in loc2inventory:
                  elements["edges"].append({"data": {"source": locationIDs[-1], "target": enb_id, "weight":10}})
                  loc2inventory.append(locationIDs[-1] + enb_id)
            else:
                if ("NoLocation" + enb_id) not in loc2inventory:
                  elements["edges"].append({"data": {"source": "NoLocation", "target": enb_id, "weight":10}})      
                  loc2inventory.append("NoLocation" + enb_id)

            # rrh Locations
            if rrh_location_name:                
                locationNames = rrh_location_name.split('>')
                locationIDs = rrh_location.split('_')
                # print('size: {}'.format(len(locationNames)))
                # print(locationNames)
                # print(locationIDs)

                for id, name in zip(locationIDs, locationNames):
                    if id not in locIDs:                        
                        locIDs.append(id)
                        elements["nodes"].append({"data": {"id": id, "name": name, "faveColor":"yellow", "weight":85}})

                for i in xrange(len(locationNames) - 1):
                    if (locationIDs[i] + locationIDs[i + 1]) not in locEdges:
                        locEdges.append(locationIDs[i] + locationIDs[i + 1])
                        elements["edges"].append({"data": {"source": locationIDs[i], "target": locationIDs[i + 1], "weight":10}})

                # last location node should point to rrh
                if ("NoLocation" + rrh_id) not in loc2inventory:
                    elements["edges"].append({"data": {"source": locationIDs[-1], "target": rrh_id, "weight":10}})
                    loc2inventory.append("NoLocation" + rrh_id)
            else:
                if ("NoLocation" + rrh_id) not in loc2inventory:
                    elements["edges"].append({"data": {"source": "NoLocation", "target": rrh_id, "weight":10}})            
                    loc2inventory.append("NoLocation" + rrh_id)

    # print(elements)

    return elements

# def getGraphData():
#     elements = {"nodes": [], "edges": []}

#     with open('inventory.csv', 'rb') as csvfile:
#         spamreader = csv.reader(csvfile, delimiter=',')

#         eNBs = []
#         teams = []
#         for row in spamreader:
#             team,type,rrh_name,rrh_id,rrh_sn,rrh_model,enb_name,enb_id = row

#             elements["nodes"].append({"data": {"id": rrh_id, "name": type + rrh_name, "faveColor":"#EDA1ED"}})
#             elements["edges"].append({"data": {"source": enb_id, "target": rrh_id}}) 

#             if team not in teams:
#                 elements["nodes"].append({"data": {"id": team, "name": team, "faveColor":"black"}})
#                 teams.append(team)

#             if enb_id not in eNBs:
#                 elements["nodes"].append({"data": {"id": enb_id, "name": enb_name, "faveColor":"#6FB1FC"}})
#                 elements["edges"].append({"data": {"source": team, "target": enb_id}})
#                 eNBs.append(enb_id)

#     return elements

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
            'width': 'mapData(weight, 0, 100, 10, 60)',
            'height': 'mapData(weight, 0, 100, 10, 60)',            
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