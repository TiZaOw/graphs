import pandas as pd

import graphs

df = graphs.df
# df = graphs.get_cleaning_df(graphs.df)
import time


def isDateFormat(input):
    try:
        pd.to_datetime(input,)
        return numeric(input)
    except:
        return False

def isHourFormat(input):
    try:
        print(pd.to_datetime(input).dt.strftime('%H:%M'))
        return True
    except ValueError:
        return False


def numeric(data):  #da to_datetime alle zahlen durchlässt
    try:
        stringdata = data.astype(str)
        num = stringdata.str.isnumeric()
        #schaut ob alle werte numerisch sind -> datums haben ./-
        if num.all() == True:
            return False
        else:
            return True
    except:
        return False

# score=df['datum'].astype(str)
# print(score.str.isnumeric())
# print(df['score_essen'].str.isnumeric())
# df['datum'].to_string().isnumeric()

# print(parse(str(df["datum"].head(1))))
# print(pd.to_datetime(df["datum"]))
# print(str(df["datum"].head(1)))
# print(pd.to_datetime(df["datum"]).dt.strftime("%d.%m.%Y"))
# print(pd.to_datetime(df["datum"], format="%d-%m-%Y"))


testdf = pd.DataFrame({'col1': ["12-1-09"], 'col2': ["5/8/2002"], 'col3': ["9.9.99"],
                       'col4': ["12:45:19"], 'col5': ["09:17"]})

df2 = pd.DataFrame({"col1": ["5:26"],"col2":["15.12.2019"], "col3": ["8"], "col4": ["montag"]})


def configdata(df):
    datum = 'datum'
    uhrzeit = 'uhrzeit'
    for column in df:
        if isDateFormat(df[column]):
            if df[column].str.contains(":").all():
                uhrzeit = column
            else:
                datum = column
            # print(pd.to_datetime(df[column]))
            # if pd.to_datetime(df[column]).time():
            #     print(f"%column, is timeformat")
            # print('errorfor sure')
    return datum, uhrzeit



def get_x_dict(datum, uhrzeit):
    x = [{"label": "Datum", "value": datum},
         {"label": "Wochentag", "value": 'wochentag'},
         {"label": "Uhrzeit", "value": uhrzeit}, ]
    #
    return [i for i in x]



configdata(df2)