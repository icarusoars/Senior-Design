# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


"""
LAYOUT
"""
from src.layouts.tab_collect import tab_collect
from src.layouts.tab_analyze import tab_analyze
from src.layouts.tab_trend import tab_trend

app.layout = html.Div(children=[
    html.H1(id = "app-title", children='Ankle Stress Monitor'),
    html.H6(id = "app-subtitle", children = "An App that Helps Basketball Players Minimize Injury Risk"),
    dcc.Tabs(
        id = "tabs",
        children = [
            tab_collect,
            tab_analyze,
            tab_trend
        ]
    )
    
])



"""
CALLBACKS
"""
from src.callbacks.collect_data import register_collect_data_callback
from src.callbacks.analyze_data import register_analyze_data_callback

if __name__ == '__main__':

    register_collect_data_callback(app)
    register_analyze_data_callback(app)

    app.run_server(debug=True, use_reloader = True)