import numpy as np
import copy
import random
import time

def defaultContainerMCTSPolicy(container):
    cont = True
    projectedContainer = copy.deepcopy(container)
    while cont:
        if len(projectedContainer.getRemainingBoxes()) > 0:
            box = projectedContainer.getRemainingBoxes()[0]
            cont = projectedContainer.addBox(box)
        else:
            cont = False
    return projectedContainer

class ContainerMCTNode():
    def __init__(self, container, parent):
        self.container = container
        self.projectedContainer = container
        self.isLeaf = container.isFilled
        self.isFullyExpanded = self.isLeaf
        self.parent = parent
        self.visits = 0
        self.children = {}
        self.text = ""
        self.totalCBM = 0
        self.nodeCBM = 0


class ContainerMCTS():
    def __init__(self, container, maxIterations=None, explorationConstant=0, policy=defaultContainerMCTSPolicy):
        self.maxIterations = maxIterations
        self.explorationConstant = explorationConstant
        self.policy = policy
        self.container = container

    def fill(self):
        cnt = copy.deepcopy(self.container)
        self.root = ContainerMCTNode(cnt, None)
        self.root.text = "Root"

        for i in range(self.maxIterations):
            if not self.runIteration(i):
                print("All options tried.")
                break

        bestNode = self.getBestLeaf(self.root, explorationConstant=0)
        return bestNode

    def runIteration(self, ind):
        start = time.time()
        node = self.selectMCTNode(self.root)
        if node is not None:
            projectedContainer = self.policy(node.container)
            projectedCBM = projectedContainer.getCurrentCBM()
            node.projectedContainer = projectedContainer
            end = time.time()
            print("Ran iteration # %s  TTL:%.4f CBM (max:%.4f) in %.2f sec" % (ind, projectedCBM, self.root.totalCBM, (end-start)))
            self.registerTotalCBM(node, projectedCBM)
            return True
        else:
            return False


    def selectMCTNode(self, node):
        if not node.isLeaf:
            if node.isFullyExpanded:
                bestNode = self.getBestLeaf(node, self.explorationConstant)
                #print("Best is %s" % (bestNode.text))
                return self.selectMCTNode(bestNode)
            else:
                #print("Expanding %s " % node.text)
                return self.expand(node)
        return node

    def expand(self, node):
        boxes = node.container.getRemainingBoxes()
        ind = random.randint(0, len(boxes) - 1)
        box = boxes[ind]

        str_format = "{}xL:{} H:{} W:{}"
        box_str = str_format.format(ind, box["length"], box["height"], box["width"])

        while box_str in node.children:
            ind = random.randint(0, len(boxes)-1)
            box = boxes[ind]
            box_str = str_format.format(ind, box["length"], box["height"], box["width"])

        newContainer = copy.deepcopy(node.container)
        result = newContainer.addBox(box)
        if result:
            newNode = ContainerMCTNode(newContainer, node)
            newNode.text = box_str
            newNode.boxConfig = box
            node.children[box_str] = newNode
            #print("ADDED %s to %s, TTL:%s TTL CBM:%s" %  (box_str, node.text, len(newNode.container.addedBoxes), newNode.container.getCurrentCBM()))

            if len(boxes) == len(node.children):
                node.isFullyExpanded = True
                #print("********** %s FULLY EXPANDED" % (node.text))
            return newNode
        else:
            print("couldn't add %s" % box)
            node.isLeaf = True

    def getBestLeaf(self, node, explorationConstant):
        bestTotalCBM = float(0)
        bestNextLeaf = None

        for child in node.children.values():
            # nodeCBM = child.totalCBM / child.visits + explorationConstant * math.sqrt(2 * math.log(node.visits) / child.visits)
            nodeCBM = child.totalCBM
            if nodeCBM >= bestTotalCBM:
                bestTotalCBM = nodeCBM
                bestNextLeaf = child

        if explorationConstant > 0:
            mode = np.random.uniform(0, 1)
            if mode < explorationConstant and len(node.children.values()) > 0:
                # exploration
                return random.choice(list(node.children.values()))
            else:
                # exploitation
                return bestNextLeaf
        else:
            return bestNextLeaf

    def registerTotalCBM(self, node, totalCBM):
        while node is not None:
            node.visits += 1
            node.totalCBM = max(node.totalCBM, totalCBM)
            node = node.parent
