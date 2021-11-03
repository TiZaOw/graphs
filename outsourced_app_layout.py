import graphs
import dash_bootstrap_components as dbc
from dash import html
import configparser

df = graphs.df_clean


def get_config():
    config = configparser.ConfigParser()
    config.read('config.ini')

    x_values = config['values']['x-values']
    y_values = config['values']['y-values']
    col_list = df.columns

    x_col_list = [e for e in col_list if e in x_values]
    y_col_list = [e for e in col_list if e in y_values]
    return x_col_list, y_col_list


def changing_layout(x_col_list, y_col_list, n_clicks):
    layout = html.Div(children=[dbc.Row([
        dbc.Col(html.Div(
            dbc.RadioItems(
                id={'type': "x-values", 'index': n_clicks},
                className="btn-group",
                labelClassName="btn btn-primary",
                labelCheckedClassName="active",
                options=[{'label': i.title(), 'value': i} for i in x_col_list],
                value=x_col_list[0],
            ), className='radio-group'), align='center', width='auto'),
        ], justify='center'),
        dbc.Row([dbc.Col(html.Div(
            dbc.RadioItems(
                id={'type': "y-values", 'index': n_clicks},
                className="btn-group",
                labelClassName="btn btn-secondary",
                labelCheckedClassName="active",
                options=[{'label': i.title(), 'value': i} for i in y_col_list],
                value=y_col_list[0]
            ), className='radio-group'), align='center', width='auto')
        ], justify='center')
    ])

    return layout


unique_restaurant = df["restaurant_name"].unique().tolist()
