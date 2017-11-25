# # Val Chapple
# # Cody Dhein
# # Date: Nov 22, 2017
#
# # from tsp_utils import Map, City
# import sys
# from operator import itemgetter
#
# # KDTree Class
# #
# # Build KDTree from city data points
#
# ## Initialize
# def BuildKDTree2(filename):
#     try:
#         inFile = open(filename, "r")
#     except:
#         print("No file named: " + filename)
#         sys.exit()
#
#     # Read file
#     text = inFile.read().splitlines()
#
#     # 2D array [ [ id, x, y ],... ]
#     pointsX = [ [int(i[0]), int(i[1]), int(i[2])] for i in [j.split() for j in text ]]
#
#     pointsX.sort(key=itemgetter(1))
#     pointsY = sorted(pointsX, key=itemgetter(2))
#     # print(points)
#     # kd-tree with points, 0 depth start, and dimensions of 2 (x and y)
#     start = 0
#     end = len(pointsX)
#     root = kDTree( pointsX, pointsY, start, end-1,  0, 2)
#     printkDtreePreOrder(root)
#
# def printkDtreePreOrder( tree ):
#     try:
#         sys.stdout.write("(")
#         sys.stdout.write( str(tree.city) )
#         sys.stdout.write(",")
#         printkDtreePreOrder( tree.left )
#         sys.stdout.write(",")
#         printkDtreePreOrder( tree.right )
#         sys.stdout.write(")")
#     except AttributeError:
#         sys.stdout.write("None")
#
#
# class kDNode:
#     def __init__(self, city, left, right):
#         self.city = city
#         self.left = left
#         self.right = right
#
# def kDTree( pointsX, pointsY, start, end, depth, d ):
#     # Check that points has a list
#     # if len(points) < 1:
#     print(start, end, depth)
#
#     if start >= end-1:
#         print("None")
#         return None
#
#     # Find median: even for x= equation, and odd for y= equation
#     mid = ( end - start ) / 2
#
#     if depth % d == 0:
#         return kDNode(
#             pointsX[mid],
#             kDTree(pointsX, pointsY, start, mid-1, depth + 1, d),
#             kDTree(pointsX, pointsY, mid+1, end, depth + 1, d)
#         )
#     elif depth % d == 1:
#         return kDNode(
#             pointsY[mid],
#             kDTree(pointsX, pointsY, start, mid-1, depth + 1, d),
#             kDTree(pointsX, pointsY, mid+1, end, depth + 1, d)
#         )
#     # count = 0
#     # for i in points:
#     #     print(str(count) + " " + str(i))
#     #     count += 1
#     # print(points[mid])
#
#
# if __name__ == '__main__':
#     # Check input file name exists
#     try:
#         filename = sys.argv[1]
#     except:
#         print("Usage: " + sys.argv[0] + " <inputfilename>")
#         sys.exit()
#
#     BuildKDTree2(filename)
