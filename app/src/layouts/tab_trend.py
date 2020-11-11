import dash
import dash_core_components as dcc
import dash_html_components as html


tab_trend = dcc.Tab(label='Ankle Stress Trend', children=[
    dcc.Graph(
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [8, 9, 2],
                    'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5],
                'type': 'bar', 'name': u'Montréal'},
            ]
        }
    )
])