import dash
from dash import dcc
import dash_html_components as html
from dash import Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash_bootstrap_templates import load_figure_template
import graphs
from datetime import date


heading = dbc.Row([
    dbc.Col(html.H1("Analyse Kundenbewertungen Demo"), width='auto', align='center'),
    dbc.Col(html.Img(src='assets/logo.jpg', style={'align': 'middle'}), width='auto', align='end')
])

default_fig = graphs.get_default_fig()

app_layout = dbc.Container(fluid=True, children= [
    html.Div([
        dbc.Row([dbc.Col(html.Div(heading), width='auto')], justify='end'),
        html.Hr(),
        html.Br(),
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col(html.Div(
                        dbc.RadioItems(
                            id="radios",
                            className="btn-group",
                            labelClassName="btn btn-primary",
                            labelCheckedClassName="active",
                            options=[
                                {"label": "Datum", "value": 'datum'},
                                {"label": "Wochentag", "value": 'wochentag'},
                                {"label": "Uhrzeit", "value": 'uhrzeit'},
                            ],
                            value='datum',
                        ),className='radio-group'),align='center', width='auto'),
                ],justify='center'),
                dbc.Col(html.Div(
                    dbc.RadioItems(
                        id="y-value",
                        className="btn-group",
                        labelClassName="btn btn-secondary",
                        labelCheckedClassName="active",
                        options=[
                            {'label': 'Score-Essen', 'value': 'score_essen'},
                            {'label': 'Score-Lieferung', 'value': 'score_lieferung'}
                        ],
                        value='score_essen'
                    ),className='radio-group'),align='center', width='auto')
            ],width='auto', align='center'),
        ], justify='center'),
        dbc.Row([

         dbc.Col(dcc.Graph(id='graph', figure=default_fig), width='auto', align='center'),

        ], justify='center'),
    ]),
    html.Br(),
    html.Div([
        html.Label('Datumsbereich'),
        dcc.DatePickerRange(
            id='my-date-picker-range',
            display_format="DD.MM.YYYY",
            initial_visible_month=date(2021, 6, 5),
            # end_date=date(2021, 10, 25)
        ),
    ]),
    html.Div([
        dcc.Checklist(
            id="months",
            options=[
                {'label': 'Monate gruppieren?', 'value': 'months'},
            ],
            value=['months']
        ),
    ]),
    html.Br(),
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
        ]),
    html.Div([
        html.Label('Uhrzeit Filter'),
        dcc.Input(id='start_time', value='00:00', type='text'),
        dcc.Input(id='end_time', value='24:00', type='text'),
    ]),
    html.Div([
        dbc.Collapse(
            dbc.Card(dbc.CardBody([
                html.Label('Stunden grupieren'),
                dcc.Slider(id='hours', min=0, max=5,
                           marks={i: str(i) for i in range(1, 6)}, value=4, ),
            ])),
            id="collapse",
            is_open=False,
        )
    ])
],)