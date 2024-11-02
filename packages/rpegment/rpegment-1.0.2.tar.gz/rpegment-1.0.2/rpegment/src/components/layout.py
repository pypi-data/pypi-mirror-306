from dash import Dash, dcc, html

from . import control, raw, segment, analysis


def create_layout(app: Dash) -> html.Div:
    return html.Div(
        children=[
            html.Div(
                children=[
                    html.Div(
                        children=[raw.render(app)],
                        style={
                            'width': '50%',
                        }
                    ),
                    html.Div(
                        children=[segment.render(app)],
                        style={
                            'width': '50%',
                        }
                    )
                ],
                style={
                    'display': 'flex',
                    'flex-direction': 'row',
                    'gap': '5px',
                    'width': '100%',
                }
            ),
            html.Div(
                children=[control.render(app)],
                style={
                    'width': '100%',
                }
            ),
            html.Div(
                children=[analysis.render(app)],
                style={
                    'width': '100%',
                }
            ),
        ],
        style={
            'display': 'flex',
            'flex-direction': 'column',
            'align-items': 'center',
            'height': '98%',
            'width': '98%',
        }
    )
