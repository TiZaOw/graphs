import json
import pandas as pd
import pymongo
import certifi

# with open('mongo_db/test_db.json') as file:
#     json_file = json.load(file)
#
#
# df_json = pd.DataFrame.from_dict(json_file, orient='columns')
#
# datum, uhrzeit = find_right_columns.configdata(df_json)

ca = certifi.where()
database_url = "mongodb+srv://admin:admin@review-cluster.y16gr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(database_url, tlsCAFile=ca)
db = client.db_reviews
reviews = db.general

#print(db.getCollection('db_reviews'))
#df = pd.DataFrame.from_records(reviews.find())
#df = pd.DataFrame(iter(db.find()))
def fetch_data():
    df = pd.DataFrame(iter(reviews.find()))
    return df