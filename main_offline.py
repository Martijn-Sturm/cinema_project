from problem.problem import Offline


problem = Offline("input/test_input.txt")
problem.cinema.set_score_of_walls()
# problem.cinema.print_score_grid()
problem.cinema.find_solution(problem.groups.freq_dict)
print(problem.cinema)

"""
def brach(nodes):
    if node       
        node = get_max_score(node_list)
        problem.cinema.place_group(node.coord_node, node.size_group)
        total_score += node.score_node
        update_group_size_list(node.size_group)
        new_group_list = problem.groups.get_all_group_sizes_list()
        find_solution(new_group_list)
        # print(problem.cinema)
    return
"""

"""
max = max([n.score_node for n in node_list])
for n in node_list:
    if n.score_node == max:
        print(n.coord_node, n.size_group, n.score_node)
"""


"""
group_sizes = problem.groups.group_sizes  # list of all the group sizes
# print(group_sizes)
# group_sizes.sort(reverse=True)
possible_sizes = problem.cinema.get_placement_possibilities()
possiblities_groups = []

for g in group_sizes:
    group_places = []
    for possiblility in possible_sizes:
        if g > possiblility.size:
            continue
        if g == possiblility.size:
            group_places.append(possiblility.coordinates)
            continue
        if g < possiblility.size:
            group_places.append(possiblility.coordinates)
            for i in range(1, possiblility.size-g+1):
                c = possiblility.coordinates
                group_places.append((c[0], c[1]+i))
    possiblities_groups.append(group_places)
print(possiblities_groups)

"""
# problem.cinema.place_group(possiblility.coordinates, g, "group_id_test")
# possible_sizes = problem.cinema.get_placement_possibilities()
"""
problem.cinema.place_group((2,0), 4, "group_id_test")
problem.cinema.place_group((0,1), 2, "group_id_test")
problem.cinema.place_group((0,7), 2, "group_id_test")
problem.cinema.place_group((2,7), 2, "group_id_test")
problem.cinema.place_group((4,0), 2, "group_id_test")
problem.cinema.place_group((5,3), 1, "group_id_test")
problem.cinema.place_group((5,8), 1, "group_id_test")
problem.cinema.place_group((4,5), 1, "group_id_test")
problem.cinema.place_group((1,5), 1, "group_id_test")
print(problem.cinema)
"""
"""
# get list all group sizes
group_sizes = []
for group in problem.groups.freq_dict:
    for i in range(problem.groups.freq_dict[group]):
        group_sizes.append(group)
"""
"""
for i in list(problem.cinema.seating_graph.nodes):
    problem.cinema.seating_graph.nodes[i]['score'] = 0
nx.draw(problem.cinema.seating_graph, with_labels=True)
plt.draw()
plt.show()
"""
"""
nodes = list(problem.cinema.seating_graph.nodes)[0]
print("nodes", nodes)
problem.cinema.seating_graph.nodes[nodes]['score'] = 5
print(problem.cinema.seating_graph.nodes[nodes]['score'])
score = 0  # number of seated people
group_sizes = problem.groups.group_sizes  # list of all the group sizes
group_sizes.sort(reverse=True)
print("gorop_size", group_sizes)

possible_sizes = problem.cinema.get_placement_possibilities()
print(possible_sizes)
for g in group_sizes:
    for possiblility in possible_sizes:
        if g > possiblility.size:
            # print(g, possiblility, "no")
            continue
        if g == possiblility.size:
            # print("value", possiblility, "size_group: ", g)
            problem.cinema.place_group(possiblility.coordinates, g, "group_id_test")
            # print("after", problem.cinema)
            possible_sizes = problem.cinema.get_placement_possibilities()
            break
        # if g < possiblility.size:


"""
"""
print(problem.cinema)

problem.cinema.place_group((1, 0), 2, "group_id_test")
print(problem.cinema)

neighboors_01 = problem.cinema.get_neighboors_from_coordinates((0, 1))

print("\nNeighboors from (0,1)", neighboors_01)

print("\nSame with coordinates:")
for neighb in neighboors_01:
    print(neighb, neighb.get_coordinates())


"""
