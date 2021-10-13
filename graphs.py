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
locale.setlocale(locale.LC_TIME, 'de_DE')

load_figure_template("litera")


app = dash.Dash(
    external_stylesheets=[dbc.themes.LITERA]
)

with open('mongo_db/test_db.json') as file:
    json_file = json.load(file)

df_json = pd.DataFrame.from_dict(json_file, orient='columns')


bar_fig = px.bar(df_json, x='datum', y='score_essen')


heading = dbc.Row([
    dbc.Col(html.H1("Analyse Kundenbewertungen Demo"), width='auto', align='center'),
    dbc.Col(html.Img(src='assets/logo.jpg', style={'align': 'middle'}), width='auto', align='end')
])


app.layout = dbc.Container(fluid=True, children= [
    html.Div([
        dbc.Row([dbc.Col(html.Div(heading), width='auto')], justify='end'),
        html.Hr(),
        html.Br(),
        dbc.Row( #Selector
        [
            dbc.Col(
                [
                    dbc.Row(
                        [
                            dbc.Col(html.Div(
                                dbc.RadioItems(
                                    id="radios",
                                    className="btn-group",
                                    labelClassName="btn btn-secondary",
                                    labelCheckedClassName="active",
                                    options=
                                        [
                                        {"label": "Datum", "value": 'datum'},
                                        {"label": "Wochentag", "value": 'wochentag'},
                                        {"label": "Uhrzeit", "value": 'Uhrzeit'},
                                        ],
                                    value='datum',
                                ),className='radio-group'),align='center', width='auto'),

                                dbc.Row([dbc.Col(html.Div(id='output'), width='auto', align='center')], justify='center')

                        ],justify='center'),


                ],width='auto', align='end'),


        ], justify='center'),
        dbc.Row(
        [

         dbc.Col(dcc.Graph(id='graph', figure=bar_fig), width='auto', align='center'),

        ], justify='center'),
    ]),
    html.Br(),
    html.Div([
        dcc.DatePickerRange(
            id='my-date-picker-range',
            min_date_allowed=date(2021, 4, 5),
            max_date_allowed=date(2021, 9, 19),
            initial_visible_month=date(2021, 6, 5),
            end_date=date(2021, 10, 25)
        ),
        html.Div(id='output-container-date-picker-range')
    ]),
    html.Br(),
    html.Div([
        html.Label('y-Achsen Auswahl'),
        dcc.Dropdown(
            id="y-value",
            options=[
                {'label': 'Score-Essen', 'value': 'score-essen'},
                {'label': 'Score-Lieferung', 'value': 'score-lieferung'}
            ],
            value='score-essen'
        ),
        html.Div(id='output-score-dropdown')
    ]),
    html.Div([
        html.Label('Wochentag Filter'),
            dcc.RadioItems(
                id="weekday",
                options=[
                    {'label': 'Alle Wochentage', 'value': 'all'},
                    {'label': 'Montag', 'value': 'Montag'},
                    {'label': 'Dienstag', 'value': 'Dienstag'},
                    {'label': 'Mittwoch', 'value': 'Mittwoch'},
                    {'label': 'Donnerstag', 'value': 'Donnerstag'},
                    {'label': 'Freitag', 'value': 'Freitag'},
                    {'label': 'Samstag', 'value': 'Samstag'},
                    {'label': 'Sonntag', 'value': 'Sonntag'}
                ],
                value='all'
            ),
        html.Div(id='output-weekday-filter')
        ]),
    html.Div([
        html.Label('Uhrzeit Filter'),
            dcc.Input(id=('start_time'), value='11:00', type='text'),
            dcc.Input(id=('end_time'), value='23:00', type='text'),
    ]),
    html.Div([
        html.Label('Stunden grupieren'),
        dcc.Slider(id=('hours'), min=0, max=5,
                    marks={i: str(i) for i in range(1, 6)}, value=4, ),
    ])
],)


@app.callback(
    Output('output-container-date-picker-range', 'children'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))
def date_range(start_date, end_date):   #displays selected dates -> removeable
    string_prefix = 'You have selected: '
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%d.%m.%Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%d.%m.%Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string

    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix

@app.callback(
    Output('graph', 'figure'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('radios', 'value'),
    Input('y-value', 'value'),
    Input('weekday', 'value'),
    Input('start_time', 'value'),
    Input('end_time', 'value'),
    Input('hours', 'value'))
def visualize_func(min_date, max_date, x_value, y_value, weekday, start_time, end_time, hours):
    df = df_json
    df = sort_by_dates(df)
    if(min_date is not None and max_date is not None):
        df = filter_for_date(min_date, max_date, df)
    if(weekday != "all"):
        df = filter_for_weekday(weekday, df)
    if(start_time != "11:00" or end_time != "23:00"):
        df = filter_for_time(start_time, end_time, df)

    if(x_value == "Uhrzeit"):
        df = group_hours(df, x_value, y_value, hours)

    fig = average(x_value, y_value, df)

    return fig


def filter_for_date(min_date, max_date, df):
    min_in_datetime = datetime.datetime.strptime(min_date, '%Y-%m-%d')
    max_in_datetime = datetime.datetime.strptime(max_date, '%Y-%m-%d')

    df_date = df.loc[min_in_datetime < pd.to_datetime(df["datum"], dayfirst=True)]
    df_date = df_date.loc[max_in_datetime > pd.to_datetime(df["datum"], dayfirst=True)]
    return df_date


def sort_by_dates(df_date):
    df_date["datum"] = pd.to_datetime(df_date["datum"], dayfirst=True) #zu datetime
    df_date = df_date.sort_values(by="datum")   #sortiert
    df_date["datum"] = df_date["datum"].dt.strftime("%d.%m.%Y") #umwandeln in deutsches format
    return df_date

def filter_for_weekday(day, df):
    german = {
        "Monday": "Montag",
        "Tuesday": "Dienstag",
        "Wednesday": "Mittwoch",
        "Thursday": "Donnerstag",
        "Friday": "Freitag",
        "Saturday": "Samstag",
        "Sunday": "Sonntag"
    }
    df_wd = df.loc[pd.to_datetime(df["datum"], dayfirst=True).dt.strftime('%A') == day]
    # print(pd.to_datetime(df_wd["datum"]).dt.strftime('%A'), pd.to_datetime(df_wd["datum"]))
    return df_wd


def filter_for_time(start_time, end_time, df):
    df_time = df.loc[start_time < df["Uhrzeit"]]
    df_time = df_time.loc[end_time > df_time["Uhrzeit"]]
    # df_time['Uhrzeit'] = pd.to_datetime(df_time["Uhrzeit"]).dt.hour #unnötig jetzt
    return df_time


def group_hours(df, x_value, y_value, hours):
    d_time = {"Uhrzeit": pd.to_datetime(df["Uhrzeit"]), y_value: df[y_value].astype(float)}
    df_time = pd.DataFrame(data=d_time)
    time_range = str(hours) + "H"
    df_time = df_time.resample(time_range, on='Uhrzeit').mean()
    df_time = df_time.reset_index()  # notwendig, weil das drüber den index verschiebt
    df_time["Uhrzeit"] = df_time["Uhrzeit"].dt.strftime("%H:%M:%S")
    return df_time


def average(x,y,data):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    for contestant, group in data.groupby(x, sort=False):
        avg = list(group[y].astype(float))
        avg = mean(avg)  # mittelwert der gegroupten y-werte
        # m = []
        # m.append(avg)
        m = [avg]
        fig = fig.add_trace(go.Bar(x=group[x], y=m,
                             name=contestant, #text=group[y],
                             textposition='auto',
                             ))
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
