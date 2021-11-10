import pandas as pd
import db
import configparser

df_raw = db.fetch_data()

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


def numeric(data):  # da to_datetime alle zahlen durchlässt
    try:
        stringdata = data.astype(str)
        num = stringdata.str.isnumeric()
        # schaut ob alle werte numerisch sind -> datums haben ./-
        if num.all():
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


# TODO: wochentag wird in graphs.py nie verwendet, könnte weggelassen werden? (hier wird eng-version erstellt)
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
y_axis = is_y_axis(df_clean)
df_clean = df_clean.dropna(subset=[datum])  # drops NaN


def write_config(x_values, y_values):
    # Get the configparser object
    config_object = configparser.ConfigParser()

    config_object["values"] = {
        "x-values": x_values,
        "y-values": y_values
    }
    #Write the above sections to config.ini file
    with open('config.ini', 'w') as conf:
        config_object.write(conf)


def get_config():
    config = configparser.ConfigParser()
    config.read('config.ini')

    x_values = config['values']['x-values']
    y_values = config['values']['y-values']
    col_list = df_clean.columns

    x_col_list = [e for e in col_list if e in x_values]
    y_col_list = [e for e in col_list if e in y_values]
    return x_col_list, y_col_list


write_config([datum, wochentag, uhrzeit], y_axis)
