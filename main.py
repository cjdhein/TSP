#!/usr/bin/python2.7

# Val Chapple
# Cody Dhein
# Date: Nov 22, 2017

# TSP Driver program
# Reads input data set and selects algorithm based on size.
#
# Usage:
# tsp.py [options] <filename>
# INPUTS:
# filename:
#   each line is a city with city Id, x-coord, y-coord
# options:
#   -u : (unlimied) Sets program to run for unlimited time
#   -s [start node] : Provide valid integer representing start node

import sys
import os.path
sys.path.append('./util')
sys.path.append('./MST')
sys.path.append('./NN')
sys.path.append('./NN-KDTree')

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
        print("Usage: " + sys.argv[0] + " [options]" + " <inputfilename>")
        sys.exit()

    try:
        inFile = open(filename, "r")
    except:
        print("No file named: " + filename)
        sys.exit()
    
    unlimitedRun = False
    randomRun = True

    # Really ugly command line argument handling!!
    try:
        argCount = len(sys.argv)
        if argCount == 3:
            if sys.argv[2] == '-u':
                unlimitedRun = True
            else:
                print("Invalid argument provided")
                sys.exit(1)
        elif argCount == 4:
            if sys.argv[2] != '-s':
                print("Invalid argument ided.")
                sys.exit(1)
            else:
                startCity = int(sys.argv[3])
                randomRun = False
        elif argCount == 5:
            if sys.argv[2] == '-u':
                unlimitedRun = True
                if sys.argv[3] != '-s':
                    print("Invalid argument provided.")
                    sys.exit(1)
                else:
                    startCity = int(sys.argv[4])
                    randomRun = False
            elif sys.argv[2] == '-s':
                startCity = int(sys.argv[3])
                randomRun = False
                if sys.argv[4] != '-u':
                    print("Invalid argument provided.")
                    sys.exit(1)
                else:
                    unlimitedRun = True
        elif argCount > 5:
            sys.exit(1)

    except:
        print("Invalid argument provided. Ensure valid integer arugment is given for starting node.")
        sys.exit(1)


    if unlimitedRun == True:
        print("Running algorithm with no time limit.")
    else:
        print("Running with 3 minute time limit.")

    # Split text input into lines and read length to determine algorithm to run
    dataIn = inFile.read().splitlines()
    inputSize = len(dataIn)

    print 'File loaded with ' + str(inputSize)

    t2 = timeit.default_timer() 

    if inputSize > 500:
        ###TODO: Implement the running of KDTree for the larger data sets. Since I already read in the data as lines, we might want to edit the data input handled in your kdTreeNN function.

        print 'Run with KDTree'
        exit(0)
    else: # Running with MST
        # Create data structure
        map = Map(dataIn)


        # Checks for valid integer argument to specify desired start node for input file sizes
        # below 500. If none is given startCity is set to a random value.
        if randomRun == False:
            if startCity < 0 or startCity > len(map.cities)-1:
                print("Provided start node is invalid, running with random start...")
                randomRun = True

        if randomRun == True:
            startCity = rand.randint(0,len(map.cities)-1)
        # Build MST and route
        mst = MST(map)


        print 'Running with start city as ' + str(startCity)
        mst.buildRoute(startCity)


        # Optimize route
        if inputSize == 250:
            mst.twoOptFI()
        else:
            mst.twoOptBI()
        length = mst.calcLength() 
        print 'Route length: ' + str(length)
        t3 = timeit.default_timer()

        # t3 - t2 is time taken to build the MST and route
        print 'Finished MST and route build, time: ' + str(t3-t2)

    fileWrite = open(filename + ".tour", "w")
    mst.saveSolution(fileWrite)
    fileWrite.close()

#    fileWrite = open(filename + ".tourTime", "w")
#    fileWrite.write(str(t4-t2) + "\n")
#    fileWrite.close()
