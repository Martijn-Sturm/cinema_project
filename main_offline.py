from problem.problem import Offline


problem = Offline("input/offline_bnbChallenge.txt")
problem.cinema.find_solution(problem.groups.freq_dict)
# print(problem.cinema)
