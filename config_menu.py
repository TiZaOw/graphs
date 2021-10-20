import dash_bootstrap_components as dbc
import dash_html_components as html
from dash import dcc
import dash_table
import graphs

df = graphs.df

layout = dbc.Container(fluid=True, children=[
    html.Div([
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
        )
    ])
])
