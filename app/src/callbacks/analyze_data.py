import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import time
import json
import pandas as pd

import plotly
import plotly.graph_objects as go

from ..api_process_data.process_data import get_session_df, \
                                            get_metrics_by_time, \
                                            get_metrics_by_events



def register_analyze_data_callback(app):


    @app.callback(
        [
            Output("hidden-div", "children"),
            Output("hidden-div-thresholds", "children")
        ],
        [
            Input("analyze_data_button", "n_clicks")
        ]
    )
    def refresh_data(n_clicks):
        df, thresholds = get_session_df()
        # serialize session data
        return (df.to_json(), json.dumps(thresholds))

    @app.callback(
        [
            Output("processed-data-graph", "figure"),
            Output("analyze_data_header", "children")
        ],
        [
            Input("hidden-div", "children"),
            Input("hidden-div-thresholds", "children"),
            Input('analyze_plane_dropdown', 'value')
        ]
    )
    def regresh_graph(session_data, thresholds, dropdown_value):
        # unserialize session data
        df = pd.read_json(session_data)
        thresholds = json.loads(thresholds)

        # select the plane to analyze
        # frontal plane: flex1 and flex2 sensors
        # sagittal plane: flex3 and flex4 sensors
        x = df['timestamp']
        y = df[dropdown_value]


        # assemble processed-data-graph
        trace1 = dict(
            type="scatter",
            x = x,
            y = y,
            line={"color": "#42C4F7"},
            hoverinfo="skip",
            mode="lines",
        )

        

        fig_angle = go.Figure(data = [trace1])

        # add threshold traces
        fig_angle.add_shape(
            type = "line",
            x0 = min(x),
            x1 = max(x),
            y0 = thresholds[dropdown_value]['max'] * 0.6,
            y1 = thresholds[dropdown_value]['max'] * 0.6,
            line_color = "Red"
        )
        fig_angle.add_shape(
            type = "line",
            x0 = min(x),
            x1 = max(x),
            y0 = thresholds[dropdown_value]['min'] * 0.6,
            y1 = thresholds[dropdown_value]['min'] * 0.6,
            line_color = "Red"
        )

        fig_angle.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis_title = "Time",
            yaxis_title = "Angle (degrees)",
            xaxis = dict(
                tickmode = 'array',
                tickvals = [60_000*i for i in range(max(x) // 60_000)],
                ticktext = [f"{i}:00" for i in range(max(x) // 60_000)]
            )
        )
        fig_angle.update_xaxes(rangeslider_visible = True)

        header_text = "Frontal Plane Angle" if dropdown_value == "frontal_plane" \
                        else "Sagittal Plane Angle"

        return (fig_angle, header_text)


    @app.callback(
        # [
            # Output("relayout-test", "children"),
            Output("metrics-time-graph", "figure"),
        # ],
        [
            Input("hidden-div", "children"),
            Input("hidden-div-thresholds", "children"),
            Input("processed-data-graph", "relayoutData"),
            Input('analyze_plane_dropdown', 'value')
        ]
    )
    def update_metrics_by_time(session_data, thresholds, relayoutData, dropdown_value):

        # unserialize session data
        df = pd.read_json(session_data)
        thresholds = json.loads(thresholds)

        print(df.shape)

        # subselect dataframe if xaxis range is changed
        if relayoutData:

            if ("xaxis.range[0]" in relayoutData) and \
               ("xaxis.range[1]" in relayoutData):
                time_start = relayoutData['xaxis.range[0]']
                time_end   = relayoutData['xaxis.range[1]']

                df = df[(df['timestamp'] >= time_start) &
                        (df['timestamp'] <= time_end)]
                
                print("df filtered")
                print(df.shape)
            
            elif "xaxis.range" in relayoutData:
                time_start = relayoutData['xaxis.range'][0]
                time_end   = relayoutData['xaxis.range'][1]

                df = df[(df['timestamp'] >= time_start) &
                        (df['timestamp'] <= time_end)]

                print("df filtered")
                print(df.shape)


        tot_stress, avg_stress, std = get_metrics_by_time(df, dropdown_value, thresholds)
        # print(tot_stress, avg_stress, std)

        fig_metrics = plotly.subplots.make_subplots(
            rows = 3, cols = 1,
            # specs=[[{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}]],
            specs=[[{"type": "indicator"}], [{"type": "indicator"}], [{"type": "indicator"}]],
            vertical_spacing = 0.2
        )
        fig_metrics.add_trace(
            go.Indicator(
                mode = "number",
                value = tot_stress,
                title_text = "<b>Total Stress</b>",
                number_font_color = "#42C4F7"

            ),
            row = 1,
            col = 1
        )
        fig_metrics.add_trace(
            go.Indicator(
                mode = "number",
                value = avg_stress,
                title_text = "<b>Average Stress</b>",
                number_font_color = "#42C4F7"
            ),
            row = 2,
            col = 1,
            
        )
        fig_metrics.add_trace(
            go.Indicator(
                mode = "number",
                value = std,
                title_text = "<b>Angle s.d.</b>",
                number_font_color = "#42C4F7" 
            ),
            row = 3,
            col = 1,
            
        )
        fig_metrics.update_layout(
            margin=dict(l=0, r=0, t=30, b=30)
        )

        # return (json.dumps(relayoutData, indent = 4), fig_metrics)
        return fig_metrics

    @app.callback(
        # [
            # Output("relayout-test", "children"),
            Output("metrics-events-graph", "figure"),
        # ],
        [
            Input("hidden-div", "children"),
            Input("hidden-div-thresholds", "children"),
            Input("processed-data-graph", "relayoutData"),
            Input('analyze_plane_dropdown', 'value'),
            Input('events-radiobutton', 'value')

        ]
    )
    def update_metrics_by_events(session_data, thresholds, relayoutData,
                                 dropdown_value, radio_value):

        # unserialize session data
        df = pd.read_json(session_data)
        thresholds = json.loads(thresholds)

        print(df.shape)

        # subselect dataframe if xaxis range is changed
        if relayoutData:

            if ("xaxis.range[0]" in relayoutData) and \
               ("xaxis.range[1]" in relayoutData):
                time_start = relayoutData['xaxis.range[0]']
                time_end   = relayoutData['xaxis.range[1]']

                df = df[(df['timestamp'] >= time_start) &
                        (df['timestamp'] <= time_end)]
                
                print("df filtered")
                print(df.shape)
            
            elif "xaxis.range" in relayoutData:
                time_start = relayoutData['xaxis.range'][0]
                time_end   = relayoutData['xaxis.range'][1]

                df = df[(df['timestamp'] >= time_start) &
                        (df['timestamp'] <= time_end)]

                print("df filtered")
                print(df.shape)

        tot_stress, avg_stress, std = get_metrics_by_events(df, dropdown_value,
                                                          thresholds, radio_value)

        fig_metrics = plotly.subplots.make_subplots(
            rows = 3, cols = 1,
            # specs=[[{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}]],
            specs=[[{"type": "indicator"}], [{"type": "indicator"}], [{"type": "indicator"}]],
            vertical_spacing = 0.2
        )
        fig_metrics.add_trace(
            go.Indicator(
                mode = "number",
                value = tot_stress,
                title_text = "<b>Total Stress</b>",
                number_font_color = "#42C4F7"

            ),
            row = 1,
            col = 1
        )
        fig_metrics.add_trace(
            go.Indicator(
                mode = "number",
                value = avg_stress,
                title_text = "<b>Average Stress</b>",
                number_font_color = "#42C4F7"
            ),
            row = 2,
            col = 1,
            
        )
        fig_metrics.add_trace(
            go.Indicator(
                mode = "number",
                value = std,
                title_text = "<b>Angle s.d.</b>",
                number_font_color = "#42C4F7" 
            ),
            row = 3,
            col = 1,
            
        )
        fig_metrics.update_layout(
            margin=dict(l=0, r=0, t=30, b=30)
        )

        # return (json.dumps(relayoutData, indent = 4), fig_metrics)
        return fig_metrics
