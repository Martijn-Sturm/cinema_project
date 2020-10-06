from problem.problem import Offline, Onfline
import pickle

# f = open("/Users/clazinasteunenberg/Documents/GitHub/cinema_project/output/onfline.txt", "wb")
# dict = {}
for i in range(21):
    name = "Exact" + str(i + 1)
    Offline(name + ".txt")
# pickle.dump(dict, f)