import csv

def getGraphData():
    elements = []

    with open('inventory.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')

        eNBs = ()
        for row in spamreader:
            team,type,rrh_name,rrh_id,rrh_sn,rrh_model,enb_name,enb_id = row

            elements.append({"group":"nodes", "data": {"id": rrh_id, "name": type + rrh_name}})
            elements.append({"group":"edges", "data": {"id": enb_id + rrh_id, "source": enb_id, "target": rrh_id}}) 

            if enb_id not in eNBs:
                elements.append({"group":"nodes", "data": {"id": rrh_id, "name": row[1] + row[2]}})


    return elements