from gurobipy import *

def read(inputfile):
    f = open(inputfile, 'r') # Open .txt file
    line = f.readline() # Read the first line, returns string
    fields = str.split(line) # Split the line, returns list
    n = int(fields[0]) # Number of vertices in G
    m = int(fields[1]) # Number of edges in G
    adjLists = [] # Initialize adjacency list

    for i in range(0, n):
        adjLists.append([])

    # Fill adjacency list
    for line in f:
        fields = line.split(' ')
        i = int(fields[0])
        j = int(fields[1])
        adjLists[i].append(j)
        adjLists[j].append(i)
    f.close # Close .txt file once finished reading
    return n, m, adjLists


n, m, adjLists = read("../dat/jazz.graph.txt")


MWC_model = Model('MaxWeightClique')
MWC_model.Params.OutputFlag = 0
y = {}
for i in range(n):
    y[i] = MWC_model.addVar(vtype=GRB.BINARY, name="y_{}".format(i))

MWC_model.update()
MWC_model.modelSense = GRB.MAXIMIZE

for i in range(n):
    for j in range(i+1, n):
        if (j not in adjLists[i]):
            MWC_model.addConstr(y[i] + y[j] <= 1)


VP_model = Model('VertexPacking')
VP_model.Params.PreCrush = 1 # Allow user cuts
VP_model.Params.CliqueCuts = 0 # Prevent Gurobi from adding their clique cuts
VP_model.Params.Presolve = 0 #
x = {}
for i in range(n):
    x[i] = VP_model.addVar(vtype=GRB.BINARY, obj = 1, name="x_{}".format(i))

VP_model.update()
VP_model.modelSense = GRB.MAXIMIZE

for i in range(n):
    for j in adjLists[i]:
        if (i < j):
            VP_model.addConstr(x[i] + x[j] <= 1)


VP_model._x = x
VP_model._n = n
VP_model._MWC = MWC_model
VP_model._y = y

def CliqueCuts(VP_model, where):
    if (where == GRB.Callback.MIPNODE):
        status = VP_model.cbGet(GRB.Callback.MIPNODE_STATUS)
        if status == GRB.OPTIMAL:
            x_sol = VP_model.cbGetNodeRel(VP_model._x)
            for i in range(n):
                VP_model._y[i].Obj = x_sol[i]
            VP_model._MWC.optimize()
            print('Max weighted clique: {}'.format(MWC_model.objval))
            for i in range(n):
                if (y[i].x > 0.5):
                    print("{} ".format(i), end='')
            print("\n")
            if VP_model._MWC.objval > 1:
                VP_model.cbCut(quicksum(VP_model._x[i]*y[i].x for i in range(VP_model._n)) <= 1)

VP_model.optimize(CliqueCuts)
