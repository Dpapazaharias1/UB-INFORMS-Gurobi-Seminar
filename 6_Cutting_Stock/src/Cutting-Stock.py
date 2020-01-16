from gurobipy import *
import math

def read(inputfile):
        f = open(inputfile, 'r')
        line = f.readline()
        fields = str.split(line)
        m = int(fields[0])
        W = int(fields[1])
        width = []
        demand = []
        for line in f:
            fields = line.split(' ')
            s = int(fields[0])
            d = int(fields[1])
            width.append(s)
            demand.append(d)

        f.close
        return m, W, width, demand


m, W, width, demand =  read("../dat/CSP.txt")

master = Model('Cutting-Stock')
n = m
x = {}
for i in range(n):
    x[i] = master.addVar(vtype=GRB.CONTINUOUS, obj = 1, name="x_{}".format(i))
master.setParam("OutputFlag", 0)
master.update()
master.modelSense = GRB.MINIMIZE

orders = {} # Place Constraints in dictionary
pi = [] # Dual Values
for j in range(m):
    pi.append(0)
    orders[j] = master.addConstr(math.floor(W/float(width[j]))*x[j]  >= demand[j])


def printMasterSol(master, x, n, m):
    print("-----------")
    print("Iteration: {}".format(n - m))
    print("-----------")
    print("Rolls used: {}".format(master.objval))
    for i in range(n):
        if x[i].X > 0:
            print("{} = {}".format(x[i].VarName, x[i].x))
    print("-----------")

def printDualSol(subproblem, y, m):
    print("New column found with reduced cost {}".format(1 - subproblem.objval))
    for j in range(m):
        if y[j].X > 0:
            print("{} rolls of item {}".format(y[j].X, j))



subproblem = Model("Knapsack")
y = {}
for j in range(m):
    y[j] = subproblem.addVar(vtype=GRB.INTEGER, name="y_{}".format(j))

subproblem.setParam("OutputFlag", 0)
subproblem.modelSense = GRB.MAXIMIZE
subproblem.addConstr(quicksum(width[j]*y[j] for j in range(m)) <= W)
subproblem.update()

master.optimize()
printMasterSol(master, x, n, m)

for j in range(m):
    print(orders[j].Pi)
    y[j].Obj = orders[j].Pi

subproblem.optimize()
printDualSol(subproblem, y, m)

while(subproblem.objval > 1):
    printDualSol(subproblem, y, m)
    
    x[n] = master.addVar(vtype=GRB.CONTINUOUS, obj = 1, name="x_{}".format(n))
    master.update()
    
    for i in range(m):
        if y[i].x > 0.1:
            master.chgCoeff(orders[i], x[n], y[i].x)
    
    master.optimize()
    n += 1
    printMasterSol(master, x, n, m)
    
    for i in range(m):
        y[i].Obj = orders[i].Pi
    
    subproblem.optimize()

master.setParam("OutputFlag", 1)
for i in range(n):
    x[i].vtype = GRB.INTEGER
master.update()
master.optimize()