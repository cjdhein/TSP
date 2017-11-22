# Val Chapple
# Cody Dhein
# Date: Nov 22, 2017

from tsp_utils import Map, City
import sys

# NearestNeighbor Class
#
# Greedy algorithm

## Initialize with an instance of Map class
class NearestNeighbor:
    def __init__(self, cityMap):
        if cityMap.__class__.__name__ != "Map":
            print("invalid city")
            return
        else:
            self.cityMap = cityMap
            self.route = []
            self.distance = float('inf')

    # If optDistance is known, compare it to
    # NN solution of each starting cities, recording best percentage route
    def calculateAllStartingRoutes(self, optDist):
        bestStartCity = None
        bestStartPercent = float('inf')
        bestRoute = []
        bestDist = float('inf')
        for i in self.cityMap.cities:
            self.calculateRoute(i.getId())

            percent = abs(self.distance * 10000 / optDist - 10000)
            if percent < bestStartPercent:
                bestStartCity = i
                bestStartPercent = percent
                bestRoute = self.route
                bestDist = self.distance

            # print( str(self.distance) + " / " + str(optDist) + " = " + str(self.distance * 100 / optDist))
        print("Distance: " + str(bestDist) + "\tStartId: " + str(bestStartCity.getId()) + "\tPercentError: " + str(bestStartPercent/100.0))
        self.route = bestRoute
        self.distance = bestDist


    # Calculate the distance starting at the city with startId
    def calculateRoute(self, startId):
        # Use distMatrix from Map instance to determine nearest neighbor
        self.route = []
        self.distance = float('inf')

        # Tally variables
        count = 0
        n = len(self.cityMap.cities)
        totalDistance = 0

        # Starting City (add to visited)
        city = self.cityMap.cities[ startId]
        visited = [city.getId()]
        count += 1

        while ( count < n ):
            minCity = None
            minDist = float('inf')

            # Loop through distances to all cities to find nearest city
            for i in self.cityMap.cities:
                if i.getId() in visited:
                    continue
                if (minDist > self.cityMap.distMatrix[city.getId()][i.getId()][0]):
                    minCity = i
                    minDist = self.cityMap.distMatrix[city.getId()][i.getId()][0]

            if (minCity is not None):
                city = minCity
                totalDistance += minDist
                visited.append(city.getId())
                count += 1
            else:
                print("error in calculateRoute() nn.py")
                print(minCity)
                print(minDist)
                sys.exit()

        self.route += visited
        self.distance = totalDistance

    # Get route array
    def getRoute(self):
        return self.route

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
        for i in self.route:
            fileWrite.write(str(i))
            fileWrite.write("\n")
