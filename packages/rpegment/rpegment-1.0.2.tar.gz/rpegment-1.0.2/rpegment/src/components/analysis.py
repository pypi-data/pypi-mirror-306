from dash import Dash, html

from . import ids, image


def render(app: Dash) -> html.Div:

    return html.Div(
        children=[
            html.Div(
                children=[image.render(ids.IMAGE_COLORBAR, modebar=False)],
                style={
                    'width': '25%',
                }
            ),
            html.Div(
                children=[image.render(ids.IMAGE_ANALYSIS)],
                style={
                    'width': '50%',
                }
            ),
            html.Div(
                children=[],
                style={
                    'width': '25%',
                }
            )
        ],
        style={
            'display': 'flex',
            'flex-direction': 'row',
            'width': '100%',
            'gap': '5px',
        },
    )
