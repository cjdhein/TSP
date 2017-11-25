# Cody Dhein
# Val Chapple

import sys
import math
import numpy as np
import random

#       City
# Represents a given city on the map.
# Has data members 'id' 'x' and 'y'
# Main usage will be to call distanceTo
class City:
	def __init__(self,id,x,y):
		self.id = int(id)
		self.x = int(x)
		self.y = int(y)
		self.visited = False

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


#       Map
# Holds the entire map/list of cities from the input file
# Constructor accepts the loaded input file and
# then builds a list of City objects and a distance matrix
class Map:
	def __init__(self, inputFile):
		self.cities = []
		self.loadCities(inputFile)
		self.distMatrix = np.array([[x for x in self.cities] for y in self.cities])
		self.buildMatrix()

	# load's cities from input file
	def loadCities(self,text):
		_data = text.read().splitlines()

		for _line in _data:
			newCity = _line.split()
			self.cities.append(City(newCity[0], newCity[1], newCity[2]))

	# format: 'id' 'x' 'y'
	def printMap(self):
		for city in self.cities:
			print str(city.id)

	# Accepts the IDs of two different cities and
	# gives us the distance between them
	def distanceBetween(self,id1, id2):
		dist = self.cities[int(id1)].distanceTo(self.cities[int(id2)])
		return dist

	# Build a distance matrix containing the distances between each city x and city y
	# If x=y, distance is float infinity
	# The values in the array are tuples containing the distance, from city id and to city id
	def buildMatrix(self):
		for i in range(0,len(self.cities)):
			for j in range(i,len(self.cities)):
				city1 = self.cities[i]
				city2 = self.cities[j]
				if city1 == city2:
					dist = float('inf')
				else:
					dist = city1.distanceTo(city2)
				self.distMatrix[city1.getId()][city2.getId()] = (dist,city1.getId(),city2.getId())
				self.distMatrix[city2.getId()][city1.getId()] = (dist,city2.getId(),city1.getId())

	def printMatrix(self):
		print self.distMatrix
