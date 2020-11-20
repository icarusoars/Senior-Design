import dash
import dash_core_components as dcc
import dash_html_components as html


tab_trend = dcc.Tab(label='Ankle Stress Trend', children=[
    
    html.Div(
        className = "trend-container",
        children = [
            html.Div(
                className = "trend-top-container",
                children = [
                    html.Div(
                        className = "trend-top-left",
                        children = [
                            dcc.Graph(
                                id = "histogram-avg-stress"
                            )
                        ]
                    ),
                    html.Div(
                        className = "trend-top-right",
                        children = [
                            dcc.Graph(
                                id = "histogram-ankle-variance"
                            )
                        ]
                    )
                ]
            ),
            html.Div(
                className = "trend-bottom-container",
                children = [
                    dcc.Graph()
                ]
            ),
        ]
    )
    
])