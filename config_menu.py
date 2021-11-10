import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash import dash_table
import graphs

df = graphs.df_sorted
col_list = df.columns
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
    dbc.Col(html.H3("Config Menu ᓚᘏᗢ"), width='auto', align='center'),
    html.Div([
        html.Label("Wähle die x-Werte"),
        dcc.Checklist(
            id="x-values-config",
            options=[{'label': i, 'value': i} for i in col_list],
            value=[],
            labelStyle={'display': 'inline-block'}
        )
    ]),
    html.Div([
        html.Label("Wähle die y-Werte"),
        dcc.Checklist(
            id="y-values-config",
            options=[{'label': i, 'value': i} for i in col_list],
            value=[],
            labelStyle={'display': 'inline-block'}
        )
    ]),
    html.Div([
        html.Button("Submit to config", id="submit-config", n_clicks=0),
        html.Div(id='button-output')
    ]),
    html.Label('Uhrzeit Filter: '),
    dcc.Input(id='start_time_config', value='03:00', type='text'),
    dcc.Input(id='end_time_config', value='06:00', type='text'),
    html.Div([
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
        )
    ])
])


def change_table(start_time, end_time):
    df_time_filtered = graphs.filter_for_time(start_time, end_time, graphs.df_sorted)
    return remove_bad_columns(df_time_filtered)
