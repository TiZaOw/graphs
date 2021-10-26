import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import graphs
import configparser
from configparser import ConfigParser

df = graphs.df
col_list = df.columns

layout = dbc.Container(fluid=True, children=[
    html.Div(
        dcc.Link('Back', href='/')
    ),
    dbc.Col(html.H3("Config Menu"), width='auto', align='center'),
    html.Div([
        html.Label("Wähle die x-Werte"),
        dcc.Checklist(
            id="x-values",
            options=[
                {'label': i, 'value': i} for i in col_list
            ],
            value=[],
            labelStyle={'display': 'inline-block'}
        )
    ]),
    html.Div([
        html.Label("Wähle die y-Werte"),
        dcc.Checklist(
            id="y-values",
            options=[
                {'label': i, 'value': i} for i in col_list
            ],
            value=[],
            labelStyle={'display': 'inline-block'}
        )
    ]),
    html.Div([
        html.Button("Submit to config", id="submit-config", n_clicks=0),
        html.Div(id='button-output')
    ]),
    html.Div([
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
        )
    ])
])


def write_config(x_values, y_values):
    # Get the configparser object
    config_object = ConfigParser()

    config_object["values"] = {
        "x-values": x_values,
        "y-values": y_values
    }
    #Write the above sections to config.ini file
    with open('config.ini', 'w') as conf:
        config_object.write(conf)
