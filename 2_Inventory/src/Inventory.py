'''
# # Invetory Problem
#
# The main activity of a company in northern France is the production of drinking
# glasses.  It currently sells two different types of glasses (wine and martini
#glasses) that are produced in batches of 10 glasses. The company wishes to plan
#its production for the next 4 weeks.
'''



'''
# Sets
#
# We have two sets in this problem: drinking glasses and weeks.
'''

'''
#  Parameters
#
#
# ### Weekly demand
#
# Let parameter $d_{ij}$ represent the demand of glass $i$ during week $j$.
#
#
# The demand of wine and martini glasses in weeks one to four are:
#
#         |Week 1 | Week 2| Week 3| Week 4|
# |Wine   | 1000  |  500  | 300   | 4000  |
# |Martini| 2500  |  200  | 800   | 350   |
#
# **Note**: The number of glasses prouced per batch is 10. Since our demand is currently in units of glasses we need to translate it to batches.
#
# |       | Week 1| Week 2 | Week 3 | Week 4|
# |Wine   | 100   | 50     | 30     | 400   |
# |Martini| 250   | 20     | 80     | 35    |
'''




'''
# ### Initial and Final Stock
#
# Initially, we have 250 wine glasses (25 batches) and 100 (10 batches) of martini
# glasses in stock. At the end of week 4, there must be at least 1000 wine glasses
# (100 batches) and 600 martini glasses (60 batches) in stock.
#
# Let $I_{i0}$ represent the intial stock of glass $i$.
#
# Let $I_{if}$ represent the final required stock for glass $i$.
'''




'''
#  Production and Storage Parameters
#  Let:
#
# * $p_i$ represent the production cost of glass $i$
# * $s_i$ represent the storage cost of glass $i$
# * $q$   represent the required storage space per batch of glasses
# * $w_i$ represent the worker hours required to produce a batch of glass $i$
# * $m_i$ represent the machine hours required to produce a batch of glass $i$
# * $K_w$ represent the number of worker hours available in a week
# * $K_m$ represent the machine hour capacity per week
# * $K_s$ repersent the storage capacity in the stock room
'''




'''
# ## Decision Variables
#
# "Which quantities of the different glass types need to be produced in every
# period to minimize the total cost of production and storage?"
#
# We need to decide how many of each glass type to produce each week. Let,
#
# x_{ij} -  batches of glass i to produce in week j
#
# Not only do we need to decide how many batches of each type to produce each week but we also need to figure out how many batches of each glass type we need to store at the end of each week.
#
# Let
#
# I_{ij} - batches of glass i to store at the end of week j
'''




'''
# ## Objective Function
#
# Here we wish to minimize the total cost of production and storage.
'''




'''
# Constraints
#
# ### Personnel hour constraint
#
# _"The number of working hours of the personnel is limited to 1000 hours per week"_.
# Recall that each batch of wine and martini glasses require 2 and 1.5 personnel hours, respectively.
#
# So our model will contain a constraint for each week of the production planning period limiting the number of personnel hours.
#
#  2x_11 + 1.5x_21 <= 1000, j = 1
#  2x_12 + 1.5x_22 <= 1000, j = 2
#  2x_13 + 1.5x_23 <= 1000, j = 3
#  2x_14 + 1.5x_24 <= 1000, j = 4
#
# Which can be concisely written as:
# for j in Weeks:
#   quicksum( w_i x_ij <= K_w for i in Glasses)
#
# ### Machine hour constraint
#
# Likewise, we will have a constraint for the machine hours each week
#
# for j in Weeks:
#   quicksum( m_i x_ij <= K_m for i in Glasses)
#
#
# ### Stock storage constraint
#
# In addition, we will have a similar constraint based on I_{ij} to not exceed the storage capacity of the facility.
# for j in Weeks:
#   quicksum( q I_ij <= K_s for i in Glasses)
'''




'''
# ### Conservation of Glasses constraint
#
# The crucial constraint for the inventory problem is the conservation of stock.
#
# $$ I_{ij} = I_{ij-1} + x_{ij} - d_{ij} $$
#
# This constraint is crucial because it ensures that your remaining inventory for week $j$, $I_{ij}$, after satisfying demand $d_{ij}$, must either be from:
#
# 1. The inventory from last week $I_{i j-1}$
#
# 2. The batches you produced this week $x_{ij}$
#
#
# This constraint requires some care when coding as the initial stock $I_{i0}$ is a parameter and does not belong to our dictionary $I$.
'''




'''
#  Final stock constraint
#
# "The required final stock at the end of week four of both wine and martini
# glasses should be at least 1000 and 600 glasses, respectively"
#
# Lastly, we need to ensure that
#
# I_{i4} = I_{if}
#
# If we do not know the total number of weeks off the top of our head we can
# easily access it using the negative indexing of python.

 I[i, Weeks[-1]] == final_Inventory[i]
'''




'''
# ## Optimize the model
#
# Now that we have loaded
#
# * Sets
# * Parameters
# * Decision Variables
# * Constraints
# * Objective Function
#
# to our model, we can now tell Gurobi to optimize the model!
'''

# Print Solution
