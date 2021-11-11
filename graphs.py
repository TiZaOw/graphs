import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash_bootstrap_templates import load_figure_template
import datetime
from statistics import mean
from plotly.subplots import make_subplots
import locale
import numpy as np
import find_right_columns

# df = pd.read_excel('mongo_db/new_york_pizza_clean.xlsx')

locale.setlocale(locale.LC_TIME, 'de_DE')
load_figure_template("litera")

datum = find_right_columns.datum
uhrzeit = find_right_columns.uhrzeit
wochentag = find_right_columns.wochentag
y_axis = find_right_columns.y_axis


def get_default_fig():  # not used right-now
    fig = px.bar(df_sorted, x=datum, y=y_axis[0])
    return fig


def get_empty_figure():
    from PIL import Image
    img = np.array(Image.open(f"assets/{'logo.jpg'}"))
    fig = px.imshow(img)     # TODO: just 4fun, remove later..?
    # fig = make_subplots(specs=[[{"secondary_y": True}]])
    return fig


def sort_by_dates(df_date):
    df_date[datum] = pd.to_datetime(df_date[datum], dayfirst=True)
    df_date = df_date.sort_values(by=datum)
    df_date[datum] = df_date[datum].dt.strftime("%d.%m.%Y")
    return df_date


df_sorted = sort_by_dates(find_right_columns.df_clean)


def generate_figure(min_date, max_date, x_value, y_value, weekday, start_time, end_time, hours,
                    months, weekly, restaurant, wmj_selector, both_y, df):
    # TODO "filter setzten" Funkionalität. Startet mit keinem Filter und kann hinzegfügt werden
    df = all_filters(min_date, max_date, weekday, start_time, end_time, restaurant, wmj_selector, df)

    number = df.shape[0]
    if weekly != 'no':
        fig = weekly_trend(df, y_value)
        return fig, number
    if both_y != 'no':
        x_col_list, y_col_list = find_right_columns.get_config()
        df1 = get_x_axis(x_value, y_col_list[0], hours, df, months)
        df2 = get_x_axis(x_value, y_col_list[1], hours, df, months)
        fig = both_y_figure(x_value, y_col_list, df1, df2)
        return fig, number

    df = get_x_axis(x_value, y_value, hours, df, months)

    fig = draw_figure(x_value, y_value, df)

    return fig, number


def all_filters(min_date, max_date, weekday, start_time, end_time, restaurant, wmj_selector, df):
    if restaurant != "all":
        df = filter_for_restaurant(restaurant, df)
    if wmj_selector != 'no':
        df = filter_for_date_with_selector(wmj_selector, df)
    if min_date is not None and max_date is not None:
        df = filter_for_date(min_date, max_date, df)
    if weekday != "all":
        df = filter_for_weekday(weekday, df)
    if start_time != '00:00' or end_time != '24:00':
        df = filter_for_time(start_time, end_time, df)
    return df


def get_x_axis(x, y, hours, df, month_grouped):
    if x == datum and month_grouped:
        df = group_month(df, y)
    if x == uhrzeit:
        df = group_hours(df, y, hours)
    if x == wochentag:
        df = group_weekdays(df, y)
    return df


def filter_for_restaurant(restaurant, df):
    df_restaurant = df.loc[restaurant == df["restaurant_name"]]
    return df_restaurant


def filter_for_date_with_selector(range, df):
    now = datetime.datetime.now()
    min_date = now
    if range == 'w':
        min_date = now - datetime.timedelta(days=7)
    elif range == 'm':
        min_date = now - pd.DateOffset(months=1)
    elif range == '3m':
        min_date = now - pd.DateOffset(months=3)
    elif range == 'j':
        min_date = now - pd.DateOffset(months=12)
    df_date = df.loc[min_date < pd.to_datetime(df[datum], dayfirst=True)]
    return df_date


def filter_for_date(min_date, max_date, df):
    min_in_datetime = datetime.datetime.strptime(min_date, '%Y-%m-%d')
    max_in_datetime = datetime.datetime.strptime(max_date, '%Y-%m-%d')

    df_date = df.loc[min_in_datetime < pd.to_datetime(df[datum], dayfirst=True)]
    df_date = df_date.loc[max_in_datetime > pd.to_datetime(df[datum], dayfirst=True)]
    return df_date


def filter_for_weekday(day, df):
    df_wd = df.loc[pd.to_datetime(df[datum], dayfirst=True).dt.strftime('%A') == day]
    return df_wd


def filter_for_time(start_time, end_time, df):
    if start_time < end_time:
        df_time = df.loc[start_time <= df[uhrzeit]]
        df_time = df_time.loc[end_time >= df_time[uhrzeit]]
    else:
        df_time = df.loc[np.logical_or(start_time <= df[uhrzeit], end_time >= df[uhrzeit])]
    return df_time


