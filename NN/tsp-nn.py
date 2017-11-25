#!/usr/bin/python2.7

# Val Chapple
# Cody Dhein
# Date: Nov 22, 2017

# NearestNeighbor Driver program
#
# Greedy algorithm
# Usage:
# tsp-nn.py <filename> [optimal distance]
# INPUTS:
# filename:
#   each line is a city with city Id, x-coord, y-coord
# optimal distance: (WARNING: Only use for small number of cities)
#   optional argument if optimal distance is known
#   program compares distances of each city as a start city to the optimal solution

import sys
sys.path.insert(0, '../util')

import timeit
from tsp_utils import Map, City
from nn import NearestNeighbor

if __name__ == '__main__':
    t1 = timeit.default_timer()
    # Check input file name exists and is readable file
    try:
        filename = sys.argv[1]
    except:
        print("Usage: " + sys.argv[0] + " <inputfilename>")
        sys.exit()

    try:
        inFile = open(filename, "r")
    except:
        print("No file named: " + filename)
        sys.exit()

    # Create data structure
    cities = Map(inFile)
    NN = NearestNeighbor(cities)

    # Check each start city with optimal distance provided
    # or calculate nearest neighbor distance from first city only
    try:
        optDistance = int(sys.argv[2])
        NN.calculateAllStartingRoutes(optDistance)
    except:
        NN.calculateRoute(0)
        fileWrite = open(filename + ".tour", "w")
        NN.saveSolution(fileWrite)
        fileWrite.close()

    t2 = timeit.default_timer()
    fileWrite = open(filename + ".tourTime", "w")
    fileWrite.write(str(t2-t1) + "\n")
    fileWrite.close()
