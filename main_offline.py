from problem.problem import Offline

problem = Offline("/Users/clazinasteunenberg/Documents/GitHub/cinema_project/input/offline_challengingInput.txt")
print(problem.cinema)

neighboors_01 = problem.cinema.get_neighboors_from_coordinates((0, 1))

print("\nNeighboors from (0,1)", neighboors_01)

print("\nSame with coordinates:")
for neighb in neighboors_01:
    print(neighb, neighb.get_coordinates())
