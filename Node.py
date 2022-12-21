import sys
import socket
import threading
INF = sys.maxsize
HOST = "127.0.0.1"

class Edge:
    toNode = None
    cost = INF
    isNeighbor = False

    def printEdge(self):
        print(f" -{self.toNode} | {self.cost}")
    def stringEdge(self):
        return str(self.toNode)+","+str(self.cost)

class Node:
    nodeId = None
    edgesList = []

    def __init__(self,nodeId):
        self.nodeId = nodeId
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((HOST,nodeId))
        self.s.listen()
        self.s.settimeout(5) 

    def getEdgeCost(self,u_nodeId):
        for edge in self.edgesList:
            if(edge.toNode == u_nodeId):
                return edge.cost

    def updateEdge(self,u_nodeId,u_cost):
        for edge in self.edgesList:
            if(edge.toNode == u_nodeId):
                edge.cost = u_cost

    def makeNeighbor(self,u_nodeId):
        for edge in self.edgesList:
            if(edge.toNode == u_nodeId):
                edge.isNeighbor = True

    def printNode(self):
        for edge in self.edgesList:
            print(f"{self.nodeId}", end='')
            edge.printEdge()

    def stringNode(self):
        ans_string = ""
        for edge in self.edgesList:
            ans_string += str(self.nodeId) + "," + edge.stringEdge() + "|"
        return ans_string

#--------------Global Variables--------------

read_nodeId = sys.argv[1]
fd = open(f"{sys.argv[1]}.costs", "r")
lineCount = 0
nodeCount = 0
tempNode = Node(int(read_nodeId))

#--------------------------------------------

def update(nodeString):
    splitedNodeString = nodeString.split('|')
    isUpdated = False

    for i in range(nodeCount):
        edgeString = splitedNodeString[i].split(',')

        interNode = int(edgeString[0])
        targetNode = int(edgeString[1])
        targetCost = int(edgeString[2])
        newCost = targetCost+tempNode.getEdgeCost(interNode)

        if(tempNode.getEdgeCost(targetNode) > newCost):
            tempNode.updateEdge(targetNode,newCost)
            isUpdated = True
    return isUpdated

def transmit_distance_vector():
    for edge in tempNode.edgesList:
        if(edge.isNeighbor):
            destination = edge.toNode
            edge_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                edge_s.connect((HOST, destination))
            except ConnectionRefusedError:
                continue

            edge_s.sendall(bytes(str(tempNode.stringNode()), 'utf-8'))
            edge_s.close()

def receive_distance_vector():
    tempNode.s.settimeout(5)
    while True:
        try:
            conn, addr = tempNode.s.accept()
            data = conn.recv(2048).decode('utf-8')
            if(update(data)):
                transmit_distance_vector()
                tempNode.s.settimeout(5)
        except socket.timeout:
            tempNode.printNode()
            tempNode.s.close()
            break
    

lines = fd.readlines()
for line in lines:
    if(lineCount == 0):
        nodeCount = int(line)
        for i in range(nodeCount):
            tempEdge = Edge()
            tempEdge.toNode = 3000+i
            if(3000+i == tempNode.nodeId):
                tempEdge.cost = 0
            tempNode.edgesList.append(tempEdge)
    else:
        lineElements = line.split(' ')
        tempEdge = Edge()
        destination = int(lineElements[0])
        distance = int(lineElements[1])
        tempNode.updateEdge(destination,distance)
        tempNode.makeNeighbor(destination)
    lineCount += 1

transmit_distance_vector()
receive_distance_vector()
