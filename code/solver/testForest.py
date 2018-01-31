import forest as ft
from master import MasterTree
from multiprocessing import Manager
from copy import deepcopy
import random as rd

# parameters
name = "tree_test4CPU"
frequency = 10
budget = 100

mydate = '20180108'

# ft.Forest.download_scenarios(mydate,latBound = [50-28, 50],lonBound = [-40 + 360, 360])
#
Weathers = ft.Forest.load_scenarios(mydate, latBound=[40, 50], lonBound=[360 - 15, 360])

# We create N simulators based on the scenarios
NUMBER_OF_SIM = 4  # <=20
SIM_TIME_STEP = 6  # in hours
STATE_INIT = [0, 47.5, -3.5 + 360]
N_DAYS_SIM = 8  # time horizon in days

sims = ft.Forest.create_simulators(Weathers, numberofsim=NUMBER_OF_SIM, simtimestep=SIM_TIME_STEP,
                                   stateinit=STATE_INIT, ndaysim=N_DAYS_SIM)

# initialize the simulators to get common destination and individual time min

missionheading = 235
ntra = 50

# destination, timemin = ft.Forest.initialize_simulators(sims, ntra, STATE_INIT, missionheading)
# print("destination : " + str(destination) + "  &  timemin : " + str(timemin) + "\n")
destination = [44.62224559323147, 350.9976771826662]
timemin = 5.2654198058866042

forest = ft.Forest(listsimulators=sims, destination=destination, timemin=timemin, budget=budget)
nodes = forest.launch_search(STATE_INIT, frequency)
print(type(nodes))
new_dict = dict()
for k, v in nodes.items():
    new_dict[k] = v.my_copy()

forest.master = MasterTree(sims, destination, nodes=new_dict)
print(len(forest.master.nodes))
for i in range(4):
    print(forest.master.nodes[hash(tuple([]))].rewards[i, 6].h)
# forest.master.get_children()

print(rd.choice(list(forest.master.nodes.values())).children)

forest.master.get_depth()
forest.master.get_best_policy()
forest.master.save_tree(name)
