from datetime import date
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import outsourced_app_layout
import graphs

heading = dbc.Row([
    dbc.Col(html.H1("Analyse Kundenbewertungen Demo"), width='auto', align='center'),
    dbc.Col(html.Img(src='assets/logo.jpg', style={'align': 'middle'}), width='auto', align='end')
])

# default_fig = graphs.get_default_fig()


layout = dbc.Container(fluid=True, children=[
    html.Div([
        dbc.Row([dbc.Col(html.Div(heading), width='auto')], justify='end'),
        dbc.Row([dcc.Link('Config Menu', href='/config')]),
        html.Hr(),
        html.Button("Add graph", id="dynamic-add-graph", n_clicks=0),
        html.Div(id='dynamic-graph', children=[]),
        ]),
    ])


def layout_graph_and_filter(n_clicks):
    layout_graph_and_filter = html.Div([
        dcc.Dropdown(
            id={'type': 'restaurant',
                'index': n_clicks},
            options=[
                # {'label': 'Alle', 'value': 'all'},
                {'label': i.title(), 'value': i} for i in outsourced_app_layout.unique_restaurant
            ],
            value='all'
        ),
        html.Br(),
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.Div(id='radios'),
                ],width='auto', align='center'),
            ], justify='center'),
            dbc.Row([
                dbc.Col(dcc.Graph(id={'type': 'graph', 'index': n_clicks}), width='auto', align='center'), #hatte mal noch figure=defaultfigure nach id
            ], justify='center'),
        ]),
        html.Br(),
        html.Div([
            dbc.Col(html.Div(
                dbc.RadioItems(
                    id={'type': 'weekly',
                        'index': n_clicks},
                    className="btn-group",
                    labelClassName="btn btn-secondary",
                    labelCheckedClassName="active",
                    options=[
                        {"label": "weekly-trend", "value": 'weekly'},
                        {"label": "no", "value": 'no'},
                    ],
                    value='no',
                ), className='radio-group'), align='center', width='auto'),
        ]),
            html.Div([
                html.Label('Datumsbereich'),
                dcc.DatePickerRange(
                    id={'type': 'my-date-picker-range',
                        'index': n_clicks},
                    display_format="DD.MM.YYYY",
                    initial_visible_month=date(2021, 6, 5),
                    # end_date=date(2021, 10, 25)
                ),
            ]),
            html.Div([
                dbc.Checklist(
                    id={'type': 'months',
                        'index': n_clicks},
                    options=[
                        {'label': 'Monate gruppieren?', 'value': 'months'},
                    ],
                    value=['months']
                ),
            ]),
            html.Div([
                html.Label('Wochentag Filter: '),
                dbc.Col(html.Div(dcc.RadioItems(
                    id={'type': 'weekday',
                        'index': n_clicks},
                    # className="btn-group",
                    # labelClassName="btn btn-secondary",
                    # labelCheckedClassName="active",
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
                ),),)
            ]),
            html.Br(),
            html.Div(),
            html.Div([
                html.Label('Uhrzeit Filter: '),
                dcc.Input(id={'type': 'start_time', 'index': n_clicks}, value='00:00', type='text'),
                dcc.Input(id={'type': 'end_time', 'index': n_clicks}, value='24:00', type='text'),
            ]),
            html.Div([
                dbc.Collapse(
                    dbc.Card(dbc.CardBody([
                        html.Label('Stunden grupieren'),
                        dcc.Slider(id={'type': 'hours', 'index': n_clicks}, min=0, max=5,
                                   marks={i: str(i) for i in range(0, 5)}, value=4),
                    ])),
                    id={'type': "collapse", 'index': n_clicks},
                    is_open=False,
                )
            ])
    ])
    return layout_graph_and_filter


app_layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])
