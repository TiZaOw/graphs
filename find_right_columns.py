# from configparser import ConfigParser
#
# #Get the configparser object
# config_object = ConfigParser()
#
# #Assume we need 2 sections in the config file, let's call them USERINFO and SERVERCONFIG
# config_object["USERINFO"] = {
#     "admin": "Chankey Pathak",
#     "loginid": "chankeypathak",
#     "password": "tutswiki"
# }
#
# config_object["SERVERCONFIG"] = {
#     "host": "tutswiki.com",
#     "port": "8080",
#     "ipaddr": "8.8.8.8"
# }
#
# #Write the above sections to config.ini file
# with open('config.ini', 'w') as conf:
#     config_object.write(conf)
import pandas as pd

import graphs

df = graphs.df
# df = graphs.get_cleaning_df(graphs.df)
import time


def isDateFormat(input):
    try:
        pd.to_datetime(input,)
        # print('ok')
        # if input.isnumeric():
        #     return False
        return numeric(input)
    except:
        # try:
        #     pd.to_datetime(input, format="%d.%m.%Y")
        #     return True
        # except:
        #     try:
        #         pd.to_datetime(input, format="%d/%m/%Y")
        #         return True
        #     except:
        #         try:
        #             pd.to_datetime(input, format="%d-%m-%Y")
        #             return True
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
    if 'datum' not in df.columns:
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
            else:
                print(column)
        #options = get_x_dict(datum, uhrzeit)
        #print(options)


# df2["col1"].str.contains(":")

def get_x_dict(datum, uhrzeit):

    x = [{"label": "Datum", "value": datum},
         {"label": "Wochentag", "value": 'wochentag'},
         {"label": "Uhrzeit", "value": uhrzeit}, ]
    #
    return [i for i in x]

# options=get_x_dict()
# print(options)

configdata(df2)