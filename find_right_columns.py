import pandas as pd
import graphs
import db

# df = graphs.df_clean
df = db.fetch_data()
df = df.dropna(subset=["datum"])
import time
# TODO: erkennt die y-achsen solange die scores keine 0 enthalten (und es keine weiteren columns mit werten >0 gibt)

def isDateFormat(input):
    try:
        pd.to_datetime(input,)
        return numeric(input)
    except:
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


testdf = pd.DataFrame({'col1': ["12-1-09"], 'col2': ["5/8/2002"], 'col3': ["9.9.99"],
                       'col4': ["12:45:19"], 'col5': ["09:17"]})

df2 = pd.DataFrame({"col1": ["5:26"],"col2":["15.12.2019"], "col3": ["8"], "col4": ["montag"],
                    "col5":[19],"c6":[float("NaN")]})


def configdata(df):
    datum = 'datum'
    uhrzeit = 'uhrzeit'
    for column in df:
        stringdata = df[column].astype(str)
        if isDateFormat(stringdata):
            if stringdata.str.contains(":").all():
                uhrzeit = column
            else:
                datum = column
                print('hey')

    return datum, uhrzeit


def is_y_axis(df):
    y_axis = []
    for column in df:
        if pd.to_numeric(df[column], errors='coerce').notnull().all():
            stringdata = df[column].astype(str)
            if stringdata.str.contains("0").any():
                pass
            else:
                y_axis.append(column)
    return y_axis

print(is_y_axis(df))
print(configdata(df))
wochentag="wochentag"


#wochentag wird immer überschrieben
def extract(df):
    datum, uhrzeit = configdata(df)
    if datum == uhrzeit:
        df[datum] = pd.to_datetime(df[datum], dayfirst=True)
        df["uhrzeit"] = df[datum].dt.strftime('%H:%M')
        df[wochentag] = df[datum].dt.strftime('%A')
        df[datum] = df[datum].dt.strftime('%d.%m.%Y')
        return df, datum, "uhrzeit"
    else:
        df[datum] = pd.to_datetime(df[datum], dayfirst=True)
        # TODO: df[uhrzeit] format?
        df[wochentag] = df[datum].dt.strftime('%A')
        df[datum] = df[datum].dt.strftime('%d.%m.%Y')
        return df, datum, uhrzeit


df_clean, datum, uhrzeit = extract(df)
