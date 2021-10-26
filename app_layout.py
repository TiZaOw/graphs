from datetime import date

import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import graphs


heading = dbc.Row([
    dbc.Col(html.H1("Analyse Kundenbewertungen Demo"), width='auto', align='center'),
    dbc.Col(html.Img(src='assets/logo.jpg', style={'align': 'middle'}), width='auto', align='end')
])

# default_fig = graphs.get_default_fig()


layout = dbc.Container(fluid=True, children= [
    html.Div([
        dbc.Row([dbc.Col(html.Div(heading), width='auto')], justify='end'),
        dbc.Row([dcc.Link('Config Menu', href='/config')]),
        html.Hr(),
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.Div(id='radios'),
                dbc.Col(html.Div(
                    dbc.RadioItems(
                        id="weekly",
                        className="btn-group",
                        labelClassName="btn btn-primary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "weekly-trend", "value": 'weekly'},
                            {"label": "no", "value": 'no'},
                        ],
                        value='no',
                    ), className='radio-group'), align='center', width='auto'),
            ],width='auto', align='center'),
        ], justify='center'),
        dbc.Row([
            dbc.Col(dcc.Graph(id='graph'), width='auto', align='center'), #hatte mal noch figure=defaultfigure nach id
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
                           marks={i: str(i) for i in range(0, 5)}, value=4, ),
            ])),
            id="collapse",
            is_open=False,
        )
    ])
],)

app_layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])