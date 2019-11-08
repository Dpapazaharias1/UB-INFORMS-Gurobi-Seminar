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


n, m, adjLists = read("jazz.graph.txt")
# -------- Max Weighted Clique --------
MWC_model = Model('MaxWeightClique')
MWC_model.Params.OutputFlag = 0
y = {}

# -------- Vertex Packing Model --------
VP_model = Model('VertexPacking')
VP_model.Params.PreCrush = 1 # Allow user cuts
VP_model.Params.CliqueCuts = 0 # Prevent Gurobi from adding their clique cuts
VP_model.Params.Presolve = 0 #
x = {}

# Load data into the model

# ------- Separation Algorithm ------
def CliqueCuts(VP_model, where):
    pass

VP_model.optimize(CliqueCuts)
