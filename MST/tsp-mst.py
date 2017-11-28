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
import multiprocessing as mp

# run as a sub process; terminate externally after set time elapsed
# runs FI and BI alternately
def bestOfMany(mst):
    best = float('inf')
    iteration = 1
    while True:
        print 'Iteration: ' + str(iteration)
        mst.buildRoute()
        mst.twoOptBI()
        tmp = mst.calcLength()
        iteration += 1
        if tmp < best:
            best = tmp
            print 'New best: ' + str(best)



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

    t1 = timeit.default_timer()

    # Create data structure
    cities = Map(inFile)

    t2 = timeit.default_timer() 

    # t2 - t1 is time taken to calculate distances
    print 'Finished distance calc, time: ' + str(t2-t1)

    # Build MST and route
    mst = MST(cities)
    mst.buildRoute()

    t3 = timeit.default_timer()

    # t3 - t2 is time taken to build the MST and route
    print 'Finished MST and route build, time: ' + str(t3-t2)
   

  ## Below is implemented to allow multiple iterations of improvement and selection of the best
  ### within the 3 minute time limit.

  #  # time limit of 2min 55sec
  #  limit = 175.00
  #  
  #  start = timeit.default_timer()
  #  subProc = mp.Process(target=bestOfMany,name="bestOfMany",args=(mst,))
  #  subProc.start()
  #  tmp = timeit.default_timer()

  #  while (tmp - start) < limit:
  #      tmp = timeit.default_timer()

  #  subProc.terminate()
  
    # Optimize route
    #mst.twoOptBI()
    mst.twoOptFI()
    
    t4 = timeit.default_timer()
    
    print 'Finished optimization, time: ' + str(t4 - t3)
    print ''
    print 'Route length: ' + str(mst.calcLength())
    print 'Total time: ' + str(t4-t1)

    fileWrite = open(filename + ".tour", "w")
    mst.saveSolution(fileWrite)
    fileWrite.close()

    fileWrite = open(filename + ".tourTime", "w")
    fileWrite.write(str(t4-t1) + "\n")
    fileWrite.close()
