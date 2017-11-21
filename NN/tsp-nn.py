#!/usr/bin/python2.7

# Val Chapple
# Cody Dhein

import sys
sys.path.insert(0, '../util')

from tsp_utils import Map, City

if __name__ == '__main__':
    try:
        inFile = sys.argv[1]
    except:
        print("Usage: " + sys.argv[0] + " <inputfilename>")
        sys.exit()

    cities = Map(inFile)
