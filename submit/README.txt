main.py

Cody Dhein
Val Chapple
CS325 - Fall 2017
Group 1

USAGE
********************************
main.py requires Python 2.7

Usage:
  python2.7 ./main.py <filename>

Example:
  python2.7 ./main.py ./tsp_example_1.txt


FOLDER CONTENTS
********************************
* best_unlimited_results
  - contains  solutions to unlimited time for all 10 instances
  - instances less than 1000 were computed with MST.
  - instances greater than or equal to 1000 were computed with kd-tree 2-Opt.
* main_results
  - contains solutions for 3-minute time limit, from program main.py on flip2
  - instances less than 500 were computed with MST.
  - instances greater than or equal to 500 were computed with kd-tree no opt.
* MST
  - contains python files for the MST route building and optimization
* NN_KDTREE
  - contains a python file for the kd-tree route building and optimization
* util
  - contains a python file for the utilities implemented with MST
