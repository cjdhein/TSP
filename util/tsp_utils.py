# Cody Dhein
# Val Chapple

import sys
import math

#    City
# Represents a given city on the map.
# Has data members 'id' 'x' and 'y'
# Main usage will be to call distanceTo
class City:
    def __init__(self,id,x,y):
        self.id = id
        self.x = int(x)
        self.y = int(y)
    
    # returns city's id
    def getId(self):
        return self.id
    
    # returns tuple with x,y coords of city
    def getCoords(self):
        return (self.x,self.y)
    
    # accepts another city object and returns the euclidean
    # distance to that other city rounded to nearest int
    def distanceTo(self, otherCity):
        # (I did some testing on various methods of calculating this result (using numpy function, using pow(), etc)
        # This method was faster than the others.
        initialVal = math.sqrt((self.x - otherCity.x)**2 + (self.y - otherCity.y)**2)
        
        roundedVal = int(round(initialVal))
        
        return roundedVal

#    Map
# Holds the entire map/list of cities from the input file
# Constructor accepts the name of the input file and it
# then builds a list of City objects
class Map:
    def __init__(self, inputFileName):
        self.cities = []
        self.loadCities(inputFileName)
    
    # load's cities from input file
    def loadCities(self,text):
        _rawData = open(text,"r")
        _data = _rawData.read().splitlines()
        
        for _line in _data:
            newCity = _line.split()
            self.cities.append(City(newCity[0], newCity[1], newCity[2]))
    
    # function to print all cities
    # format: 'id' 'x' 'y'
    def printMap(self):
        for city in self.cities:
            print city.id + ' ' + city.x + ' ' + city.y

# Accepts the IDs of two different cities and
# gives us the distance between them
def distanceBetween(self,id1, id2):
    dist = self.cities[int(id1)].distanceTo(self.cities[int(id2)])
    return dist

if __name__ == '__main__':
    inFile = sys.argv[1]
    
    cities = Map(inFile)
    print cities.distanceBetween(5,29)
