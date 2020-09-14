from problem.problem import Offline

problem = Offline("input/test_input.txt")
print(problem.cinema)

problem.cinema.place_group((1, 0), 2, "group_id_test")
print(problem.cinema)

neighboors_01 = problem.cinema.get_neighboors_from_coordinates((0, 1))

print("\nNeighboors from (0,1)", neighboors_01)

print("\nSame with coordinates:")
for neighb in neighboors_01:
    print(neighb, neighb.get_coordinates())
