import json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
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
import config_menu
import outsourced_app_layout

locale.setlocale(locale.LC_TIME, 'de_DE')
load_figure_template("litera")


app = dash.Dash(
    external_stylesheets=[__name__, dbc.themes.LITERA],
    suppress_callback_exceptions=True
)

server = app.server
app.layout = app_layout.app_layout


@app.callback(
    Output('radios', 'children'),
    Input('url', 'pathname'))
def variable_layout(pathname):
    if pathname == "/":
        x_col_list, y_col_list = outsourced_app_layout.change_col_list()
        return outsourced_app_layout.changing_layout(x_col_list, y_col_list)
    else:
        pass


@app.callback(
    Output("page-content", "children"),
    Input('url', 'pathname'))
def change_layout(pathname):
    if pathname == "/":
        return app_layout.layout
    elif pathname == "/config":
        return config_menu.layout
    else:
        pass


@app.callback(
    Output('button-output', 'children'),
    Input('submit-config', 'n_clicks'),
    State('x-values', 'value'),
    State('y-values', 'value'))
def change_config(n_clicks, x_values, y_values):
    if n_clicks > 0:
        config_menu.write_config(x_values, y_values)
        return 'Config file has been changed'
    else:
        return 'Click to change config'


@app.callback(
    Output('graph', 'figure'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('x-values', 'value'),
    Input('y-values', 'value'),
    Input('weekday', 'value'),
    Input('start_time', 'value'),
    Input('end_time', 'value'),
    Input('hours', 'value'),
    Input('months', 'value'),
    Input('weekly', 'value'), prevent_initial_call=True)
def visualize_func(min_date, max_date, x_value, y_value, weekday, start_time, end_time, hours, months, weekly):

    # try:
    #     fig = graphs.generate_figure(min_date, max_date, x_value, y_value, weekday,
    #                                  start_time, end_time, hours, months, graphs.get_cleaning_df(graphs.df))
    # except Exception as e:
    #     print('error generating figure')
    #     print(str(e))
    #     return graphs.get_empty_figure()
    fig = graphs.generate_figure(min_date, max_date, x_value, y_value, weekday,
                                 start_time, end_time, hours, months, weekly, graphs.get_cleaning_df(graphs.df))

    return fig


@app.callback(
    Output("collapse", "is_open"),
    Input("x-values", "value"),
)
def toggle_collapse(radios):
    if radios == "uhrzeit":
        return True
    return False


if __name__ == "__main__":
    app.run_server(debug=True)
