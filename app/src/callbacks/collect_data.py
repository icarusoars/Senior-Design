import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import time
import json

import datetime as dt

from ..api_sensor_data.api import get_wind_data, get_sensor_data


def register_collect_data_callback(app):

    def get_current_time():
        """ Helper function to get the current time in seconds. """

        now = dt.datetime.now()
        total_time = (now.hour * 3600) + (now.minute * 60) + (now.second)
        return total_time

    # @app.callback(
    #     [
    #         Output("sensor-flex-1", "figure"),
    #         Output("sensor-flex-2", "figure"),
    #         Output("sensor-pressure-1", "figure"),
    #         Output("sensor-pressure-2", "figure")
    #     ],
    #     [
    #         Input("sensor-update-interval", "n_intervals")
    #     ]
    # )
    # def get_dummy_data(interval):
    #     """
    #     Get the data collected by sensor.
    #     Return data in format for plotly to graph.
    #     :params interval: update the plotly graph based on this interval
    #     """

    #     total_time = get_current_time()
    #     df = get_wind_data(total_time - 200, total_time)

    #     trace = dict(
    #         type="scatter",
    #         y = df["Speed"],
    #         line={"color": "#42C4F7"},
    #         hoverinfo="skip",
    #         mode="lines",
    #     )

    #     layout = dict(
    #         font={"color": "#fff"},
    #         xaxis={
    #             "range": [0, 200],
    #             "showline": True,
    #             "zeroline": False,
    #             "fixedrange": True,
    #             "tickvals": [0, 50, 100, 150, 200],
    #             "ticktext": ["200", "150", "100", "50", "0"],
    #             "title": "Time Elapsed (sec)",
    #         },
    #         yaxis={
    #             "range": [
    #                 min(0, min(df["Speed"])),
    #                 max(45, max(df["Speed"]) + max(df["SpeedError"])),
    #             ],
    #             "showgrid": True,
    #             "showline": True,
    #             "fixedrange": True,
    #             "zeroline": False,
    #             "nticks": max(6, round(df["Speed"].iloc[-1] / 10)),
    #         },
    #         margin=dict(l=20, r=20, t=20, b=20),
    #     )

    #     output = dict(data=[trace], layout=layout)

    #     return output, output, output, output


    # @app.callback(
    #     Output("test_p", "children"),
    #     [
    #         Input("sensor-update-interval", "n_intervals"),
    #     ]
    # )
    # def test_interval(interval):
    #     start_time = time.time()
    #     sensor_data = get_sensor_data(socket)
    #     print(interval)
    #     print(time.time() - start_time)
    #     return json.dumps(sensor_data)

    

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
        
        trace1 = dict(
            type="scatter",
            y = df["flex1"],
            line={"color": "#42C4F7"},
            hoverinfo="skip",
            mode="lines",
        )
        trace2 = dict(
            type="scatter",
            y = df["flex2"],
            line={"color": "#42C4F7"},
            hoverinfo="skip",
            mode="lines",
        )
        trace3 = dict(
            type="scatter",
            y = df["flex3"],
            line={"color": "#42C4F7"},
            hoverinfo="skip",
            mode="lines",
        )
        trace4 = dict(
            type="scatter",
            y = df["flex4"],
            line={"color": "#42C4F7"},
            hoverinfo="skip",
            mode="lines",
        )
        trace5 = dict(
            type="scatter",
            y = df["pres1"],
            line={"color": "#42C4F7"},
            hoverinfo="skip",
            mode="lines",
        )

        layout = dict(
            font={"color": "#fff"},
            xaxis={
                "range": [0, 200],
                "showline": True,
                "zeroline": False,
                "fixedrange": True,
                "tickvals": [0, 50, 100, 150, 200],
                "ticktext": ["200", "150", "100", "50", "0"],
                "title": "Time Elapsed (sec)",
            },
            yaxis={
                "range": [
                    0,5,
                ],
                "showgrid": True,
                "showline": True,
                "fixedrange": True,
                "zeroline": False,
                "nticks": max(6, round(df["flex1"].iloc[-1] / 10)),
            },
            margin=dict(l=20, r=20, t=20, b=20),
        )

        output1 = dict(data=[trace1], layout=layout)
        output2 = dict(data=[trace2], layout=layout)
        output3 = dict(data=[trace3], layout=layout)
        output4 = dict(data=[trace4], layout=layout)
        output5 = dict(data=[trace5], layout=layout)
        
        return output1, output2, output3, output4, output5