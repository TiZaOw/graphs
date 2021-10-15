import json
import pandas as pd

with open('mongo_db/test_db.json') as file:
    json_file = json.load(file)

df_json = pd.DataFrame.from_dict(json_file, orient='columns')