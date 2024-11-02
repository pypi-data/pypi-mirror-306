from dash import Dash, html, dcc, no_update
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State

from . import ids, image


def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.BACKUP_SEGMENT, 'data', allow_duplicate=True),
        Input(ids.UPLOAD_SEGMENT, 'contents'),
        prevent_initial_call=True
    )
    def update_backup(contents):
        if contents is None:
            raise PreventUpdate
        segment_array = image.decode(contents)
        backup = image.encode(segment_array)
        return backup

    @app.callback(
        Output(ids.IMAGE_SEGMENT, 'figure', allow_duplicate=True),
        Input(ids.BACKUP_SEGMENT, 'data'),
        [State(ids.IMAGE_RAW, 'figure'),
         State(ids.CHECKLIST_OVERLAP, 'value')],
        prevent_initial_call=True
    )
    def update_segment(backup, raw, overlap):
        img = image.make()
        segment_array = image.decode(backup)
        if overlap:
            image_data = raw['data']
            if image_data:
                image_list = image_data[0]['z']
                image_array = image.imglist2array(image_list)
                segment_array = image.overlap(image_array, segment_array)

        img = image.plot(img, segment_array)
        return img

    @app.callback(
        Output(ids.DOWNLOAD, 'data'),
        Input(ids.BUTTON_DOWNLOAD, 'n_clicks'),
        State(ids.BACKUP_SEGMENT, 'data'),
        prevent_initial_call=True
    )
    def download_segment(_, backup):
        if not backup:
            raise PreventUpdate

        image_bytes = image._decode(backup)
        return dcc.send_bytes(
            lambda x: x.write(image_bytes),
            filename="rpegment.png",
            type="image/png"
        )

    @app.callback(
        Output(ids.IMAGE_SEGMENT, 'figure', allow_duplicate=True),
        Input(ids.CHECKLIST_OVERLAP, 'value'),
        [State(ids.IMAGE_RAW, 'figure'),
         State(ids.IMAGE_SEGMENT, 'figure'),
         State(ids.BACKUP_SEGMENT, 'data')],
        prevent_initial_call=True
    )
    def draw_overlap(overlap, raw, segment, backup):
        if not segment['data'] or not raw['data']:
            raise PreventUpdate

        image_list = raw['data'][0]['z']
        image_array = image.imglist2array(image_list)
        if overlap:
            segment_list = segment['data'][0]['z']
            segment_array = image.imglist2array(segment_list)
            segment_array = image.overlap(image_array, segment_array)
        else:
            segment_array = image.decode(backup)

        segment['data'][0]['z'] = segment_array.tolist()
        return segment

    @app.callback(
        [Output(ids.BACKUP_SEGMENT, 'data', allow_duplicate=True),
         Output(ids.IMAGE_SEGMENT, 'clickData')],
        Input(ids.IMAGE_SEGMENT, 'clickData'),
        [State(ids.BACKUP_SEGMENT, 'data'),
         State(ids.IMAGE_SEGMENT, 'figure')],
        prevent_initial_call=True
    )
    def handle_click(_, backup, segment):
        shapes = segment['layout']['shapes']
        if not shapes:
            raise PreventUpdate
        segment_array = image.decode(backup)
        for shape in shapes:
            path = shape['path']
            segment_array = image.modify_segmentation(segment_array, path)
        segment['layout']['shapes'] = []
        return image.encode(segment_array), None

    return html.Div(
        children=[
            dcc.Store(id=ids.BACKUP_SEGMENT),
            html.Div(
                children=[
                    dcc.Upload(
                        className='drag-drop',
                        children=html.Div(
                            'Drag and Drop/Select Segmentation'
                        ),
                        id=ids.UPLOAD_SEGMENT,
                        multiple=False
                    ),
                    dcc.Loading(
                        id=ids.LOADING_DOWNLOAD,
                        type='default',
                        children=[
                            dcc.Download(id=ids.DOWNLOAD),
                            html.Button(
                                id=ids.BUTTON_DOWNLOAD,
                                children='Download',
                                className="dash-button"
                            )
                        ],
                    ),
                    dcc.Checklist(
                        id=ids.CHECKLIST_OVERLAP,
                        options=[
                            {'label': ' Overlap', 'value': 'overlap'},
                        ],
                        value=[]
                    ),
                ],
                style={
                    'display': 'flex',
                    'flex-direction': 'row',
                    'align-items': 'center',
                    'justifyContent': 'space-around',
                }
            ),
            html.Div(
                children=[image.render(ids.IMAGE_SEGMENT)],
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
