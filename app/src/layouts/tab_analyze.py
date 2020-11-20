import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly
import plotly.graph_objects as go

# import sqlite3
import pandas as pd
# import pathlib





"""-------- Analyze Data Tab Layout --------"""


tab_analyze = dcc.Tab(label='Analyze Session', children=[
    html.Div(
        className = "analyze-container",
        children = [
            html.Div(
                className = "analyze-top",
                children = [
                    html.Div(
                        id = "analyze_header_div",
                        children = [
                            html.H2("Frontal Plane Angle", id = "analyze_data_header"),
                            dcc.Dropdown(
                                id='analyze_plane_dropdown',
                                options=[
                                    {'label': 'Frontal Plane', 'value': 'frontal_plane'},
                                    {'label': 'Sagittal Plane', 'value': 'sagittal_plane'},
                                ],
                                value='frontal_plane'
                            ),
                            html.Button(id = "analyze_data_button", children = "Refresh Session Data"),
                        ]
                    ),
                    dcc.Graph(
                        id = "processed-data-graph",
                        # figure = fig_angle
                    ),
                    html.Div(
                        id=  "hidden-div",
                        style = {'display': 'none'}
                    ),
                    html.Div(
                        id = "hidden-div-thresholds",
                        style = {'display': 'none'}
                    )
                ]
            ),
            html.Div(
                className = "analyze-bottom",
                children = [
                    html.Div(
                        className = "analyze-bottom-left",
                        children = [
                            html.H2("Metrics by Time"),
                            dcc.Graph(
                                id = "metrics-time-graph",
                                className = "metrics-graph",
                                # figure = fig_metrics,
                            ),
                            # html.Pre(id='relayout-test')
                        ]
                    ),
                    html.Div(
                        className = "analyze-bottom-right",
                        children = [
                            html.H2("Metrics by Events"),
                            dcc.RadioItems(
                                id = "events-radiobutton",
                                options = [
                                    {'label': "Jumps", 'value': "jumps"},
                                    {'label': "Landings", 'value': "landings"},
                                ],
                                value = 'jumps',
                                labelStyle = {
                                    'display': "inline-block",
                                    'padding-right': '2em',
                                    'padding-left': '2em'
                                }
                            ),
                            dcc.Graph(
                                id = "metrics-events-graph",
                                className = "metrics-graph",
                                # figure = fig_metrics
                            )
                        ]
                    )
                ]
            )
        ]
    )
    
    
])