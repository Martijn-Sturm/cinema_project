from utils.test_file import generate_group_sequence
from multiprocessing import Pool, cpu_count
from joblib import Parallel, delayed

# from algorithms.online import FirstFit, BestFit, WorstFit, MinCovidChairs, Hybrid_BF_CC
import pandas as pd

# import matplotlib.pyplot as plt
from os import listdir

# FILEPATH = "input/online_input_big1.txt"
# GROUPS_LIST = [generate_group_sequence(50) for i in range(100)]
# FILE_DIR = "input/online"


def run_algorithm_with_original_groups(algorithm, filepath):
    alg = algorithm(filepath)
    cinema_result = alg.execute()
    return len(cinema_result.get_occupied_seats())


def repeat_algorithm_with_different_groups(algorithm, filepath, groups_list):
    results = Parallel(n_jobs=10)(
        delayed(do_for_different_group)(algorithm, filepath, group)
        for group in groups_list
    )
    return results


def do_for_different_group(algorithm, filepath, groups):
    alg = algorithm(filepath)
    alg.set_new_groups(groups)
    cinema_result = alg.execute()
    seats_occupied = len(cinema_result.get_occupied_seats())
    return seats_occupied


def get_file_names(directory):
    return [file for file in listdir(directory)]

