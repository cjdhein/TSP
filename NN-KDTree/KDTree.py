# Val Chapple
# Cody Dhein
# Date: Nov 22, 2017

# from tsp_utils import Map, City
import sys
from operator import itemgetter

# KDTree Class
#
# Build KDTree from city data points

## Initialize
def BuildKDTree2(filename):
    try:
        inFile = open(filename, "r")
    except:
        print("No file named: " + filename)
        sys.exit()

    # Read file
    text = inFile.read().splitlines()

    # 2D array [ [ id, x, y ],... ]
    points = [ [int(i[0]), int(i[1]), int(i[2])] for i in [j.split() for j in text ]]

    # print(points)
    # kd-tree with points, 0 depth start, and dimensions of 2 (x and y)
    root = kDTree( points, 0, 2)
    printkDtreePreOrder(root)

def printkDtreePreOrder( tree ):
    try:
        sys.stdout.write("(")
        sys.stdout.write( str(tree.city) )
        sys.stdout.write(",")
        printkDtreePreOrder( tree.left )
        sys.stdout.write(",")
        printkDtreePreOrder( tree.right )
        sys.stdout.write(")")
    except AttributeError:
        sys.stdout.write("None")


class kDNode:
    def __init__(self, city, left, right):
        self.city = city
        self.left = left
        self.right = right

def kDTree( points, depth, d ):
    # Check that points has a list
    if len(points) < 1:
        return None

    # sort by axis chosen to find median:
    # even for x= equation, and odd for y= equation
    points.sort(key=itemgetter(depth % d + 1))
    mid = len(points) / 2

    return kDNode(
        points[mid],
        kDTree(points[:mid], depth + 1, d),
        kDTree(points[mid+1:], depth + 1, d)
    )
    # count = 0
    # for i in points:
    #     print(str(count) + " " + str(i))
    #     count += 1
    # print(points[mid])


if __name__ == '__main__':
    # Check input file name exists
    try:
        filename = sys.argv[1]
    except:
        print("Usage: " + sys.argv[0] + " <inputfilename>")
        sys.exit()

    BuildKDTree2(filename)
