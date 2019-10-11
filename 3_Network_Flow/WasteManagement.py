#!/usr/bin/env python
# coding: utf-8

# # Waste Management
# 
# A company in the southwest of France needs to transport 180 tons of chemical products stored in four depots D1 to D4 to three recycling centers C1, C2, and C3. The depots D1 to D4 currently store respectively 50, 30, 35, and 65 tons of product and the recycling centers require 30, 65 and 85 tons, respectively. Two transportation modes are available: road and rail. Depot D1 only delivers to centers C1 and C2 by road at a cost of $\$12,000$ per ton and $\$11,000$ per ton, respectively; Depot D2 can deliver to C2, by road at a cost of $\$9,000$ per ton and to C3 by rail or road for $\$4,000$ per ton and $\$5,000$ per ton, respectively; depot D3 delivers to center C1 by road at a cost of $\$7,000$ ton and to C3 by rail or road for $\$9,000$ per ton or $\$9,500$ per ton, respectively; depot D4 delivers to center C2 by rail or road at a cost of $\$11,000$ ton and $\$14,000$ ton, and to C3 by rail or road for $\$10,000$ per ton and $\$14,000$ per ton, respectively.
# 
# Currently, a contract with the train transporter requires the company to transport at least 10 tons and at most 50 tons for any single delivery between the depots and centers for which the train service is available.
# In other words, wherever there is a rail service, between a depot and a center, the company must send at least 10 tons via that service. **How should the company transport the 180 tons of chemicals to minimize the total transportation cost?**
# 
# ## Modelling Tricks
# 
# ### Issue
# 
# Some depots have the option to deliver to centers by road or rail. How can we differentiate these arcs?
# 
# 
# 
# <div>
# <img src="railroad.png" width="500"/>
# </div>
# 
# ### Solution
# 
# 
# Create two artificial intermediate nodes ($b_i=0$), one for road and one for rail. The arcs from $C^{rail}_i$ to $C_i$ will have parameters $(c^{rail}_{ii},\ell^{rail}_{ii},u^{rail}_{ii}) = (0, 0, \infty)$. Likewise, for $C^{road}_i$, $(c^{road}_{ii},\ell^{road}_{ii},u^{road}_{ii}) = (0, 0, \infty)$
# 
# <div>
# <img src="splitnodes.png" width="500"/>
# </div>
# 
# We will say that $C_i^r$ will represent shipment by road and $C_i^\ell$ represents shipment by rail.
# 
# ## The Network
# 
# 
# <div>
# <img src="network.png" width="600"/>
# </div>
# 
# 
# 

# In[ ]:


from gurobipy import *


# ## Multidict
# 
# This function splits a single dictionary into multiple dictionaries. The input dictionary should map each key to a list of n values. The function returns a list of the shared keys as its first result, followed by the n individual Gurobi tuple dictionaries (stored as tupledict objects).
# 
# 
# ### Arguments
# 
# **data**: A Python dictionary. Each key should map to a list of values.
# 
# ### Return value
# 
# A list, where the first member contains the shared key values, and the following members contain the dictionaries that result from splitting the value lists from the input dictionary.
# 
# ### Example
# 
# ```Python
# keys, dict1, dict2 = multidict( {
#     'key1': [1, 2],
#     'key2': [1, 3],
#     'key3': [1, 4] } )```
# 
# Returns
# 
# ```Python 
# keys = ['key1', 'key2', 'key3']
# dict1 = {'key1':1, 'key2':1, 'key3':1}
# dict2 = {'key1':2, 'key2':3, 'key3':4}
# ```
# 
# Usally we use multidict to specify a set i.e Nodes and Arcs, and define all the parameters associate with that set all in one function

# In[ ]:


Nodes, Supply= multidict({
'D1': 50,
'D2': 30,
'D3': 35,
'D4': 65,
'C1r': 0,
'C1l': 0,
'C2r': 0,
'C2l': 0,
'C3r': 0,
'C3l': 0,
'C1':-30,
'C2':-65,
'C3':-85
})


# In[ ]:


Arcs, cost, lb, ub = multidict({
('C1r','C1'): [0,0,100],
('C1l','C1'): [0,0,120],
('C2r','C2'): [0,0,120],
('C2l','C2'): [0,0,120],
('C3r','C3'): [0,0,120],
('C3l','C3'): [0,0,120],
('D1','C1r'): [12,0,100],
('D1','C2r'): [11,0,100],
('D2','C2r'): [9,0,100],
('D2','C3r'): [5,0,100],
('D2','C3l'): [4,10,50],
('D3','C1r'): [7,0,100],
('D3','C3r'): [9.5,0,100],
('D3','C3l'): [9,10,50],
('D4','C2r'): [14,0,100],
('D4','C3r'): [14,0,100],
('D4','C2l'): [11,10,50],
('D4','C3l'): [10,10,50],
})


# In[ ]:


Arcs = tuplelist(Arcs)


# In[ ]:


def minCostFlow(Nodes, Arcs, Supply, cost, lb, ub):
    pass


# In[ ]:


minCostFlow(Nodes,Arcs,Supply, cost, lb, ub)

