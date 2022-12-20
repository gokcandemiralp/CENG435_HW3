import sys
INF = sys.maxsize

class Edge:
    fromNode = None
    toNode = None
    Cost = INF

    def printEdge(self):
        print(f"{self.fromNode} -{self.toNode} | {self.Cost}")

class Node:
    nodeId = None
    edgesList = []

    def printNode(self):
        for edge in self.edgesList:
            edge.printEdge()


nodes = []
nodeId = sys.argv[1]
fd = open(f"{sys.argv[1]}.costs", "r")
lineCount = 0
nodeCount = 0
tempNode = Node()

tempNode.nodeID = int(nodeId)
lines = fd.readlines()


for line in lines:
    if(lineCount == 0):
        nodeCount = int(line)
        print(nodeCount)
    else:
        lineElements = line.split(' ')
        tempEdge = Edge()
        tempEdge.fromNode = int(nodeId)
        tempEdge.toNode = int(lineElements[0])
        tempEdge.Cost = int(lineElements[1])
        tempNode.edgesList.append(tempEdge)
    lineCount += 1
nodes.append(tempNode)
tempNode.printNode()
