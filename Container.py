from enum import Enum
import numpy as np
import math
import copy
import random

UnitsOfMeasure = Enum('Inch', 'Centimeter')

class Container:

    boxes = []
    addedBoxes = []
    addedBoxLocations = []
    remainingBoxes = []
    spaceOptimizationFactor = 1
    length = 0
    width = 0
    height = 0
    totalVolume = 0.0

    nextEmptySpace = {"z": 0, "x": 0, "y": 0}
    scaledDimensions = {"length": 0, "width": 0, "height": 0}
    isFilled = False

    minHeightAtRow = 0
    minLengthAtRow = 0

    def __init__(self, length, width, height, boxes, spaceOptimizationFactor = 1, useDeepSearch= False, unitsOfMeasure = UnitsOfMeasure.Centimeter):

        self.boxes = boxes
        self.spaceOptimizationFactor = spaceOptimizationFactor
        self.remainingBoxes = copy.deepcopy(boxes)
        self.addedBoxes = []
        self.addedBoxLocations = []

        self.nextEmptySpace = {"z": 0, "x": 0, "y": 0}
        self.nextNeighborSpaces = {"right": None, "top": None, "front": None}

        self.minHeightAtRow = 0
        self.minLengthAtRow = 0
        self.useDeepSearch = useDeepSearch

        self.totalVolume = 0.0
        self.unitsOfMeasure = unitsOfMeasure

        self.isFilled = False
        self.length = length
        self.height = height
        self.width = width

        self.scaledDimensions["length"] = math.floor(length / spaceOptimizationFactor)
        self.scaledDimensions["width"] = math.floor(width / spaceOptimizationFactor)
        self.scaledDimensions["height"] = math.floor(height / spaceOptimizationFactor)

        self.dimensions = np.zeros((self.scaledDimensions["length"],
                                    self.scaledDimensions["height"],
                                    self.scaledDimensions["width"]),
                                    dtype=bool)

    def placeBoxesSequentially(self):
        success = True
        for box in self.boxes:
            res = self.addBox(box)
            success = success and res

        if success:
            print("ALL FIT!")
        else:
            print("Out of space for all, could at most add %s boxes" % len(self.addedBoxes))

        return success

    def placeBoxesRandomly(self):
        success = True
        while len(self.remainingBoxes) > 0 and success:
            box = random.choice(self.remainingBoxes)
            res = self.addBox(box)
            success = success and res

        if success:
            print("ALL FIT!")
        else:
            print("Out of space for all, could at most add %s boxes" % len(self.addedBoxes))

        return success

    def getContainerCBM(self):
        container_cbm = self.length * self.width * self.height

        if self.unitsOfMeasure == UnitsOfMeasure.Centimeter:
            return container_cbm / 1000000
        elif self.unitsOfMeasure == UnitsOfMeasure.Inch:
            return container_cbm * (2.54 * 2.54 * 2.54) / 1000000

    def getCurrentCBM(self):
        if self.unitsOfMeasure == UnitsOfMeasure.Centimeter:
            return self.totalVolume / 1000000
        elif self.unitsOfMeasure == UnitsOfMeasure.Inch:
            return self.totalVolume * (2.54 * 2.54 * 2.54) / 1000000

    def getRemainingBoxes(self):
        return self.remainingBoxes

    def addBox(self, box):

        length = self.scaledDimensions["length"]
        height = self.scaledDimensions["height"]
        width = self.scaledDimensions["width"]

        blockLength = math.ceil(box["length"] / self.spaceOptimizationFactor)
        blockHeight = math.ceil(box["height"] / self.spaceOptimizationFactor)
        blockWidth = math.ceil(box["width"] / self.spaceOptimizationFactor)

    #    print("Next neighbors is %s" % (self.nextNeighborSpaces))
     #   print("Next Empty Space is %s" % (self.nextEmptySpace))

        isAdded = False

        for i in range(self.nextEmptySpace["z"], self.scaledDimensions["length"]):
            for j in range(self.nextEmptySpace["y"], self.scaledDimensions["height"]):
                for k in range(self.nextEmptySpace["x"], self.scaledDimensions["width"]):

                    doesFit = True
                    # Determine whether it fits to current empty row

                    if i + blockLength > length or j + blockHeight > height or k + blockWidth > width:
                        doesFit = False
                    else:
                        for p in range(1, blockLength+1):
                            for r in range(1, blockHeight+1):
                                for s in range(1, blockWidth+1):
                                    if self.dimensions[i + p - 1, j + r - 1, k + s - 1]:
                                        doesFit = False

                    # If fits, add the box, block the space, move to right (in X/width direction)
                    if doesFit:
                        #print("Found location @ Z:%s Y:%s X:%s" % (i, j, k))
                        isAdded = True
                        self.addedBoxes.append(box)
                        self.remainingBoxes.remove(box)
                        addedLocation = {"z": i, "y": j, "x": k}
                        self.addedBoxLocations.append(addedLocation)
                        self.totalVolume += box["length"] * box["height"] * box["width"]

                        if self.minHeightAtRow == 0:
                            self.minHeightAtRow = blockHeight + j
                        else:
                            self.minHeightAtRow = min(self.minHeightAtRow, blockHeight + j)

                        if self.minLengthAtRow == 0:
                            self.minLengthAtRow = blockLength + i
                        else:
                            self.minLengthAtRow = min(self.minLengthAtRow, blockLength + i)

                        for p in range(1, blockLength+1):
                            for r in range(1, blockHeight+1):
                                for s in range(1, blockWidth+1):
                                    self.dimensions[i + p - 1, j + r - 1, k + s - 1] = True

                        self.mapNeighborSpacesAfterBox(blockLength=blockLength, blockHeight=blockHeight, blockWidth=blockWidth,
                                                       currentLength=i, currentHeight=j, currentWidth=k)
                        self.nextEmptySpace = self.nextNeighborSpaces["right"]
                        self.nextNeighborSpaces["right"] = None
                        #print("Moving right to %s" % self.nextEmptySpace)

                        #print("-------------------")

                        return True

                if not isAdded:
                    if self.nextNeighborSpaces["top"]:
                        # go up row
                        self.nextEmptySpace = self.nextNeighborSpaces["top"]
                        self.nextNeighborSpaces["top"] = None
                        #print("Going up row to %s" % self.nextEmptySpace)
                        return self.addBox(box)

            if not isAdded:
                if self.nextNeighborSpaces["front"]:
                    # come forward one row
                    self.nextEmptySpace = self.nextNeighborSpaces["front"]
                    self.minHeightAtRow = 0
                    self.nextNeighborSpaces["front"] = None
                    #print("Coming forward row to %s" % self.nextEmptySpace)
                    return self.addBox(box)

        self.isFilled = not isAdded
        return isAdded

    def mapNeighborSpacesAfterBox(self, blockLength, blockWidth, blockHeight, currentLength, currentWidth, currentHeight):

        if currentWidth + blockWidth <= self.scaledDimensions["width"]:
            space = self.nextEmptySpace.copy()
            # location of one row right
            space["x"] = currentWidth + blockWidth
            self.nextNeighborSpaces["right"] = space

        if currentHeight + blockHeight <= self.scaledDimensions["height"]:
            space = self.nextEmptySpace.copy()
            # location of one row up
            space["x"] = 0
            # Y location of this box ending
            space["y"] = space["y"] + blockHeight

            if self.useDeepSearch:
                # Y location smallest in the current row available
                space["y"] = min(space["y"], self.minHeightAtRow)

            self.nextNeighborSpaces["top"] = space

        if currentLength + blockLength <= self.scaledDimensions["length"]:
            space = self.nextEmptySpace.copy()
            # location of one row forward
            space["x"] = 0
            space["y"] = 0
            # Z location of this box ending
            space["z"] = space["z"] + blockLength

            if self.useDeepSearch:
                # Z location smallest in the current row available
                space["z"] = min(space["z"], self.minLengthAtRow)

            self.nextNeighborSpaces["front"] = space

    def getResultsJSON(self):
        cnt = 1
        outBoxes = []

        for box in self.addedBoxes:
            loc = self.addedBoxLocations[cnt - 1]
            cnt += 1
            outBoxes.append({
                "box": box,
                "location": loc
            })

        data = {
            "boxes" : outBoxes,
            "cbm": self.getCurrentCBM(),
            "containerCBM" : self.getContainerCBM(),
            "dimensions": {
                "length": self.length,
                "width": self.width,
                "height": self.height
            },
            "scaledDimensions" : self.scaledDimensions,
            "spaceOptimizationFactor" : self.spaceOptimizationFactor,
            "usedDeepSearch": self.useDeepSearch
        }

        return data
