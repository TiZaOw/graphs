import json
import dash
from dash import dcc
from dash import html
from dash import Input,Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash_bootstrap_templates import load_figure_template

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
    ])
],)




def x_filter_for_date(df_json):
    pass
def x_filter_for_weekday(df_json):
    pass
def x_filter_for_time(df_json):
    pass

@app.callback(Output("output", "children"),
              Output('graph', 'figure'),
              [Input("radios", "value")])
def display_value(value):
    fig = px.bar(df_json, x=value, y='score-essen')
    return f"Selected value: {value}", fig



if __name__ == "__main__":
    app.run_server(debug=True)