import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash import dash_table
import graphs
from configparser import ConfigParser

df = graphs.df_clean
col_list = df.columns
# df = pd.read_excel('mongo_db/new_york_pizza_clean.xlsx')
df = df.head()


def remove_bad_columns(df): #which dont want to be in a dash_table
    for column in df:
        try:
            df[column].to_json()
        except:
            df = df.drop(columns=[column])
    return df

df = remove_bad_columns(df)

layout = dbc.Container(fluid=True, children=[
    html.Div(
        dcc.Link('Back', href='/')
    ),
    dbc.Col(html.H3("Config Menu"), width='auto', align='center'),
    html.Div([
        html.Label("Wähle die x-Werte"),
        dcc.Checklist(
            id="x-values-config",
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
            id="y-values-config",
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