def group_month(df, y_value):
    df_month = pd.DataFrame({datum: df[datum], y_value: df[y_value].astype(float)})
    df_month[datum] = pd.to_datetime(df_month[datum], dayfirst=True)
    df_month = df_month.resample("M", on=datum).mean()
    df_month = df_month.reset_index()
    df_month[datum] = df_month[datum].dt.strftime("%m.%Y")
    return df_month


def group_hours(df, y_value, hours):
    if hours == 0:
        return df.sort_values(by=uhrzeit)
    df_time = pd.DataFrame({uhrzeit: df[uhrzeit], y_value: df[y_value].astype(float)})
    time_range = str(hours) + "H"
    df_time[uhrzeit] = pd.to_datetime(df_time[uhrzeit], format="%H:%M")
    df_time = df_time.resample(time_range, on=uhrzeit).mean()
    df_time = df_time.reset_index()  # notwendig, weil resample den index verschiebt
    df_time[uhrzeit] = df_time[uhrzeit].dt.strftime("%H:%M")
    return df_time


def group_weekdays(df, y_value):
    days = {0: "Montag", 1: "Dienstag", 2: "Mittwoch", 3: "Donnerstag",
            4: "Freitag", 5: "Samstag", 6: "Sonntag"}
    df_week = pd.DataFrame({wochentag: pd.to_datetime(df[datum], dayfirst=True).dt.weekday,  # wochentage als zahlen
                            y_value: df[y_value].astype(float)})
    df_week = df_week.groupby(df_week[wochentag]).mean()
    df_week = df_week.reset_index()
    df_week = df_week.replace({wochentag: days})  # zahlen zu wochentage
    return df_week


def draw_figure(x, y, data):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    for contestant, group in data.groupby(x, sort=False):
        avg = list(group[y].astype(float))
        avg = mean(avg)
        m = [avg]
        rounded = "%.2f" % avg
        fig = fig.add_trace(go.Bar(x=group[x], y=m,
                                   hovertemplate=f"{x}: {contestant} <br>{y}: {rounded} <extra></extra>",
                                   name=contestant, text=rounded, showlegend=False))
    return fig


def both_y_figure(x, y_col_list, df1, df2):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    df_list = [df1, df2]
    color = {y_col_list[0]: 'red',
             y_col_list[1]: 'blue'}

    def check_showlegend(check_var, run_var):
        if check_var != run_var:
            bool = True
        else:
            bool = False
        return bool

    check_showlegend_var = -1
    for i in range(len(df_list)):

        for contestant, group in df_list[i].groupby(x, sort=False):

            avg = list(group[y_col_list[i]].astype(float))
            avg = mean(avg)
            m = [avg]
            rounded = "%.2f" % avg
            bar = go.Bar(x=group[x], y=m,
                         hovertemplate=f"{x}: {contestant} <br>{y_col_list[i]}: {rounded} <extra></extra>",
                         name=y_col_list[i], legendgroup=str(y_col_list[i]), marker={'color': color[y_col_list[i]]},
                         text=rounded, opacity=0.7, showlegend=check_showlegend(check_showlegend_var, i))
            if i == 0:
                fig = fig.add_trace(bar, secondary_y=False)
            else:
                fig = fig.add_trace(bar, secondary_y=True)

            if check_showlegend_var != i:
                check_showlegend_var = i

    fig.update_layout(yaxis=dict(range=[0, 5]), yaxis2=dict(range=[0, 5]))

    return fig


def weekly_trend(df, y_value):
    df_weekly = pd.DataFrame({datum: df[datum], y_value: df[y_value].astype(float)})
    df_weekly[datum] = pd.to_datetime(df_weekly[datum], dayfirst=True)
    df_weekly = df_weekly.resample("7d", on=datum).mean()
    df_weekly = df_weekly.reset_index()
    df_weekly[datum] = df_weekly[datum].dt.strftime("%d.%m.%y")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_weekly[datum],
                             y=smoothTriangle(df_weekly[y_value], 5),
                             # mode='markers',
                             # marker=dict(size=2, color='rgb(0, 0, 0)'),
                             name='Sine'
                             ))
    return fig


# 1:1 copied from web, TODO: sollte verbessert werden, schießt errors bei zu wenig daten...was sinn macht
def smoothTriangle(data, degree):
    triangle = np.concatenate((np.arange(degree + 1), np.arange(degree)[::-1]))  # up then down
    smoothed = []

    for i in range(degree, len(data) - degree * 2):
        point = data[i:i + len(triangle)] * triangle
        smoothed.append(np.sum(point) / np.sum(triangle))
    # Handle boundaries
    smoothed = [smoothed[0]] * int(degree + degree / 2) + smoothed
    while len(smoothed) < len(data):
        smoothed.append(smoothed[-1])
    return smoothed
