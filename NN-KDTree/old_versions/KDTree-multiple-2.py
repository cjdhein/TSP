# # Val Chapple
# # Cody Dhein
# # Date: Nov 22, 2017
# #
# # Resources:
# # Overall Concepts: An introductory tutorial on kd trees by Andrew W  Moore
# #       Carnegie Mellon University, Extract from Andrew Moore's PhD Thesis
# # Construction: https://www.cise.ufl.edu/class/cot5520fa09/CG_RangeKDtrees.pdf
# # Querying: https://web.engr.oregonstate.edu/~tgd/classes/534/slides/part3.pdf
# #
# import sys
# from operator import itemgetter
#
# #import random
# import heapq
# import math
# import timeit
# import numpy as np
#
# # KDTreeNN
# #
# # Build KDTree from city data points
# # Use Tree to find solution
# def kdTreeNN(filename, outfilename):
#
#     # Read file with city Id, city x, and city y
#     try:
#         inFile = open(filename, "r")
#     except:
#         print("No file named: " + filename)
#         sys.exit()
#
#     text = inFile.read().splitlines()
#
#     # Save data as 2D list [ [ id, x, y ],... ]
#     points = [ [int(i[0]), int(i[1]), int(i[2])] for i in [j.split() for j in text ]]
#
#     # Create kd-tree structure with points, 0 start depth, and 2D(x and y)
#     root = kDTree( points, 0, 2)
#
#     # Distance Matrix
#     numNN = len(points) * .002
#     if (numNN < 10):
#         numNN = 10
#
#     #fileResults = open("results1.txt", "w")
#     (totalDist, routeNodes, distSqdMatrix) = kDTreeSearchNN(root, len(points), numNN)
#     #print(totalDist, routeNodes)
#     #fileResults.write("total dist: " + str(totalDist) + "\n")
#     # for i in routeNodes:
#     #     fileResults.write(str(i.city[0]) + ", " + str(i.city[1]) + ", " + str(i.city[2]) + "\n")
#     #
#     # fileResults.close()
#
#     fileResults = open("results2.txt", "w")
#     # (totalDist, route) = twoOptImprove(route , distSqdMatrix)
#     (totalDist, route) = twoOptImproveK(routeNodes , distSqdMatrix)
#     #print(totalDist, route)
#     fileResults.write("total dist: " + str(totalDist) + "\n")
#     for i in route:
#         fileResults.write(str(i) + "\n")
#     fileResults.close()
#
#     # Save route
#     outFile = open(outfilename, "w")
#     outFile.write(str(totalDist) + "\n")
#     for i in route:
#         outFile.write(str(i) + "\n")
#     return
#
# # kDNode
# # Nodes of trees
# # value is the city
# # left and right point to other nodes
# # dim represents the splitting axis (aka index to use on the city data)
# class kDNode:
#     def __init__(self, city, left, right, dim):
#         self.city = city
#         self.visited = False
#         self.left = left
#         self.right = right
#         self.dim = dim      # 0 or 1
#         self.nn = []
#
#     def addNN( self, distSqd, node, maxNN ):
#         if len(self.nn) < maxNN:
#             self.nn.append( ( distSqd, node ) )
#         else:
#             self.nn.sort(key=itemgetter(0), reverse=True)
#             if (self.nn[0][0] > distSqd):
#                 # Replace largest dist with dist
#                 self.nn[0] = ( distSqd, node )
#
#     def getNNs( self ):
#         return [ x for x in self.nn ]
#
#     def __str__(self, level=1):
#         ret = ""
#         ret += "\t"*(level-1)+"-----"+repr(self.city[0])+"\n"
#         if self.left != None:
#             ret += self.left.__str__(level+1)
#         if self.right != None:
#             ret += self.right.__str__(level+1)
#         return ret
#
# # kDTree
# # Creates kd-tree recursively with city data, depth into tree and dimensions (k)
# # Returns a kDNode and its subtree
# def kDTree( points, depth, k ):
#     # Check that points has a list
#     if len(points) < 1:
#         return None
#
#     # sort by axis chosen to find median:
#     #   even for x= equation, and odd for y= equation
#     points.sort(key=itemgetter(depth % k + 1))
#     mid = len(points) / 2
#
#     return kDNode(
#         points[mid],
#         kDTree(points[:mid], depth + 1, k),
#         kDTree(points[mid+1:], depth + 1, k),
#         depth % k + 1
#     )
#
# # printkDtree
# # Print tree (tabs represent level of tree), grows left to right
# def printkDtree( tree ):
#     print(tree)
#     print(tree.city[0])
#
#
# # kDTreeSearchNN
# # Determines a tour distance and route
# # Uses greedy method of finding nearest unvisited city to target city
# def kDTreeSearchNN( tree, numCities, maxNN ):
#     start = tree
#     target = start
#     route = []
#     totalDist = 0
#     distSqdMatrix  = [[ -1 for x in range(0, numCities)] for y in range(0, numCities)]
#
#     # Find nearest city for entire loop
#     while len(route) < numCities:
#         heap = []
#         bestDistSqd = float('inf')
#         bestNode = None
# 
#         # Add to priority queue
#         heapq.heappush( heap, (0 , tree ) )
#         while len(heap) != 0:
#             (d, node) = heapq.heappop( heap )
#             if (d >= bestDistSqd):
#                 break       # No node is closer, end while loop
#             if node == None:
#                 continue    # Skip node
#
#             # Get distance squared value for comparison
#             dist = distSqdMatrix[ node.city[0] ][ target.city[0] ]
#             if dist == -1:
#                 distSqdMatrix[ node.city[0] ][ target.city[0] ] = dist_sqd( node.city, target.city )
#                 distSqdMatrix[ target.city[0] ][ node.city[0] ] = distSqdMatrix[ node.city[0] ][ target.city[0] ]
#                 dist = distSqdMatrix[ node.city[0] ][ target.city[0] ]
#             target.addNN( dist , node, maxNN)
#
#             # Possibly update best distance ONLY IF city is unvisited
#             if node.visited == False:
#                 if (dist < bestDistSqd ):
#                     bestDistSqd = dist
#                     bestNode = node
#
#             # Add child nodes to priority queue, adjusting priority left/right
#             if (target.city[node.dim] <= node.city[node.dim]):
#                 heapq.heappush(heap, (0, node.left ))
#                 heapq.heappush(heap, (dist, node.right ))  # sorting by dist?
#             else:
#                 heapq.heappush(heap, (0, node.right ))
#                 heapq.heappush(heap, (dist, node.left ))
#
#         # Add nearest neighbor to route, mark visited, update target
#         bestNode.visited = True
#         route.append(bestNode)
#         target = bestNode
#         totalDist += int(round(math.sqrt(bestDistSqd)))
#
#     # Add distance from last target city to start city
#     totalDist += int(round(math.sqrt(dist_sqd(target.city, start.city))))
#     return (totalDist, route, distSqdMatrix)
#
# def dist_sqd( city1, city2 ):
#     x_dist = city2[1] - city1[1]
#     y_dist = city2[2] - city1[2]
#     return x_dist*x_dist + y_dist*y_dist
#
# # swaps edges
# # accepts the full route and the indices for two nodes to swap
# def twoOptSwap(route,i,j):
# 	new_route = route[:i]
# 	tmp = list(reversed(route[i:j+1]))
# 	new_route.extend(tmp)
# 	new_route.extend(route[j+1:])
# 	return new_route
#
# # Performs a twoOpt improvement on the candidate solution
# def twoOptImproveK(routeNodes , distances):
#     noSwap = routeNodes[0]
#     currentBest = calcLengthNodes(routeNodes,distances)
#     prevBest = currentBest + 1
#     n = 0
#     while currentBest < prevBest:
#         n += 1
#         #print(str(n))
#         prevBest = currentBest
#         for i in range(0, len(routeNodes)):
#             for nn in routeNodes[i].getNNs():
#                 nnIndex = -1
#                 # nn is a tuple of (distSqdToNN, kDNode_NN)
#                 for x in range(0, len(routeNodes)):
#                     if routeNodes[x].city == nn[1].city:
#                         nnIndex = x
#
#                 if (i < nnIndex):
#                     candidate = twoOptSwap(routeNodes,i,nnIndex)
#                 else:
#                     candidate = twoOptSwap(routeNodes,nnIndex, i)
#
#                 candidate_dist = calcLengthNodes(candidate,distances)
#                 if candidate_dist < currentBest:
#                     routeNodes = candidate
#                     currentBest = candidate_dist
#                     #break
#             else:
# 				continue
#             break
# 	currentBest = calcLengthNodes(routeNodes,distances)
#     route  = [ x.city[0] for x in routeNodes ]
#     return (currentBest,  route )
#
# # calculates total length of the given tour
# # accepts the tour and a distance Matrix
# def calcLengthNodes(routeNodes, dists):
#     length = 0
#     n = 0
#     #print("HERE")
#     for i in range(len(routeNodes)-1):
#         j = i+1
#         c1 = routeNodes[i].city[0]
#         c2 = routeNodes[j].city[0]
#         if (dists[c1][c2] == -1):
#             dists[c1][c2] = dist_sqd(routeNodes[i].city, routeNodes[j].city)
#         length += int(round(math.sqrt(dists[c1][c2])))
#         # print(str(c1) + ", " + str(c2) + ", " + str(dists[c1][c2]))
#         # print(str(c2) + ", " + str(length))
#
#     # Add last leg of trip
#     c1 = routeNodes[0].city[0]
#     c2 = routeNodes[ len(routeNodes) - 1].city[0]
#     #print("First City: " + str(c1))
#     #print("Last City: " + str(c2))
#     if (dists[c1][c2] == -1):
#         dists[c1][c2] = dist_sqd(routeNodes[0].city, routeNodes[ len(routeNodes) - 1].city)
#     length += int(round(math.sqrt(dists[c1][c2])))
#     n  += 1
#     #print(str(c1) + ", " + str(length))
#     return length
#
# if __name__ == '__main__':
#     t1= timeit.default_timer()
#     # Check input file name exists
#     try:
#         filename = sys.argv[1]
#     except:
#         print("Usage: " + sys.argv[0] + " <inputfilename>")
#         sys.exit()
#
#     outfilename = filename + ".tour"
#     kdTreeNN(filename, outfilename)
#
#     t2 = timeit.default_timer()
#
#     fileWrite = open(filename + ".tourTime", "w")
#     fileWrite.write(str(t2-t1) + "\n")
#     fileWrite.close()
