from utils.test_file import generate_group_sequence
from algorithms.online import FirstFit, BestFit, WorstFit, MinCovidChairs, Hybrid_BF_CC
import pandas as pd
import matplotlib.pyplot as plt

FILEPATH = "input/online_input_big1.txt"
groups_list = [generate_group_sequence(50) for i in range(100)]


def repeat_algorithm_with_different_groups(algorithm, filepath, groups_list):
    results = []
    for groups in groups_list:
        alg = algorithm(filepath)
        alg.set_new_groups(groups)
        cinema_result = alg.execute()
        seats_occupied = len(cinema_result.get_occupied_seats())
        results.append(seats_occupied)
    return results


first_fit_result = repeat_algorithm_with_different_groups(
    FirstFit, FILEPATH, groups_list
)
best_fit_result = repeat_algorithm_with_different_groups(BestFit, FILEPATH, groups_list)
worst_fit_result = repeat_algorithm_with_different_groups(
    WorstFit, FILEPATH, groups_list
)
min_covid_chairs_result = repeat_algorithm_with_different_groups(
    MinCovidChairs, FILEPATH, groups_list
)
hybrid = repeat_algorithm_with_different_groups(Hybrid_BF_CC, FILEPATH, groups_list)
df = pd.DataFrame(
    {
        "first": first_fit_result,
        "best": best_fit_result,
        "worst": worst_fit_result,
        "minCovid": min_covid_chairs_result,
        "hybrid": hybrid,
    }
)

df.describe()
df.hist()
plt.show()
df.boxplot()
plt.show()
