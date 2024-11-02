import cv2
import base64
import feret
import warnings


import numpy as np
import numpy.typing as npt
import plotly.graph_objects as go

from dash import dcc
from cellpose import models
from skimage import measure, morphology

from ...cell import Cell

warnings.simplefilter("ignore", category=FutureWarning)


def render(id: str, modebar: bool = True) -> dcc.Graph:
    config = {
        'toImageButtonOptions': {
            'format': 'png',
            'scale': 5
        },
        'displayModeBar': modebar
    }
    return dcc.Graph(
        id=id,
        figure=make(),
        config=config,
    )


def plot(
    img: go.Figure,
    image_array: npt.NDArray[np.uint8 | np.int_ | np.float64]
) -> go.Figure:
    if len(image_array.shape) == 3:
        img.add_trace(go.Image(z=image_array))
    else:
        height, width = image_array.shape
        img.add_trace(
            go.Heatmap(
                z=np.flipud(image_array),
                colorscale='Rainbow',
                y=list(range(height)),
                x=list(range(width)),
            )
        )

        img.update_xaxes(constrain='domain')
        img.update_yaxes(
            scaleanchor='x',
            scaleratio=1.0,
            constrain='domain'
        )

        img.update_xaxes(range=[-0.5, width-0.5])
        img.update_yaxes(range=[-0.5, height-0.5])
    return img


def make() -> go.Figure:
    img = go.Figure()
    img.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=5, r=5, t=5, b=5),
        newshape_line_color='blue',
        newshape_line_width=2,
        newshape_opacity=0.7,
        modebar_add=['drawclosedpath', 'eraseshape']
    )
    return img


def _decode(data: str) -> bytes:
    _, encoded = data.split(",", 1)
    return base64.b64decode(encoded)


def decode(contents: str) -> npt.NDArray[np.uint8]:
    image_data = _decode(contents)
    np_arr = np.frombuffer(image_data, np.uint8)
    image_array = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    image_rgb = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
    return image_rgb.astype(np.uint8)


def encode(image: npt.NDArray[np.uint8]) -> str:
    _, buffer = cv2.imencode('.png', image)
    encoded_image = base64.b64encode(buffer.tobytes()).decode('utf-8')
    return f"data:image/png;base64,{encoded_image}"


def imglist2array(image_list: list[list[int]]) -> npt.NDArray[np.uint8]:
    image_array = np.array(image_list, dtype=np.uint8)
    rgb = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
    return rgb.astype(np.uint8)


def segment(image: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint8]:
    model = models.Cellpose(model_type='cyto3')
    ele = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img = [gray]
    masks, flows, styles, diams = model.eval(
        img, diameter=None, channels=[[0, 0]])  # type: ignore
    img = masks[0]

    maxId = np.amax(img) + 1
    res = np.zeros_like(img, dtype=int)
    for i in range(1, maxId):
        tmp = (img == i) * 255
        res |= cv2.erode(tmp.astype(np.uint8), ele, iterations=1)
        res[res == 255] = i

    res = (res == 0)
    res = morphology.skeletonize(res)
    res = (res * 255).astype(np.uint8)
    res = cv2.cvtColor(res, cv2.COLOR_GRAY2RGB).astype(np.uint8)
    return res


def overlap(
    image: npt.NDArray[np.uint8],
    segment: npt.NDArray[np.uint8]
) -> npt.NDArray[np.uint8]:
    image[:, :, 2] = 0
    image[:, :, 1] = segment[:, :, 1]
    red = cv2.equalizeHist(image[:, :, 0])
    image[:, :, 0] = cv2.medianBlur(red, 5)

    return image


def modify_segmentation(
    segmentation: npt.NDArray[np.uint8],
    shape_path: str
) -> npt.NDArray[np.uint8]:
    parsed_path = parse_path(shape_path)
    path = np.array(parsed_path, dtype=np.int32)
    cv2.fillPoly(segmentation, [path], color=(0, 0, 0))  # type: ignore
    cv2.polylines(segmentation, [path], isClosed=True,
                  color=(255, 255, 255), thickness=1)  # type: ignore
    return segmentation


