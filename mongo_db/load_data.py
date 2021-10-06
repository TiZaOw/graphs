import pymongo
import certifi
import json


ca = certifi.where()
database_url = "mongodb+srv://admin:admin@review-cluster.y16gr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(database_url, tlsCAFile=ca)
db = client['db']
col = db['lauches']

with open('test_db.json', 'w') as file:
    json_list =[]
    for doc in col.find():
        del doc['_id']
        print(type(doc))
        print(doc)
        json_list.append(doc)
    json.dump(json_list, file)
