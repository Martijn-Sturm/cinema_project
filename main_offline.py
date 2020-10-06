from problem.problem import Offline, Onfline
import pickle

for i in range(21):
    name = "Exact" + str(i + 1)
    Offline("/Users/clazinasteunenberg/Documents/GitHub/cinema_project/input/" + name + ".txt")