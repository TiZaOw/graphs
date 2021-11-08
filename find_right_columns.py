import pandas as pd
import db

df = db.fetch_data()
df = df.dropna(subset=["datum"]) #drops NaN
import time
# TODO: erkennt die y-achsen solange die scores keine 0 enthalten (und es keine weiteren columns mit werten >0 gibt)

def isDateFormat(input):
    try:
        pd.to_datetime(input)
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


#wochentag wird immer überschrieben
def extract(df):
    datum, uhrzeit = configdata(df)
    wochentag = "wochentag"
    if datum == uhrzeit:
        df[datum] = pd.to_datetime(df[datum], dayfirst=True)
        df["uhrzeit"] = df[datum].dt.strftime('%H:%M')
        df[wochentag] = df[datum].dt.strftime('%A')
        df[datum] = df[datum].dt.strftime('%d.%m.%Y')
        return df, datum, "uhrzeit", wochentag
    else:
        df[datum] = pd.to_datetime(df[datum], dayfirst=True)
        # TODO: df[uhrzeit] format?
        df[wochentag] = df[datum].dt.strftime('%A')
        df[datum] = df[datum].dt.strftime('%d.%m.%Y')
        return df, datum, uhrzeit, wochentag


df_clean, datum, uhrzeit, wochentag = extract(df)
