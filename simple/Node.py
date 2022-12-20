import sys
import socket
INF = sys.maxsize

class Edge:
    toNode = None
    cost = INF

    def printEdge(self):
        print(f" -{self.toNode} | {self.cost}")

class Node:
    nodeId = None
    edgesList = []

    def __init__(self,nodeId):
        self.nodeId = nodeId

    def updateEdge(self,u_nodeId,u_cost):
        for edge in self.edgesList:
            if(edge.toNode == u_nodeId):
                edge.cost = u_cost

    def printNode(self):
        for edge in self.edgesList:
            print(f"{self.nodeId}", end='')
            edge.printEdge()



read_nodeId = sys.argv[1]
fd = open(f"{sys.argv[1]}.costs", "r")
lineCount = 0
nodeCount = 0

tempNode = Node(int(read_nodeId))

PORT = int(read_nodeId)
HOST = "127.0.0.1"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)

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
        tempNode.updateEdge(int(lineElements[0]),int(lineElements[1]))
    lineCount += 1

tempNode.printNode()
