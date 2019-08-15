import numpy as np
import time
import json
import random
import plotly.io as pio
import plotly.graph_objects as go
from Container import Container


def getBoxPlotDef(start, dimensions, color):
    # 8 vertices of a cube
    x = [start["x"], start["x"], start["x"] + dimensions["width"], start["x"] + dimensions["width"], start["x"], start["x"], start["x"] + dimensions["width"], start["x"] + dimensions["width"]]
    y = [start["y"], start["y"] + dimensions["height"], start["y"] + dimensions["height"], start["y"], start["y"], start["y"] + dimensions["height"], start["y"] + dimensions["height"], start["y"]]
    z = [start["z"], start["z"], start["z"], start["z"], start["z"] + dimensions["length"], start["z"] + dimensions["length"], start["z"] + dimensions["length"], start["z"] + dimensions["length"]]

    boxDef = go.Mesh3d(
            x = x,
            y = y,
            z = z,
            color=color,
            colorbar_title='z',
            # i, j and k give the vertices of triangles
            i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
            j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
            k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
            showscale=True
    )
    return boxDef

def writeContainerDataToFile(containerData):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    filename = "files/Res-{0}".format(timestr)
    json.dump(containerData, open(filename, "w"))

def renderContainerDataFromFile(fileName, renderer="browser"):
    with open(fileName) as json_file:
        data = json.load(json_file)
        renderContainerData(data, renderer=renderer)

def renderContainerData(containerData, renderer="browser"):
    data = []

    pio.renderers.default = renderer

    cnt = 1
    for boxData in containerData["boxes"]:
        box = boxData["box"]
        location = boxData["location"]
        color = "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])

        location = {"z": location["z"] * containerData["spaceOptimizationFactor"],
                    "y": location["y"] * containerData["spaceOptimizationFactor"],
                    "x": location["x"] * containerData["spaceOptimizationFactor"]
         }

        data.append(getBoxPlotDef(location, box, color))
        cnt = cnt + 1

    fig = go.Figure(data=data)

    camera = dict(
        up=dict(x=0, y=1, z=0),
        center=dict(x=0, y=0, z=0),
        eye=dict(x=-2, y=1, z=-2)
    )

    fig['layout'].update(
        scene=dict(camera=camera),
        title="XY Plane"
    )

    fig.show()

def renderSampleContainer():
    CONTAINER_DIMENSIONS = {"length": 600, "width": 240, "height": 240}

    NUMBER_OF_BOXES = 10
    MIN_EDGE_SIZE = 20
    MAX_EDGE_SIZE = 60
    boxes, boxes_cbm = simulateBoxData(NUMBER_OF_BOXES, MIN_EDGE_SIZE, MAX_EDGE_SIZE, 10, True)

    container = Container(length=CONTAINER_DIMENSIONS["length"],
                          width=CONTAINER_DIMENSIONS["width"],
                          height=CONTAINER_DIMENSIONS["height"],
                          boxes=boxes, spaceOptimizationFactor=MIN_EDGE_SIZE)
    container.placeBoxesSequentially()
    data = container.getResultsJSON()
    renderContainerData(data)

def defaultConv(o):
    if isinstance(o, np.int64): return int(o)
    elif isinstance(o, np.float): return float(o)
    raise TypeError


def myround(x, base=5):
    return base * round(x/base)

def simulateBoxData(count, min_edge_size, max_edge_size, space_scaling_factor, save_data):
    """Create count number of boxes
        each of random size smaller than max_dims (array of length/width/height)
        """
    boxes = np.random.random_integers(low=min_edge_size, high=max_edge_size, size=(count, 3))
    boxesDictArray = []

    boxes_cbm = 0

    for box in boxes:
        length = myround(box[0], space_scaling_factor)
        height = myround(box[1], space_scaling_factor)
        width = myround(box[2], space_scaling_factor)

        boxDict = {"length": length, "height": height, "width": width}
        boxesDictArray.append(boxDict)
        boxes_cbm += boxDict["length"] * boxDict["width"] * boxDict["height"]

    boxes_cbm /= 1000000

    data = { "boxes": boxesDictArray, "boxesCBM" : boxes_cbm }
    timestr = time.strftime("%Y%m%d-%H%M%S")
    filename = "files/Exp-{0}".format(timestr)

    if save_data:
        json.dump(data, open(filename, "w"), default=defaultConv)

    return boxesDictArray, boxes_cbm


def loadBoxData(filename):
    with open("files/" + filename) as json_file:
        data = json.load(json_file)
        return data["boxes"], data["boxesCBM"]
