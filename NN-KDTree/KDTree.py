# Val Chapple
# Cody Dhein
# Date: Nov 22, 2017
#
# Resources:
# Overall Concepts: An introductory tutorial on kd trees by Andrew W  Moore
#       Carnegie Mellon University, Extract from Andrew Moore's PhD Thesis
# Construction: https://www.cise.ufl.edu/class/cot5520fa09/CG_RangeKDtrees.pdf
# Querying: https://web.engr.oregonstate.edu/~tgd/classes/534/slides/part3.pdf
#
import sys
from operator import itemgetter
#import random
import heapq
import math
import timeit

# KDTreeNN
#
# Build KDTree from city data points
# Use Tree to find solution
def kdTreeNN(filename, outfilename):

    # Read file with city Id, city x, and city y
    try:
        inFile = open(filename, "r")
    except:
        print("No file named: " + filename)
        sys.exit()

    text = inFile.read().splitlines()

    # Save data as 2D list [ [ id, x, y ],... ]
    points = [ [int(i[0]), int(i[1]), int(i[2])] for i in [j.split() for j in text ]]

    # Create kd-tree structure with points, 0 start depth, and 2D(x and y)
    root = kDTree( points, 0, 2)

    # Set Start city and find Route
    city = points[0]
    (totalDist, route) = kDTreeSearchNN(root, city, len(points))

    # Save route
    outFile = open(outfilename, "w")
    outFile.write(str(totalDist) + "\n")
    for i in route:
        outFile.write(str(i) + "\n")
    return

# kDNode
# Nodes of trees
# value is the city
# left and right point to other nodes
# dim represents the splitting axis (aka index to use on the city data)
class kDNode:
    def __init__(self, city, left, right, dim):
        self.city = city
        self.visited = False
        self.left = left
        self.right = right
        self.dim = dim      # 0 or 1

    def __str__(self, level=1):
        ret = ""
        ret += "\t"*(level-1)+"-----"+repr(self.city[0])+"\n"
        if self.left != None:
            ret += self.left.__str__(level+1)
        if self.right != None:
            ret += self.right.__str__(level+1)
        return ret


# kDTree
# Creates kd-tree recursively with city data, depth into tree and dimensions (k)
# Returns a kDNode and its subtree
def kDTree( points, depth, k ):
    # Check that points has a list
    if len(points) < 1:
        return None

    # sort by axis chosen to find median:
    #   even for x= equation, and odd for y= equation
    points.sort(key=itemgetter(depth % k + 1))
    mid = len(points) / 2

    return kDNode(
        points[mid],
        kDTree(points[:mid], depth + 1, k),
        kDTree(points[mid+1:], depth + 1, k),
        depth % k + 1
    )

# printkDtree
# Print tree (tabs represent level of tree), grows left to right
def printkDtree( tree ):
    print(tree)
    print(tree.city[0])


# kDTreeSearchNN
# Determines a tour distance and route
# Uses greedy method of finding nearest unvisited city to target city
def kDTreeSearchNN( tree, point, numCities ):
    target = point
    route = []
    totalDist = 0

    # Find nearest city for entire loop
    while len(route) < numCities:
        heap = []
        bestDistSqd = float('inf')
        bestNode = None

        # Add to priority queue
        heapq.heappush( heap, (0 , tree ) )
        while len(heap) != 0:
            (d, node) = heapq.heappop( heap )
            if (d >= bestDistSqd):
                break       # No node is closer, end while loop
            if node == None:
                continue    # Skip node

            # Get distance squared value for comparison
            dist = dist_sqd(node.city, target)

            # Possibly update best distance ONLY IF city is unvisited
            if node.visited == False:
                if (dist < bestDistSqd ):
                    bestDistSqd = dist
                    bestNode = node

            # Add child nodes to priority queue, adjusting priority left/right
            if (target[node.dim] <= node.city[node.dim]):
                heapq.heappush(heap, (0, node.left ))
                heapq.heappush(heap, (dist, node.right ))  # sorting by dist?
            else:
                heapq.heappush(heap, (0, node.right ))
                heapq.heappush(heap, (dist, node.left ))

        # Add nearest neighbor to route, mark visited, update target
        bestNode.visited = True
        route.append(bestNode.city[0])
        target = bestNode.city
        totalDist += int(round(math.sqrt(bestDistSqd)))

    # Add distance from last target city to start city
    totalDist += int(round(math.sqrt(dist_sqd(target, point))))
    return (totalDist, route)

def dist_sqd( city1, city2 ):
    x_dist = abs(city2[1] - city1[1])
    y_dist = abs(city2[2] - city1[2])
    return x_dist*x_dist + y_dist*y_dist


if __name__ == '__main__':
    t1= timeit.default_timer()
    # Check input file name exists
    try:
        filename = sys.argv[1]
    except:
        print("Usage: " + sys.argv[0] + " <inputfilename>")
        sys.exit()
    #random.seed(1)
    outfilename = filename + ".tour"
    kdTreeNN(filename, outfilename)

    t2 = timeit.default_timer()

    fileWrite = open(filename + ".tourTime", "w")
    fileWrite.write(str(t2-t1) + "\n")
    fileWrite.close()
