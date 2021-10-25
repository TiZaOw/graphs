import json
import pandas as pd
import find_right_columns

with open('mongo_db/test_db.json') as file:
    json_file = json.load(file)

#TODO value 0 = 1 Stern Bewertung
df_json = pd.DataFrame.from_dict(json_file, orient='columns')

datum, uhrzeit = find_right_columns.configdata(df_json)
