import json
import dash
from dash import dcc
import dash_html_components as html
from dash import Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash_bootstrap_templates import load_figure_template
from datetime import date
import datetime
from statistics import mean
from plotly.subplots import make_subplots
import locale
import db
import graphs
import app_layout
import os

locale.setlocale(locale.LC_TIME, 'de_DE')
load_figure_template("litera")


app = dash.Dash(
    external_stylesheets=[__name__, dbc.themes.LITERA]
)

server = app.server
app.layout = app_layout.app_layout


@app.callback(
    Output('graph', 'figure'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('radios', 'value'),
    Input('y-value', 'value'),
    Input('weekday', 'value'),
    Input('start_time', 'value'),
    Input('end_time', 'value'),
    Input('hours', 'value'),
    Input('months', 'value'))
def visualize_func(min_date, max_date, x_value, y_value, weekday, start_time, end_time, hours, months):

    try:
        fig = graphs.generate_figure(min_date, max_date, x_value, y_value, weekday,
                                     start_time, end_time, hours, months, graphs.get_cleaning_df(graphs.df))
    except Exception as e:
        print('error generating figure')
        print(str(e))
        return graphs.get_empty_figure()
    # fig = graphs.generate_figure(min_date, max_date, x_value, y_value, weekday,
    #                              start_time, end_time, hours, months, graphs.get_cleaning_df(graphs.df))

    return fig


@app.callback(
    Output("collapse", "is_open"),
    [Input("radios", "value")],
)
def toggle_collapse(radios):
    if radios == "uhrzeit":
        return True
    return False


if __name__ == "__main__":
    app.run_server(debug=True)
