#!/usr/bin/python2.7

# Val Chapple
# Cody Dhein
# Date: Nov 22, 2017

# MST Driver program
#
# Greedy algorithm
# Usage:
# tsp-mst.py <filename>
# INPUTS:
# filename:
#   each line is a city with city Id, x-coord, y-coord

import sys
sys.path.insert(0, '../util')

import timeit
from tsp_utils import Map, City
from MST import MST
import math
import random as rand

if __name__ == '__main__':
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
    map = Map(inFile)


    print 'File loaded with ' + str(len(map.cities))
    # t2 - t1 is time taken to calculate distances

    startCity = raw_input('Specify starting city in the range 0 - ' + str(len(map.cities)-1) + ', or leave blank for random start: ')
    runRandom = True
    try:
        startCity = int(startCity)
        if startCity >= 0 and startCity <= len(map.cities)-1:
            runRandom = False
        else:
            print 'Invalid input; running with random start.'
    except:
            print 'Invalid input; running with random start.'

    # Build MST and route
    mst = MST(map)

    t2 = timeit.default_timer() 

    if runRandom == True:
        startCity = rand.randint(0,len(map.cities)-1)

    print 'Running with start city as ' + str(startCity)
    mst.buildRoute(startCity)

    t3 = timeit.default_timer()

    # t3 - t2 is time taken to build the MST and route
    print 'Finished MST and route build, time: ' + str(t3-t2)
   

   # Optimize route
    #mst.twoOptBI()
    mst.twoOptFI()
    
    t4 = timeit.default_timer()
    
    print 'Finished optimization, time: ' + str(t4 - t3)
    print ''
    print 'Route length: ' + str(mst.calcLength())

    fileWrite = open(filename + ".tour", "w")
    mst.saveSolution(fileWrite)
    fileWrite.close()

    fileWrite = open(filename + ".tourTime", "w")
    fileWrite.write(str(t4-t2) + "\n")
    fileWrite.close()
