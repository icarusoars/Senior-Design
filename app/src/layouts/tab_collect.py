import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd
import datetime as dt

# the interval in milliseconds to update graphs
UPDATE_INTERVAL = 100


tab_collect = dcc.Tab(label='Collect Data', children=[
    html.Div(
        className = "collect_data_container",
        children = [
            html.Div(
                className = "collect_data_left",
                children = [
                    html.H3("Data Collection"),
                    html.P("""
                    Use the buttons below to start and stop recording data
                    from the basketball shoe.
                    """),
                    # html.Button('Connect Bluetooth', id = 'connect_button', className='collect_buttons'),
                    html.Button('Start Collect', id = 'start_button', className='collect_buttons'),
                    html.Button('End Collect', id = 'end_button', className='collect_buttons'),
                    html.Button('Save & Analyze', id = 'save_button', className='collect_buttons'),
                    html.P(id = 'test_p')
                ]
            ),
            html.Div(
                className = "collect_data_right",
                children = [
                    dcc.Interval(
                        disabled = False,
                        id="sensor-update-interval",
                        interval=int(UPDATE_INTERVAL),
                        n_intervals=0,
                    ),
                    
                    
                    html.Div(
                        className = 'sensor-data-container',
                        children = [
                            html.Div(
                                children = [html.H5("Flex Sensor 1", className="sensor-data-title")]
                            ),
                            dcc.Graph(
                                className = 'sensor-data-graph',
                                id="sensor-flex-1",
                            )
                    ]),
                    html.Div(
                        className = 'sensor-data-container',
                        children = [
                            html.Div(
                                [html.H5("Flex Sensor 2", className="sensor-data-title")]
                            ),
                            dcc.Graph(
                                className = 'sensor-data-graph',
                                id="sensor-flex-2",
                            )
                    ]),
                    html.Div(
                        className = 'sensor-data-container',
                        children = [
                            html.Div(
                                [html.H5("Flex Sensor 3", className="sensor-data-title")]
                            ),
                            dcc.Graph(
                                className = 'sensor-data-graph',
                                id="sensor-flex-3",
                            )
                    ]),
                    html.Div(
                        className = 'sensor-data-container',
                        children = [
                            html.Div(
                                [html.H5("Flex Sensor 4", className="sensor-data-title")]
                            ),
                            dcc.Graph(
                                className = 'sensor-data-graph',
                                id="sensor-flex-4",
                            )
                    ]),
                    html.Div(
                        className = 'sensor-data-container',
                        children = [
                            html.Div(
                                [html.H5("Pressure Sensor 1", className="sensor-data-title")]
                            ),
                            dcc.Graph(
                                className = 'sensor-data-graph',
                                id="sensor-pressure-1",
                            )
                    ]),

                ]
            )
        ]
    ),
    
])
