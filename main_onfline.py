from problem.problem import Offline, Onfline
import pickle

dict = {}
for i in range(7):
    name = "Online" + str(i + 1)
    dict[name] = Onfline("/Users/clazinasteunenberg/Documents/GitHub/cinema_project/input/" + name + ".txt").result
pickle.dump(dict, open("/Users/clazinasteunenberg/Documents/GitHub/cinema_project/output/onfline.txt", "wb"))