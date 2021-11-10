import graphs
import dash_bootstrap_components as dbc
from dash import html


def changing_layout(x_col_list, y_col_list, n_clicks):
    layout = html.Div(children=[
        dbc.Row([dbc.Col(html.Div(
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


df = graphs.df_sorted
unique_restaurant = df["restaurant_name"].unique().tolist()
unique_restaurant.append("all")
