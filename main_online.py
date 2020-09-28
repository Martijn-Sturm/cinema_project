from algorithms.online import FirstFit, BestFit, WorstFit, MinCovidChairs
from utils.test_file import generate_group_sequence

first_fit = FirstFit("input/online_input_big1.txt")
first_fit.execute("firstfit1")


best_fit = BestFit("input/online_input_big1.txt")
best_fit.execute("bestfit1")


worst_fit = WorstFit("input/online_input_big1.txt")
worst_fit.execute("worstfit1")

min_covid_chairs = MinCovidChairs("input/online_input_big1.txt")
min_covid_chairs.execute("mincovidchairs1")


new_groups = generate_group_sequence(50)
