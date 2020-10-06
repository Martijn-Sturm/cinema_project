from problem.problem import Offline, Onfline
import pickle
f = open("/Users/clazinasteunenberg/Documents/GitHub/cinema_project/output/onfline.txt", "wb")
dict = {}
for i in range(7):
    name = "Online" + str(i + 1)
    dict[name] = Onfline(name + ".txt").result
pickle.dump(dict, f)