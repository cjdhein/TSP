import sys
import heapq
import tsp_utils as utils
import numpy as np

# Builds a Minimum Spanning Tree using Prim's algorithm
# Accepts: pre-generated Map of cities
# Returns: set of tuples that hold (fromCity, toCity) 
#	representing the from and to connecting nodes in the tree
def primMST(map):
		
	#get distances(weights)
	dists = map.distMatrix
	cities = map.cities
	full = len(cities)      
	
	# holds the mst as a tuple of (fromNode, toNode)
	mstPath = []

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
			mstPath.append((fromCity.id,toCity.id))
			preWalk.append(toCity.id)
			options.extend(dists[toCity.id])	
			
			# reprioritize the queue by distance
			heapq.heapify(options)						
	preWalk.append(preWalk[0])
	return preWalk

# swaps edges
# accepts the full route and the indices for two nodes to swap	
def twoOptSwap(route,i,j):
	new_route = route[:i]
	tmp = list(reversed(route[i:j+1]))
	new_route.extend(tmp)
	new_route.extend(route[j+1:])
	return new_route
	
# Performs a twoOpt improvement on the candidate solution
def twoOptImprove(route,distances):
	noSwap = route[0]
	
	currentBest = calcLength(route,distances)
	prevBest = currentBest + 1

	while currentBest < prevBest:
		prevBest = currentBest
		for i in range(1,len(route)-2):
			for j in range(i+1,len(route)-1):
#				print 'Try swap ' + str(route[i]) + ', ' + str(route[j])
				candidate = twoOptSwap(route,i,j)
				candidate_dist = calcLength(candidate,distances)
				if candidate_dist < currentBest:
					route = candidate
					currentBest = candidate_dist
					break
			else:
				continue
			break
	currentBest = calcLength(route,distances)
	return route

# calculates total length of the given tour
# accepts the tour and a distance Matrix
def calcLength(tour, dists):

	length = 0
	
	for i in range(len(tour)-1):
		j = i+1
		c1 = tour[i]
		c2 = tour[j]
		length += dists[c1][c2][0]
	return length

#  generates output
def setTour(route, length, fileName):
	outFile = open(fileName,"w")

	outFile.write(str(length)+'\n')
	for i in range(len(route)-1):
		outFile.write(str(route[i])+'\n')



inFilename = sys.argv[1]
inFile = open(inFilename,"r")

outFilename = inFilename + '.tour'

# build full map using input file
# also creates distance matrix
map = utils.Map(inFile)
route = primMST(map)
print calcLength(route,map.distMatrix)
print route

route = twoOptImprove(route,map.distMatrix)
print calcLength(route,map.distMatrix)
print route

# length = calcLength(route,map.distMatrix)
# setTour(route, length, outFilename)

