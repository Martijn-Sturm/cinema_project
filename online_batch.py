from utils.test_file import generate_group_sequence
from algorithms.online import FirstFit, BestFit, WorstFit, MinCovidChairs, Hybrid_BF_CC
import pandas as pd

# import matplotlib.pyplot as plt
from os import listdir

FILEPATH = "input/online_input_big1.txt"
GROUPS_LIST = [generate_group_sequence(50) for i in range(100)]
FILE_DIR = "input/online"


def run_algorithm_with_original_groups(algorithm, filepath):
    alg = algorithm(filepath)
    cinema_result = alg.execute()
    return len(cinema_result.get_occupied_seats())


def repeat_algorithm_with_different_groups(algorithm, filepath, groups_list):
    results = []
    for groups in groups_list:
        alg = algorithm(filepath)
        alg.set_new_groups(groups)
        cinema_result = alg.execute()
        seats_occupied = len(cinema_result.get_occupied_seats())
        results.append(seats_occupied)
    return results


def get_file_names(directory):
    return [file for file in listdir(directory)]


# first_fit_result = repeat_algorithm_with_different_groups(
#     FirstFit, FILEPATH, GROUPS_LIST
# )
# best_fit_result = repeat_algorithm_with_different_groups(BestFit, FILEPATH, GROUPS_LIST)
# worst_fit_result = repeat_algorithm_with_different_groups(
#     WorstFit, FILEPATH, GROUPS_LIST
# )
# min_covid_chairs_result = repeat_algorithm_with_different_groups(
#     MinCovidChairs, FILEPATH, GROUPS_LIST
# )
# hybrid = repeat_algorithm_with_different_groups(Hybrid_BF_CC, FILEPATH, GROUPS_LIST)
# df = pd.DataFrame(
#     {
#         "first": first_fit_result,
#         "best": best_fit_result,
#         "worst": worst_fit_result,
#         "minCovid": min_covid_chairs_result,
#         "hybrid": hybrid,
#     }
# )

# df.describe()
# df.hist()
# plt.show()
# df.boxplot()
# plt.show()
