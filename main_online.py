from algorithms.online import OnlineAlgorithm

online = OnlineAlgorithm("input/online_input_big1.txt")
vacant = online.get_total_seats()
filled = online.run_naive1("naive_run1")
print(f"places filled is: {filled}, from total {vacant} places")

