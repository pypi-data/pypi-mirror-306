import pandas as pd

from dash import Dash, html, dcc, no_update
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from enum import Enum, auto
from typing import Type

from . import ids, image
from ...cell import Cell

from copy import deepcopy


def create_enum_from_class(cls: Type) -> Enum:
    attributes = cls.__annotations__.keys()
    enum_dict = {attr: auto() for attr in attributes}
    return Enum(f"{cls.__name__}Enum", enum_dict)


CellEnum = create_enum_from_class(Cell)


def render(app: Dash) -> html.Div:
    @app.callback(
        [Output(ids.IMAGE_ANALYSIS, 'figure', allow_duplicate=True),
         Output(ids.IMAGE_COLORBAR, 'figure', allow_duplicate=True),],
        [Input(ids.BACKUP_SEGMENT, 'data'),
         Input(ids.DROPDOWN_ANALYSIS, 'value'),
         Input(ids.INPUT_PIXEL, 'value')],
        prevent_initial_call=True
    )
    def update_analysis(backup, dropdown, pixel):
        if not backup:
            raise PreventUpdate
        img = image.make()
        segment_array = image.decode(backup)
        labels = image.label_cells(segment_array[:, :, 0])
        cells = image.get_all_cells(labels)
        cells = image.remove_border_cells(labels, cells, pixel)
        analysis = image.get_image_by(dropdown, labels, cells)
        analysis = image.plot(img, analysis)
        colorbar = deepcopy(analysis)
        analysis.data[-1].update(showscale=False)  # type: ignore
        analysis.update_layout(plot_bgcolor='gray')
        colorbar.update_traces(opacity=0, hoverinfo='skip')
        colorbar.update_layout(coloraxis_colorbar=dict(len=1))
        return analysis, colorbar

    @app.callback(
        Output(ids.DOWNLOAD, 'data', allow_duplicate=True),
        Input(ids.BUTTON_DOWNLOADCSV, 'n_clicks'),
        [State(ids.BACKUP_SEGMENT, 'data'),
         State(ids.INPUT_PIXEL, 'value')],
        prevent_initial_call=True
    )
    def download_csv(_, backup, pixel):
        if not backup:
            raise PreventUpdate

        segment_array = image.decode(backup)
        labels = image.label_cells(segment_array[:, :, 0])
        cells = image.get_all_cells(labels)
        cells = image.remove_border_cells(labels, cells, pixel)
        df = pd.DataFrame([cell.__dict__ for cell in cells])
        return dcc.send_data_frame(df.to_csv, "rpegment.csv", index=False)

    return html.Div(
        children=[
            dcc.Input(
                className='dash-input',
                id=ids.INPUT_PIXEL,
                type='number',
                min=0,
                max=10,
                step=1,
                value=1,
                style={
                    'width': '5%',
                    'gap': '5px',
                }
            ),
            html.Div(
                children=[
                    dcc.Dropdown(
                        id=ids.DROPDOWN_ANALYSIS,
                        options=[
                            {"label": item.name, "value": item.name}
                            for item in CellEnum  # type: ignore
                        ],
                        value=CellEnum.Label.name,  # type: ignore
                        clearable=False,
                        style={
                            'width': '50%',
                        }
                    ),
                    html.Button(
                        className="dash-button",
                        id=ids.BUTTON_DOWNLOADCSV,
                        children='Download csv',
                    )
                ],
                style={
                    'display': 'flex',
                    'justifyContent': 'space-around',
                    'flex-direction': 'row',
                    'gap': '5px',
                    'align-items': 'center',
                    'width': '60%',
                }
            ),
        ],
        style={
            'display': 'flex',
            'justifyContent': 'space-around',
            'flex-direction': 'row',
            'gap': '5px',
            'align-items': 'center',
            'width': '100%',
        }
    )
