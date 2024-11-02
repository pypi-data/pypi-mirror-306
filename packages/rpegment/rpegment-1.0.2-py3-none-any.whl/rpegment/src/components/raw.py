from dash import Dash, html, dcc, no_update
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State

from . import ids, image


def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.IMAGE_RAW, 'figure'),
        Input(ids.UPLOAD_RAW, 'contents'),
        prevent_initial_call=True
    )
    def update_raw(contents):
        if contents is None:
            raise PreventUpdate
        img = image.make()
        raw = image.decode(contents)
        img = image.plot(img, raw)
        return img

    @app.callback(
        [Output(ids.BACKUP_SEGMENT, 'data'),
         Output(ids.BUTTON_SEGMENT, 'children')],
        Input(ids.BUTTON_SEGMENT, 'n_clicks'),
        [State(ids.IMAGE_RAW, 'figure'),
         State(ids.CHECKLIST_OVERLAP, 'value')],
        prevent_initial_call=True
    )
    def segment(_, raw, overlap):
        raw_data = raw['data']
        if not raw_data:
            raise PreventUpdate

        image_list = raw_data[0]['z']
        image_array = image.imglist2array(image_list)
        segment_array = image.segment(image_array)
        backup = image.encode(segment_array)
        if overlap:
            segment_array = image.overlap(image_array, segment_array)
        return backup, no_update

    return html.Div(
        children=[
            html.Div(
                children=[
                    dcc.Upload(
                        className='drag-drop',
                        children=html.Div(
                            'Drag and Drop/Select Raw Image'
                        ),
                        id=ids.UPLOAD_RAW,
                        multiple=False
                    ),
                    dcc.Loading(
                        id=ids.LOADING_SEGMENT,
                        type='default',
                        children=[
                            html.Button(
                                id=ids.BUTTON_SEGMENT,
                                children='Segment',
                                className="dash-button"
                            )
                        ],
                    )
                ],
                style={
                    'display': 'flex',
                    'flex-direction': 'row',
                    'align-items': 'center',
                    'justifyContent': 'space-around',
                }
            ),
            html.Div(
                children=[image.render(ids.IMAGE_RAW)],
                style={
                    'width': '100%',
                }
            )
        ],
        style={
            'display': 'flex',
            'flex-direction': 'column',
            'justifyContent': 'center',
            'width': '100%',
        },
    )
