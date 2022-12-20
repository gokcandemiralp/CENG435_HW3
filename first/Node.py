import sys

class Edge:
    fromNode = None
    toNode = None
    Cost = None

    def printEdge(self):
        print(f"{self.fromNode} -{self.toNode} | {self.Cost}")

class Node:
    nodeId = None
    edgesList = []

    def printNode(self):
        print(f"nodeId: {nodeId}:")
        for edge in self.edgesList:
            edge.printEdge()


def printNodes(nodes):
    for node in nodes:
        node.printNode()

nodes = []
for nodeId in sys.argv[1].splitlines():
    fd = open(f"{nodeId}.costs", "r")
    lineCount = 0
    tempNode = Node()

    tempNode.nodeID = int(nodeId)
    lines = fd.readlines()


    for line in lines:
        if(lineCount != 0):
            lineElements = line.split(' ')
            tempEdge = Edge()
            tempEdge.fromNode = int(nodeId)
            tempEdge.toNode = int(lineElements[0])
            tempEdge.Cost = int(lineElements[1])
            tempNode.edgesList.append(tempEdge)
        lineCount += 1
    nodes.append(tempNode)

printNodes(nodes)
