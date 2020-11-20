import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly
import plotly.graph_objects as go

import time
import json

import datetime as dt

from ..api_sensor_data.api import get_sensor_data


def register_collect_data_callback(app):

    def get_current_time():
        """ Helper function to get the current time in seconds. """

        now = dt.datetime.now()
        total_time = (now.hour * 3600) + (now.minute * 60) + (now.second)
        return total_time


    @app.callback(
        [
            Output("sensor-flex-1", "figure"),
            Output("sensor-flex-2", "figure"),
            Output("sensor-flex-3", "figure"),
            Output("sensor-flex-4", "figure"),
            Output("sensor-pressure-1", "figure")
        ],
        [
            Input("sensor-update-interval", "n_intervals"),
        ]
    )
    def update_interval(interval):

        
        
        df = get_sensor_data()

        df['flex1'] = (df["flex1"] - 3.48) /  (-0.0170)
        df['flex2'] = (df["flex2"] - 3.62) /  (-0.0110)
        df['flex3'] = (df["flex3"] - 3.75) /  (-0.0049)
        df['flex4'] = (df["flex4"] - 4.00) /  (-0.0067)
        
        trace1 = dict(
            type="scatter",
            # x = (df['timestamp']),
            y = df['flex1'],
            line={"color": "#42C4F7"},
            hoverinfo="skip",
            mode="lines",
        )
        trace2 = dict(
            type="scatter",
            # x = (df['timestamp']),
            y = df['flex2'],
            line={"color": "#42C4F7"},
            hoverinfo="skip",
            mode="lines",
        )
        trace3 = dict(
            type="scatter",
            # x = (df['timestamp']),
            y = df['flex3'],
            line={"color": "#42C4F7"},
            hoverinfo="skip",
            mode="lines",
        )
        trace4 = dict(
            type="scatter",
            # x = (df['timestamp']),
            y = df['flex4'],
            line={"color": "#42C4F7"},
            hoverinfo="skip",
            mode="lines",
        )


        flex_layout = dict(
            plot_bgcolor = "#e5ecf6",
            margin=dict(l=50, r=30, t=30, b=50),
            xaxis = dict(
                tickmode = 'array',
                tickvals = [0, 50, 100, 150, 200],
                ticktext = ["200", "150", "100", "50", "0"],
                title = "Time Elapsed (s)",
                zeroline = False,
                gridcolor = "#ffffff",
            ),
            yaxis = dict(
                range = [0,120],
                title = "Angle (Degrees)",
                gridcolor = "#ffffff",
            )
        )
        flex_layout_3 = dict(
            plot_bgcolor = "#e5ecf6",
            margin=dict(l=50, r=30, t=30, b=50),
            xaxis = dict(
                tickmode = 'array',
                tickvals = [0, 50, 100, 150, 200],
                ticktext = ["200", "150", "100", "50", "0"],
                title = "Time Elapsed (s)",
                zeroline = False,
                gridcolor = "#ffffff",
            ),
            yaxis = dict(
                range = [0,180],
                title = "Angle (Degrees)",
                gridcolor = "#ffffff",
            )
        )
        fig1 =  dict(data = [trace1], layout = flex_layout)
        fig2 =  dict(data = [trace2], layout = flex_layout)
        fig3 =  dict(data = [trace3], layout = flex_layout_3)
        fig4 =  dict(data = [trace4], layout = flex_layout)
        

        trace5 = dict(
            type="scatter",
            y = df["pres1"],
            line={"color": "#42C4F7"},
            hoverinfo="skip",
            mode="lines",
        )
        pressure_layout = dict(
            plot_bgcolor = "#e5ecf6",
            margin=dict(l=50, r=30, t=30, b=30),
            xaxis = dict(
                tickmode = 'array',
                tickvals = [0, 50, 100, 150, 200],
                ticktext = ["200", "150", "100", "50", "0"],
                title = "Time Elapsed (s)",
                zeroline = False,
                gridcolor = "#ffffff",
            ),
            yaxis = dict(
                range = [0,0.5],
                title = "Voltage (V)",
                gridcolor = "#ffffff",
            )
        )
        fig5 = dict(data=[trace5], layout=pressure_layout)
        
        return fig1, fig2, fig3, fig4, fig5