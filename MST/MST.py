import sys
import heapq
import tsp_utils as utils
import numpy as np
# implementation of tree borrowed from:
# https://stackoverflow.com/questions/2358045/how-can-i-implement-a-tree-in-python-are-there-any-built-in-data-structures-in
class Tree:
        
    def __init__(self, id = 0, children=None):
        self.id = id
        self.children = []
        self.childCount = 0
        
        if children is not None:
            for child in children:
                self.add_child(child)
        
    def __repr__(self):
        return self.name
        
    def add_child(self, node):
        assert isinstance(node,Tree)
        self.children.append(node)
        self.childCount += 1
                                
# Builds a Minimum Spanning Tree using Prim's algorithm
# Accepts: pre-generated Map of cities
# Returns: set of tuples that hold (fromCity, toCity) 
#   representing the from and to connecting nodes in the tree
def primMST(map):
        
    #get distances(weights)
    dists = map.distMatrix
    cities = map.cities
    full = len(cities)      
    print full
    
    # holds the mst as a tuple of (fromNode, toNode)
    #mstPath = []

    # holds nodes in the order they are added
    preWalk = []
    
    #get smallest distance
    tmp = np.array(dists)
    start = np.amin(tmp)
    
    #select from city for this distance and set it visited
    # then append it to the preWalk
    cities[start[1]].visited = True
    preWalk.append(start[1])
    
    #initialize options to all distances connecting to our start
    # vertex so we pick the smallest distance from that vertex
    options = dists[start[1]].tolist()
    heapq.heapify(options)

    # while we have not added all vertices to the tree
    while len(preWalk) < full:
        # pop the lowest distance
        selected = heapq.heappop(options)
        fromCity = cities[selected[1]]
        toCity = cities[selected[2]]

        # check if we have already visted the 'to' city
        if toCity.visited == True:
            continue # pop next city
        else:           
            # mark city visited, append to MST and add all distances from the toCity vertex to our options
            toCity.visited = True 
            #mstPath.append((fromCity.id,toCity.id))
            preWalk.append(toCity.id)
            options.extend(dists[toCity.id])    
            
            # reprioritize the queue by distance
            heapq.heapify(options)                      
    preWalk.append(preWalk[0])
    return preWalk

def twoOptSwap(route,i,j):
    new_route = route[:i]
    tmp = list(reversed(route[i:j+1]))
    new_route.extend(tmp)
    new_route.extend(route[j+1:])
    return new_route


def improve(route,map,method):

    currentBest = calcLength(route,map)
    prevBest = currentBest + 1

    while currentBest < prevBest:
        prevBest = currentBest
        for i in range(1,len(route)-2):
            for j in range(i+1,len(route)-1):
                
                curSum = map.dist(route[i-1],route[i]) + map.dist(route[j],route[j+1])
                newSum = map.dist(route[i-1],route[j]) + map.dist(route[i],route[j+1])

                if newSum < curSum:
                    route = twoOptSwap(route,i,j)
                    new_dist = calcLength(route,map)
                    currentBest = new_dist
                    break
            else:
                continue
            break
    return route

    
def twoOptPlus(route,map):
    cities = map.cities
    dists = map.distMatrix

    bestChange = -10

    while bestChange < 0:
        bestChange = 0
        for i in range(1,len(route)-2):
            for j in range(i+1, len(route)-1):
               curSum = map.dist(route[i-1],route[i]) + map.dist(route[j],route[j+1])
               newSum = map.dist(route[i-1],route[j]) + map.dist(route[i],route[j+1])

               testChange = newSum - curSum

               if bestChange > testChange:
                   bestChange = testChange
                   besti = i
                   bestj = j

        route = twoOptSwap(route,besti,bestj)
    
    return route


def buildNeighbors(map):
    cities = map.cities
    dists = map.distMatrix

    neighbors = np.array([[None for x in range(5)] for y in cities])
    
    for city in cities:
        tmp = heapq.nsmallest(5,dists[city.id])
        for i in range(len(tmp)):
            tmp[i] = tmp[i][2]
        neighbors[city.id] = tmp

    return neighbors


def calcLength(tour, map):

    length = 0
    
    for i in range(len(tour)-1):
        j = i+1
        c1 = tour[i]
        c2 = tour[j]
        length += map.dist(c1,c2)
    return length

def setTour(route, length, fileName):
    outFile = open(fileName,"w")

    outFile.write(str(length)+'\n')
    for i in range(len(route)-1):
        outFile.write(str(route[i])+'\n')



inFilename = sys.argv[1]
inFile = open(inFilename,"r")

outFilename = inFilename + '.tour'

map = utils.Map(inFile)
route = primMST(map)
print calcLength(route,map)
print 'Normal 2-opt'
optroute = improve(route,map,1)
print calcLength(optroute,map)
print 'Faster 2-opt'
fastroute = twoOptPlus(route,map)
print calcLength(fastroute,map)
# also creates distance matrix


# length = calcLength(route,map.distMatrix)
# setTour(route, length, outFilename)

#initialize visited vertices