def parse_path(shape_path: str) -> list[list[int]]:
    shape_path = shape_path.replace('M', 'L').replace('Z', 'L')
    path_parts = shape_path.split('L')

    coordinates = []
    for part in path_parts:
        if part.strip():
            coord_str = part.strip()
            coord = [int(round(float(x))) for x in coord_str.split(',')]
            coordinates.append(coord)

    return coordinates


def label_cells(image_array: npt.NDArray[np.uint8]) -> npt.NDArray[np.int_]:
    image_inv = cv2.bitwise_not(image_array)
    label = measure.label(image_inv, background=0, connectivity=1)

    if not isinstance(label, np.ndarray):
        raise TypeError("Expected a numpy array")

    label = morphology.remove_small_objects(label, min_size=10)

    return label.astype(np.int_)


def get_all_cells(labeled_image: npt.NDArray[np.int_]) -> list[Cell]:
    props = measure.regionprops(labeled_image)
    neighbor_map = get_neighbors(labeled_image)
    cells = [prop2cell(prop, neighbor_map)
             for prop in props if prop.label != 0]
    return cells


def get_neighbors(
    labels: npt.NDArray[np.int_],
    border: int = 1
) -> npt.NDArray[np.int_]:
    properties = measure.regionprops(labels)
    properties = [prop for prop in properties if prop.label != 0]

    num_labels = np.max(labels)
    adjacency_matrix = np.zeros((num_labels + 1, num_labels + 1), dtype=bool)

    for prop in properties:
        minr, minc, maxr, maxc = prop.bbox
        region_slice = labels[minr-border:maxr+border,
                              minc-border:maxc+border]
        unique_labels = np.unique(region_slice)
        for label in unique_labels:
            if label != prop.label and label != 0:
                adjacency_matrix[prop.label, label] = True
                adjacency_matrix[label, prop.label] = True

    neighbor_counts = np.sum(adjacency_matrix, axis=0)

    neighbor_map = np.zeros_like(labels)
    for prop in properties:
        neighbor_map[labels == prop.label] = neighbor_counts[prop.label]

    return neighbor_map


def prop2cell(prop, neighbor_map: npt.NDArray[np.int_]) -> Cell:
    cell = Cell()
    cell.Label = prop.label
    x = prop.centroid[1]
    y = neighbor_map.shape[0] - prop.centroid[0]
    cell.Y, cell.X = y, x
    cell.Area = prop.area
    cell.Peri = prop.perimeter

    bbox = prop.bbox
    cell.Width, cell.Height = bbox[3] - bbox[1], bbox[2] - bbox[0]
    cell.Solidity = prop.solidity
    cell.EllipMaj = prop.major_axis_length

    min_feret, max_feret = feret.min(prop.image), feret.max(prop.image)
    cell.Feret = float(max_feret)
    cell.MinFeret = float(min_feret)

    if prop.coords.size > 0:
        coord = prop.coords[0]
        cell.Neighbors = int(neighbor_map[coord[0], coord[1]])

    cell.get_output()
    return cell


def get_image_by(
    property: str,
    labels: npt.NDArray[np.int_],
    cells: list[Cell]
) -> npt.NDArray[np.float64]:
    image = np.full_like(labels, np.nan, dtype=np.float64)
    for cell in cells:
        value = getattr(cell, property)
        if not np.isnan(value):
            image[labels == cell.Label] = value
    return image


def remove_border_cells(
    labels: npt.NDArray[np.int_],
    cells: list[Cell],
    pixel: int,
) -> list[Cell]:
    border_labels = set()
    for i in range(pixel):
        border_labels.update(np.unique(np.concatenate((
            labels[i, :],
            labels[-(i+1), :],
            labels[:, i],
            labels[:, -(i+1)]
        ))))

    cleaned_cells = [cell for cell in cells if cell.Label not in border_labels]

    return cleaned_cells
