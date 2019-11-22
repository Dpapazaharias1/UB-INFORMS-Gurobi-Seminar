from gurobipy import *
from math import sqrt
import matplotlib.pyplot as plt

def read(inputfile):
    f = open(inputfile, 'r')
    line = f.readline()
    fields = str.split(line)
    n = int(fields[0])
    
    location = [[] for i in range(n)] # initialize a list of coordinates for each city
    
    i = 0
    for line in f:
        fields = line.split('\t')
        loc_x = float(fields[0])
        loc_y = float(fields[1])
        location[i] = (loc_x, loc_y)
        i += 1
    f.close
    
    return location

def calcDistance(location):
    n = len(location) # number of nodes
    distance = [[0 for j in range (n)] for i in range(n)] # initialize arc costs
    for i in range(n):
        for j in range(i,n):
            if i < j:
                x_dist = (location[i][0] - location[j][0])**2
                y_dist = (location[i][1] - location[j][1])**2
                dist = sqrt(x_dist + y_dist)
                distance[i][j] = dist
                distance[j][i] = dist
    
    return distance

# Parameters

inputfile = '../dat/TSP_instance_n_50_s_0.dat'
location = read(inputfile) # location of each city
n = len(location) # number of cities 
distance = calcDistance(location) # arc costs

# Build Model

TSP = Model('TSP')

# Model Parameters

# Subtour Elimination Callback

def subtourelim(model, where):
    pass
            
TSP.optimize(subtourelim)

def plotSolution(x_sol, location):
    coord_x = [v[0] for v in location]
    coord_y = [v[1] for v in location]
    Arcs = []
    plt.clf()
    for i, j in x_sol.keys():
        if x_sol[i, j].X > 0.5:
            plt.plot([coord_x[i], coord_x[j]], [coord_y[i], coord_y[j]], color='b', alpha=0.4,zorder=0)
    plt.scatter(x=coord_x, y=coord_y, color='r', zorder=1)
    for i in range(len(location)):
        plt.annotate(i, (coord_x[i]+0.25,coord_y[i]+0.25))
    plt.xlim((0,22))
    plt.ylim((0,22))
    plt.show()

plotSolution(x, location)