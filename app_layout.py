from datetime import date
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
import outsourced_app_layout
import graphs

heading = dbc.Row([
    dbc.Col(html.H1("Analyse Kundenbewertungen Demo"), width='auto', align='center'),
    dbc.Col(html.Img(src='assets/logo.jpg', style={'align': 'middle'}), width='auto', align='end')
])

# default_fig = graphs.get_default_fig()

layout = dbc.Container(fluid=True, children=[
    dbc.Row([dbc.Col(html.Div(heading), width='auto')], justify='end'),
    dbc.Row([dcc.Link('Config Menu', href='/config')]),
    html.Hr(),
    html.Button("Add graph", id="dynamic-add-graph", n_clicks=0),
    html.Div(id='graph_and_filter', children=[]),
])


def layout_graph_and_filter(n_clicks):  #TODO: das mal schicker machen
    layout_graph_and_filter = html.Div([
        dcc.Dropdown(
            id={'type': 'restaurant', 'index': n_clicks},
            options=[{'label': i.title(), 'value': i} for i in outsourced_app_layout.unique_restaurant],
            value='all'
        ),
        html.Div(id={'type': 'number_of_values', 'index': n_clicks}),
        html.Br(),
        html.Div(id='radios'),
        dbc.RadioItems(
            id={'type': 'both-y', 'index': n_clicks},
            className="btn-group",
            labelClassName="btn btn-secondary",
            labelCheckedClassName="active",
            options=[
                {"label": "Beide Y-Werte", "value": 'both-y'},
                {"label": "no", "value": 'no'},
            ],
            value='no',
        ),
        dbc.Row([
            dbc.Col(dcc.Graph(id={'type': 'graph', 'index': n_clicks}), width='auto', align='center'), #hatte mal noch figure=defaultfigure nach id
        ], justify='center'),
        dbc.Col(
            dbc.RadioItems(
                id={'type': 'weekly', 'index': n_clicks},
                className="btn-group",
                labelClassName="btn btn-secondary",
                labelCheckedClassName="active",
                options=[
                    {"label": "weekly-trend", "value": 'weekly'},
                    {"label": "no", "value": 'no'},
                ],
                value='no',
            ), className='radio-group'),
        dbc.RadioItems(
            id={'type': 'date-selector', 'index': n_clicks},
            className="btn-group",
            labelClassName="btn btn-secondary",
            labelCheckedClassName="active",
            options=[
                {"label": "Woche", "value": 'w'},
                {"label": "Monat", "value": 'm'},
                {"label": "3Monate", "value": '3m'},
                {"label": "Jahr", "value": 'j'},
                {"label": "Kein Selector", "value": 'no'},
            ],
            value='no',
        ),
        html.Label('Datumsbereich'),
        dcc.DatePickerRange(
            id={'type': 'my-date-picker-range', 'index': n_clicks},
            display_format="DD.MM.YYYY",
            initial_visible_month=date(2021, 6, 5),
        ),
        dbc.Checklist(
            id={'type': 'months', 'index': n_clicks},
            options=[
                {'label': 'Monate gruppieren?', 'value': 'months'},
            ],
            value=['months']
        ),
        html.Label('Wochentag Filter: '),
        dcc.RadioItems(
            id={'type': 'weekday', 'index': n_clicks},
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
        html.Br(),
        html.Label('Uhrzeit Filter: '),
        dcc.Input(id={'type': 'start_time', 'index': n_clicks}, value='00:00', type='text'),
        dcc.Input(id={'type': 'end_time', 'index': n_clicks}, value='24:00', type='text'),
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
    return layout_graph_and_filter


app_layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])
