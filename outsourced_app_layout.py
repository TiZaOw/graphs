import graphs
import dash_bootstrap_components as dbc
import dash_html_components as html
import configparser


def change_col_list():
    config = configparser.ConfigParser()
    config.read('config.ini')

    x_values = config['values']['x-values']
    y_values = config['values']['y-values']

    col_list = graphs.df.columns
    x_col_list = [e for e in col_list if e in x_values]
    y_col_list = [e for e in col_list if e in y_values]
    return x_col_list, y_col_list


def changing_layout(x_col_list, y_col_list):
    layout = html.Div(children=[dbc.Row([
        dbc.Col(html.Div(
            dbc.RadioItems(
                id="x-values",
                className="btn-group",
                labelClassName="btn btn-primary",
                labelCheckedClassName="active",
                options=[
                    {'label': i, 'value': i } for i in x_col_list
                ],
                value=x_col_list[0],
            ),className='radio-group'),align='center', width='auto'),
    ],justify='center'),
        dbc.Col(html.Div(
            dbc.RadioItems(
                id="y-values",
                className="btn-group",
                labelClassName="btn btn-secondary",
                labelCheckedClassName="active",
                options=[
                    {'label': i, 'value': i } for i in y_col_list
                ],
                value=y_col_list[0]
            ),className='radio-group'),align='center', width='auto'),])

    return layout