# Val Chapple
# Cody Dhein
# Date: Nov 26, 2017

import sys
import tsp_utils as utils
import numpy as np
import math
import timeit
import fibonacci_heap_mod as fib
import random as rand
# MST Class
#
# Based on Prim's Algorithm


## Initialize with an instance of Map class
class MST:
    def __init__(self, cityMap):
        if cityMap.__class__.__name__ != "Map":
            print("invalid city")
            return
        else:
            self.cityMap = cityMap
            self.route = []
            self.distance = float('inf')
            self.cityCount = len(self.cityMap.cities)

    # reset visited flags for future builds
    def resetVisited(self):
        for el in self.cityMap.cities:
            el.visited = False

    # Builds a Minimum Spanning Tree and constructs a route using Prim's algorithm
    # Returns: Sets self.tree equal to set of tuples that hold (fromCity, toCity) 
    #   representing the from and to connecting nodes in the tree
    def buildRoute(self):
        trees = [[]]    
        n = len(self.cityMap.cities)      
        
        m = n*(n-1) / 2

        k = math.pow(2,(2*m)/n)


        # holds nodes in the order they are added
        preWalk = []
        
        #get smallest distance and chose the from city as start
        tmp = np.array(self.cityMap.distMatrix)
        start = np.amin(tmp)

        a = rand.randint(0,n-1)
        b = a
        while b == a:
            b = rand.randint(0,n-1)

        #start = self.cityMap.distMatrix[a][b]
        
        #select from city for this distance and set it visited
        # then append it to the preWalk
        self.cityMap.cities[start[1]].visited = True
        preWalk.append(start[1])
        
        #initialize options to all distances connecting to our start
        # vertex so we pick the smallest distance from that vertex
        options = self.cityMap.distMatrix[start[1]].tolist()

        fibheap = fib.Fibonacci_heap()
        for el in options:
            if el[0] == float('inf'):
                continue
            else:
                val = (el[1],el[2])
                fibheap.enqueue(val,el[0])

        # while we have not added all vertices to the tree
        while len(preWalk) < n:

            if len(fibheap) > k:
                print 'it will matter!'

            tmp_selected = fibheap.dequeue_min()
            selected = (tmp_selected.get_priority(),tmp_selected.get_value()[0],tmp_selected.get_value()[1])

            # pop the lowest distance
            fromCity = self.cityMap.cities[selected[1]]
            toCity = self.cityMap.cities[selected[2]]

            # check if we have already visted the 'to' city
            if toCity.visited == True:
                continue # pop next city
            else:           
                # mark city visited, append to MST and add all distances from the toCity vertex to our options
                toCity.visited = True 

                preWalk.append(toCity.id)

                tmpExt = self.cityMap.distMatrix[toCity.id]
                for el in tmpExt:
                    if el[0] == float('inf'):
                        continue
                    else:
                        val = (el[1],el[2])
                        fibheap.enqueue(val,el[0])
               
        preWalk.append(preWalk[0])
        self.route = preWalk
        self.distance = self.calcLength()
        self.resetVisited()


    # utility used to swap nodes for twoOpt improvement
    # Accepts the index of each node to swap 
    def twoOptSwap(self, i, j):
        new_route = self.route[:i]
        tmp = list(reversed(self.route[i:j+1]))
        new_route.extend(tmp)
        new_route.extend(self.route[j+1:])
        self.route = new_route
        

    # twoOpt First Improvement
    # A greedier method that looks for the first swap that will shorten the distance, performs the swap, and starts the search from the start again.
    # Continues until no more improvements can be found.
    def twoOptFI(self):
        self.distance = self.calcLength()
        change = -10

        while change < 0:
            for i in range(1,len(self.route)-2):
                for j in range(i+1,len(self.route)-1):
                    
                    curSum = self.cityMap.dist(self.route[i-1],self.route[i]) + self.cityMap.dist(self.route[j],self.route[j+1])
                    newSum = self.cityMap.dist(self.route[i-1],self.route[j]) + self.cityMap.dist(self.route[i],self.route[j+1])
                    
                    change = newSum - curSum

                    if change < 0:
                        self.twoOptSwap(i,j)
                        self.distance = self.calcLength()
                        break
                else:
                    continue
                break
        
    # twoOpt Best Improvement
    # Slightly different method. Instead of making the first improvement found, this method finds the best improvement at each stage and performs it. (Makes the improvement that shortens it the most)
    def twoOptBI(self):

        bestChange = -10
        while bestChange < 0:
            bestChange = 0
            for i in range(1,len(self.route)-2):
                for j in range(i+1, len(self.route)-1):
                   curSum = self.cityMap.dist(self.route[i-1],self.route[i]) + self.cityMap.dist(self.route[j],self.route[j+1])
                   newSum = self.cityMap.dist(self.route[i-1],self.route[j]) + self.cityMap.dist(self.route[i],self.route[j+1])

                   testChange = newSum - curSum

                   if bestChange > testChange:
                       bestChange = testChange
                       besti = i
                       bestj = j
            if bestChange != 0:
                self.twoOptSwap(besti,bestj)
                self.distance = self.calcLength()
        
    # Calculates the length of the currently set route
    def calcLength(self):

        length = 0
        for i in range(len(self.route)-1):
            j = i+1
            c1 = self.route[i]
            c2 = self.route[j]
            length += self.cityMap.dist(c1,c2)
        return length

    # Get number of cities
    def getCityCount(self):
        return self.cityCount

    # Get route array
    def getRoute(self):
        return self.route

    # Set route array
    def setRoute(self,rte):
        self.route = rte

    # Get distance integer
    def getDistance(self):
        return self.distance

    # Print solution to file
    def printSolution(self):
        print self.distance
        for i in self.route:
            print i

    # Save solution to file
    def saveSolution(self, fileWrite):
        fileWrite.write(str(self.distance))
        fileWrite.write("\n")
        for i in range(len(self.route)-1):
            fileWrite.write(str(self.route[i]))
            fileWrite.write("\n")


