import pandas as pd
import db

df_raw = db.fetch_data()
df_raw = df_raw.dropna(subset=["datum"]) #drops NaN

# TODO: muss aufjedenfall noch getestet werden ;)
# TODO: erkennt die y-achsen solange die scores keine 0 enthalten (und es keine weiteren columns mit werten >0 gibt)
# zur Erklärung: is_x_axis, schaut ob es ein datetime format ist und dann ob es den für uhrzeiten typischen : enthält
# tritt hier der fall auf, dass uhrzeit und datum im selben column sind,
# werden datum=uhrzeit gesetzt und extra ausgewertet


def is_date_format(input):
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


def is_x_axis(df):
    datum, uhrzeit = '', ''
    for column in df:
        stringdata = df[column].astype(str)
        if is_date_format(stringdata):
            if stringdata.str.contains(":").all():
                uhrzeit = column
            else:
                datum = column
    if datum == '':
        datum = uhrzeit
    elif uhrzeit == '':
        uhrzeit = datum

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


# wochentag wird immer neu gesetzt, da annahme, dass sowieso nicht standardmäßig enthalten
def set_right_x(df):
    datum, uhrzeit = is_x_axis(df)
    wochentag = "wochentag"
    if datum == uhrzeit:
        df[datum] = pd.to_datetime(df[datum], dayfirst=True)
        df["uhrzeit"] = df[datum].dt.strftime('%H:%M')
        df[wochentag] = df[datum].dt.strftime('%A')
        df[datum] = df[datum].dt.strftime('%d.%m.%Y')
        return df, datum, "uhrzeit", wochentag
    else:
        df[datum] = pd.to_datetime(df[datum], dayfirst=True)
        # TODO: df[uhrzeit] format?, währe in dem Fall schon richtig (?)
        df[wochentag] = df[datum].dt.strftime('%A')
        df[datum] = df[datum].dt.strftime('%d.%m.%Y')
        return df, datum, uhrzeit, wochentag


df_clean, datum, uhrzeit, wochentag = set_right_x(df_raw)
