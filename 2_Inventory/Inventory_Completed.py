
# Invetory Problem
#
# The main activity of a company in northern France is the production of drinking glasses.
# It currently sells two different types of glasses (wine and martini glasses) that are produced in batches of 10 glasses.
# The company wishes to plan its production for the next 4 weeks.


from gurobipy import *

model = Model('glasses_LP')

# Sets: Glasses, Weeks

Glasses = [0, 1] # 0 - wine, 1 - martini
Weeks = [0, 1, 2, 3]

# Parameters

demand = [[100, 50, 30, 400], [250, 20, 80, 35]]

initial_Inventory = [25, 10]
final_Inventory = [100, 60]

p = [15, 20]
s = [8 , 12]
q = 20
w = [2, 1.5]
m = [5, 3]
K_w = 800
K_m = 1400
K_s = 6000

# Decision Variables

x = {} # Initialize a dictionary for x_ij
I = {} # Initialize a dictionary for I_ij

for i in Glasses:
    for j in Weeks:
        x[i,j] = model.addVar(vtype = GRB.CONTINUOUS, name = 'produce_{0}_{1}'.format(i,j))
        I[i,j] = model.addVar(vtype = GRB.CONTINUOUS, name = 'store_{0}_{1}'.format(i,j))

model.update()

# Objective Function

model.setObjective(quicksum(p[i]*x[i,j] + s[i]*I[i,j] for i in Glasses for j in Weeks), GRB.MINIMIZE)

# Constraints

for j in Weeks:
    model.addConstr( quicksum(w[i]*x[i,j] for i in Glasses) <= K_w, name='personnel_{}'.format(j))
    model.addConstr( quicksum(m[i]*x[i,j] for i in Glasses) <= K_m, name='machine_{}'.format(j))
    model.addConstr( quicksum(q*I[i,j] for i in Glasses) <= K_s, name='storage_{}'.format(j))

for i in Glasses:
    for j in Weeks:
        if j == 0:
            model.addConstr(I[i,j] == initial_Inventory[i] + x[i,j] - demand[i][j], name='stock_0')
        else:
            model.addConstr(I[i,j] == I[i,j-1] + x[i,j] - demand[i][j], name='stock_{}'.format(j))


for i in Glasses:
    model.addConstr( I[i, Weeks[-1]] == final_Inventory[i], name = 'final_inv_{}'.format(i))

# Optimize

model.optimize()

# Print Solution

print("Objective Value: {}".format(model.objVal))
for j in Weeks:
    print("Week {}: Produce {} Wine {} Martini".format(j+1, x[0,j].X, x[1,j].X))
    print("Week {}: Store   {} Wine {} Martini".format(j+1, I[0,j].X, I[1,j].X))
