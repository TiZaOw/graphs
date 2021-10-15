import json
import dash
from dash import dcc
import dash_html_components as html
from dash import Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash_bootstrap_templates import load_figure_template
from datetime import date
import datetime
from statistics import mean
from plotly.subplots import make_subplots
import locale
import db

locale.setlocale(locale.LC_TIME, 'de_DE')
load_figure_template("litera")
#TODO date picker no max limit
def extract_weekday(df):

    df['wochentag'] = df["datum"].dt.strftime('%A')
    return df

def extract_hour(df):
    if 'uhrzeit' not in list(df.columns):
        df['uhrzeit'] = df['datum'].dt.strftime('%H-%M-%S')
    else:
        return df
    return df

def only_date(df):
    df['datum'] = df['datum'].dt.strftime('%d-%m-%Y')
    return df



def check_for_time_format(df):
    df['datum'] = pd.to_datetime(df["datum"], dayfirst=True)
    df = extract_weekday(df)
    df = extract_hour(df)
    df = only_date(df)

    return df

df = db.df_json

df = pd.read_excel('mongo_db/new_york_pizza_clean.xlsx')

df = check_for_time_format(df)



def get_default_fig():
    fig = px.bar(df, x='datum', y='score_essen')
    return fig

def get_empty_figure():
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    return fig

def get_cleaning_df(df):
    df = sort_by_dates(df)  # kicks NaN from Dataset, potentially removable
    df = df.dropna(subset=["uhrzeit"])
    return df


def get_x_axis(x, y, hours, df):

    if x == "uhrzeit":
        df = group_hours(df, y, hours)
    if x == "wochentag":
        df = sort_weekdays(df)
    return df


def generate_figure(min_date, max_date, x_value, y_value, weekday, start_time, end_time, hours, df):
    #TODO Nach Monated gruppieren
    #TODO "filter setzten" Funkionalität. Startet mit keinem Filter und kann hinzegfügt werden
    if min_date is not None and max_date is not None:
        df = filter_for_date(min_date, max_date, df)
    if weekday != "all":
        df = filter_for_weekday(weekday, df)
    if start_time is not None and end_time is not None: #TODO funktion anpassen mit Zeiten nach O Uhr
        df = filter_for_time(start_time, end_time, df)

    df = get_x_axis(x_value, y_value, hours, df)

    fig = draw_figure(x_value, y_value, df)

    return fig

def sort_by_dates(df_date):
    df_date["datum"] = pd.to_datetime(df_date["datum"], dayfirst=True) #zu datetime #TODO informieren warm dayfirst nötig ist
    df_date = df_date.sort_values(by="datum")   #sortiert
    df_date["datum"] = df_date["datum"].dt.strftime("%d.%m.%Y") #umwandeln in deutsches format
    return df_date


def filter_for_date(min_date, max_date, df):
    min_in_datetime = datetime.datetime.strptime(min_date, '%Y-%m-%d')
    max_in_datetime = datetime.datetime.strptime(max_date, '%Y-%m-%d')

    df_date = df.loc[min_in_datetime < pd.to_datetime(df["datum"], dayfirst=True)]
    df_date = df_date.loc[max_in_datetime > pd.to_datetime(df["datum"], dayfirst=True)]
    return df_date


def filter_for_weekday(day, df):
    df_wd = df.loc[pd.to_datetime(df["datum"], dayfirst=True).dt.strftime('%A') == day]
    return df_wd


def filter_for_time(start_time, end_time, df):
    df_time = df.loc[start_time < df["uhrzeit"]]
    df_time = df_time.loc[end_time > df_time["uhrzeit"]]
    return df_time


def group_hours(df, y_value, hours):
    if hours == 0:
        return df
    print('before')
    dict_time = {"uhrzeit": df["uhrzeit"], y_value: df[y_value].astype(float)}
    print('after')
    print(dict_time)
    df_time = pd.DataFrame(data=dict_time)
    time_range = str(hours) + "H"
    print('time_range')
    print(time_range)
    df_time['uhrzeit'] = pd.to_datetime(df_time['uhrzeit'], format="%H-%M-%S")
    df_time = df_time.resample(time_range, on='uhrzeit').mean()
    print(df_time)
    df_time = df_time.reset_index()  # notwendig, weil das drüber den index verschiebt
    print(df_time)
    df_time["uhrzeit"] = df_time["uhrzeit"].dt.strftime("%H:%M")
    print(df_time)
    return df_time


def sort_weekdays(df):  #TODO: später auf deutsch (wenn anderes dataset)
    weekdays = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
    from pandas.api.types import CategoricalDtype
    cat_type = CategoricalDtype(categories=weekdays, ordered=True)
    df['wochentag'] = df['wochentag'].astype(cat_type)
    return df


def draw_figure(x, y, data):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    for contestant, group in data.groupby(x, sort=False):
        avg = list(group[y].astype(float))
        if not avg: #falls empty nur notwendig wegen sort_weekdays!?
            break
        avg = mean(avg)
        m = [avg]
        rounded = "%.2f" % avg
        fig = fig.add_trace(go.Bar(x=group[x], y=m,
                                   hovertemplate=f"{x}: {contestant} <br>{y}: {rounded} <extra></extra>",
                                   name=contestant, text=rounded,
                                   showlegend=False))
    return fig
