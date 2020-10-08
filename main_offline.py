from problem.problem import Offline


problem = Offline("input/offline_antiGreedyInput.txt")
problem.cinema.find_solution(problem.groups.freq_dict)
