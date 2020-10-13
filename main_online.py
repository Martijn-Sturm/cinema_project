from algorithms.online import FirstFit, BestFit, WorstFit, MinCovidChairs, Hybrid_BF_CC
from utils.test_file import generate_group_sequence

FILE = "input/online/Online5.txt"
LOG = "test"

best_fit = BestFit(FILE)
best_fit.execute(f"{LOG}/bestfit")

first_fit = FirstFit(FILE)
first_fit.execute(f"{LOG}/firstfit")

worst_fit = WorstFit(FILE)
worst_fit.execute(f"{LOG}/worstfit")

min_covid_chairs = MinCovidChairs(FILE)
min_covid_chairs.execute(f"{LOG}/mincovidchairs")

# hybrid_fit = Hybrid_BF_CC(FILE)
# hybrid_fit.execute(f"{LOG}/hybrid_fit")

# new_groups = generate_group_sequence(50)
