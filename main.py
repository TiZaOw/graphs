import traceback
import dash
import sys
from dash.dependencies import Output, Input, State, MATCH
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import locale
import graphs
import app_layout
import os
import config_menu
import outsourced_app_layout

locale.setlocale(locale.LC_TIME, 'de_DE')
load_figure_template("litera")

app = dash.Dash(
    external_stylesheets=[__name__, dbc.themes.LITERA],
    suppress_callback_exceptions=True)

server = app.server
app.layout = app_layout.app_layout


@app.callback(
    Output('graph_and_filter', 'children'),
    Input('dynamic-add-graph', 'n_clicks'),
    State('graph_and_filter', 'children'))
def display_graph_and_filter(n_clicks, children):
    new_element = app_layout.layout_graph_and_filter(n_clicks)
    children.append(new_element)
    return children


@app.callback(
    Output('radios', 'children'),
    Input('url', 'pathname'),
    State('dynamic-add-graph', 'n_clicks'))
def variable_layout_of_x_and_y_options(pathname, n_clicks):
    if pathname == "/":
        x_col_list, y_col_list = outsourced_app_layout.get_config()
        return outsourced_app_layout.changing_layout(x_col_list, y_col_list, n_clicks)
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
    Output('table', 'columns'),
    Output('table', 'data'),
    Input('start_time_config', 'value'),
    Input('end_time_config', 'value'))
def change_table(start_time, end_time):
    df = config_menu.change_table(start_time, end_time)
    columns = [{"name": i, "id": i} for i in df.columns]
    data = df.to_dict('records')
    return columns, data


@app.callback(
    Output('button-output', 'children'),
    Input('submit-config', 'n_clicks'),
    State('x-values-config', 'value'),
    State('y-values-config', 'value'))
def change_config(n_clicks, x_values, y_values):
    if n_clicks > 0:
        config_menu.write_config(x_values, y_values)
        return 'Config file has been changed'
    else:
        return 'Click to change config'


@app.callback(
    Output({'type': 'graph', 'index': MATCH}, 'figure'),
    Output({'type': 'number_of_values', 'index': MATCH}, 'children'),
    Input({'type': 'my-date-picker-range', 'index': MATCH}, 'start_date'),
    Input({'type': 'my-date-picker-range', 'index': MATCH}, 'end_date'),
    Input({'type': 'x-values', 'index': MATCH}, 'value'),
    Input({'type': 'y-values', 'index': MATCH}, 'value'),
    Input({'type': 'weekday', 'index': MATCH}, 'value'),
    Input({'type': 'start_time', 'index': MATCH}, 'value'),
    Input({'type': 'end_time', 'index': MATCH}, 'value'),
    Input({'type': 'hours', 'index': MATCH}, 'value'),
    Input({'type': 'months', 'index': MATCH}, 'value'),
    Input({'type': 'weekly', 'index': MATCH}, 'value'),
    Input({'type': 'restaurant', 'index': MATCH}, 'value'),
    Input({'type': 'date-selector', 'index': MATCH}, 'value'),
    Input({'type': 'both-y', 'index': MATCH}, 'value'), prevent_initial_call=True)
def visualize_func(min_date, max_date, x_value, y_value, weekday, start_time, end_time, hours,
                   months, weekly, restaurant, date_selector, both_y):

    try:
        fig, number = graphs.generate_figure(min_date, max_date, x_value, y_value, weekday, start_time, end_time, hours,
                                     months, weekly, restaurant, date_selector, both_y, graphs.df_sorted)
    except Exception:
        print('error generating figure')
        print(traceback.format_exc())
        return graphs.get_empty_figure(), 'Output: {}'.format(0)

    return fig, 'Output: {}'.format(number)


@app.callback(  #collapse für Stunden grupieren
    Output({'type': "collapse", 'index': MATCH}, "is_open"),
    Input({'type': 'x-values', 'index': MATCH}, 'value'))
def toggle_collapse(radios):
    if radios == graphs.uhrzeit:
        return True
    return False


if __name__ == "__main__":
    app.run_server(debug=True)
