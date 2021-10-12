import json
import dash
import dash_core_components as dcc  #TODO: wieso geht bei mir zuhause nicht: from dash import dcc? ff für die nächsten 2
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash_bootstrap_templates import load_figure_template
from datetime import date
import datetime
from statistics import mean
from plotly.subplots import make_subplots

load_figure_template("litera")


app = dash.Dash(
    external_stylesheets=[dbc.themes.LITERA]
)

with open('mongo_db/test_db.json') as file:
    json_file = json.load(file)

df_json = pd.DataFrame.from_dict(json_file, orient='columns')
#print(df_json)


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
    ])
],)



def x_filter_for_date(df_json):
    pass
def x_filter_for_weekday(df_json):
    pass
def x_filter_for_time(df_json):
    pass

# @app.callback(Output("output", "children"),
#               Output('graph', 'figure'),
#               [Input("radios", "value")])
# def display_value(value):
#
#     fig = px.bar(df_json, x=value, y='score-essen')
#     return f"Selected value: {value}", fig



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

@app.callback(#Output("output", "children"),
    Output('graph', 'figure'),
    #Output('output-score-dropdown', 'children'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('radios', 'value'),
    Input('y-value', 'value'),
    Input('weekday', 'value'),
    Input('start_time', 'value'),
    Input('end_time', 'value'))
def visualize_func(min_date, max_date, x_value, y_value, day, start_time, end_time):
    df = df_json
    if(min_date is not None and max_date is not None):
        min = datetime.datetime.strptime(min_date, '%Y-%m-%d')
        max = datetime.datetime.strptime(max_date, '%Y-%m-%d')

        # print(min< pd.to_datetime(df['datum']) and pd.to_datetime(df['datum']) < max)
        df_new = df.loc[min < pd.to_datetime(df['datum'])]
        df_new2 = df_new.loc[max > pd.to_datetime(df_new['datum'])]
#TODO: es wird erst sortiert wenn dates gewählt wurden (da deutsches format)
        df_new2["datum"] = pd.to_datetime(df_new2["datum"]) #zu datetime
        df_new2 = df_new2.sort_values(by="datum")   #sortiert
        df_new2["datum"] = df_new2["datum"].dt.strftime("%d.%m.%Y") #umwandeln in deutsches format
        # fig = px.bar(df_new2, x=x_value, y=y_value)
        # fig = average(x_value, y_value, df_new2)
        df = df_new2
    if(day != "all"):   #TODO: wochentage noch auf englisch!? -> mittwoch klären
        df_wd = df.loc[df["wochentag"] == day]
        print(df["wochentag"])
        # fig = px.bar(df_wd, x=x_value, y=y_value)
        # fig = average(x_value, y_value, df_wd)
        df = df_wd
    if(start_time != "11:00" or end_time != "23:00"):
        df_time = df.loc[start_time < df["Uhrzeit"]]
        df_time = df_time.loc[end_time > df_time["Uhrzeit"]]
        # df_time = df_time.sort_values(by="Uhrzeit") #not even necesaary i think
        df_time['Uhrzeit'] = pd.to_datetime(df_time["Uhrzeit"]).dt.hour
        # fig = px.bar(df_time, x=x_value, y=y_value)
        # fig = average(x_value, y_value, df_time)
        df = df_time

    # fig = px.bar(df_json, x=x_value, y=y_value)
    fig = average(x_value, y_value, df)

    return fig

def average(x,y,data):
    fig = make_subplots(specs=[[{"secondary_y": True}]])  # added for average
    for contestant, group in data.groupby(x):
        avg = list(group[y].astype(float))    #TODO: "Cannot convert float NaN to int" -> war astype(int)
        avg = mean(avg)  # mittelwert der gegroupten y-werte
        # m = []
        # m.append(avg)
        m = [avg]   # zeichnet nur mit listen elementen
        fig = fig.add_trace(go.Bar(x=group[x], y=m,
                             name=contestant, text=group[y],
                             textposition='auto',
                             ))
    # fig.update_layout()
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)