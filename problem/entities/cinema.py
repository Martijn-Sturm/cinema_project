from tabulate import tabulate
from .utils import get_neighboors_from_grid, create_cinema_graph
from .positions import Seat, Spacer
from itertools import groupby
from operator import itemgetter
from collections import namedtuple


class Cinema:
    def __init__(self, grid, row_nr, column_nr):
        """Creates a cinema object that holds the grid with seatings, the neighbooring seatings, and the number of rows and columns.

        Args:
            grid (list(list)): A list with lists containing 0s for no seats, and 1s for seats: grid[row][column]
            row_nr (int): Number of rows in the cinema
            column_nr (int): Number of columns in the cinema
        """
        self.grid = grid  # list of lists
        self.row_nr = row_nr  # int
        self.column_nr = column_nr  # int
        self.seating_grid = self._init_seating_grid()
        self.seating_graph = self._init_seating_graph()

    def _init_seating_grid(self):
        """Initializes seating_grid which is the same as grid, but has objects populating the positions instead of 0s or 1s.

        Raises:
            ValueError: is raised if during initialization of the object, the grid argument contains any item other than integer 0 or 1

        Returns:
            list(list): List of list with objects
        """
        seating_grid = self.grid.copy()

        for row_nr, row in enumerate(self.grid):
            for column_nr, position in enumerate(row):
                if position == 1:
                    seating_grid[row_nr][column_nr] = Seat((row_nr, column_nr))
                elif position == 0:
                    seating_grid[row_nr][column_nr] = Spacer((row_nr, column_nr))
                else:
                    raise ValueError(
                        "invalid value found in grid: should be '0' or '1', but is",
                        position,
                    )

        return seating_grid

    def _init_seating_graph(self):
        """Initiates the seating graph, which is used to determine neighboors of each seat

        Returns:
            networkx.Graph: A graph with nodes representing Position objects (Seat or Spacer), and the edges denote the positions that are within Corona distance.
        """
        return create_cinema_graph(self.seating_grid)

    def __str__(self) -> str:
        print_grid = tabulate(self.seating_grid)
        return (
            # f"\nCinema with properties:\n\n"
            # f"Number of rows: {self.row_nr}\n"
            # f"Number of columns: {self.column_nr}\n"
            f"Seating grid: \n{print_grid}"
        )

    def get_position(self, coordinates):
        return self.seating_grid[coordinates[0]][coordinates[1]]

    def copy_grid(self):
        """Make a copy of the grid."""
        new_grid = []
        for r in range(self.row_nr):
            new_row = []
            for c in range(self.column_nr):
                new_row.append(self.seating_grid[r][c].copy())
            new_grid.append(new_row)
        return new_grid

    @staticmethod
    def update_group_size_list(size, freq_dict):
        """Lower the quantity of a group size."""
        d = freq_dict.copy()
        d[size] = d[size] - 1
        return d

    @staticmethod
    def get_all_group_sizes_list(groups_list):
        """Generates a list of all the sizes

        Args:
            groups_list: dict of the groups as keys and the quantity as value
        Returns:
            group_sizes: list of all the unique group sizes
        """
        group_sizes = []
        for group, quantity in groups_list.items():
            if quantity > 0:
                group_sizes.append(group)
        return group_sizes

    def find_solution(self, list_of_sizes):
        # print("begin")
        vistided_states = 0
        queue = self.branch(list_of_sizes, 0, 0)
        # for i in queue:
        #    print(i.coord_node, i.size_group)
        best_grid = self.seating_grid
        best_score = 0
        taken_free_seats = {}

        while len(queue) != 0:
            q = queue.pop(0)
            vistided_states += 1
            new_graph = create_cinema_graph(q.grid)
            self.seating_graph = new_graph
            self.seating_grid = q.grid

            self.place_group(q.coord_node, q.size_group)
            new_freq_dict = self.update_group_size_list(q.size_group, q.list_of_groups)

            taken_seats = q.nr_taken + q.size_group
            free_seats = self.get_number_of_eligible_seats()
            new_queue = []

            if taken_seats in taken_free_seats:
                # print(q.coord_node, q.size_group, "second_2")
                # print(str(self))
                if free_seats >= taken_free_seats[taken_seats]:
                    taken_free_seats[taken_seats] = free_seats
                    new_queue = self.branch(new_freq_dict, taken_seats, free_seats)

                    # print(q.coord_node, q.size_group, "second_time_lower_equal_3")
            else:
                taken_free_seats[taken_seats] = free_seats
                new_queue = self.branch(new_freq_dict, taken_seats, free_seats)
                # print(q.coord_node, q.size_group, "first_time_1")
                # print(str(self))

                if best_score < taken_seats:
                    best_score = taken_seats
                    # print("bs", best_score)
                    best_grid = self.copy_grid()
            queue += new_queue

        self.seating_grid = best_grid
        print("Result")
        print("Visited states:", vistided_states)
        print(str(self))

    def branch(self, list_of_sizes, taken, nr_eligible):
        """Get nodes to expand on"""
        possible_places = self.get_possible_places_for_all_groups(list_of_sizes)
        node_list = []

        for k, v in possible_places.items():
            if len(v) == 0:
                list_of_sizes = self.update_group_size_list(k, list_of_sizes)
                continue
            for coord in v:
                if self.bound_redundency(coord, v, k):
                    node_list.append(Node(coord, k, self.copy_grid(), list_of_sizes, taken, nr_eligible))
        return node_list

    def bound_redundency(self, coord, values, size):
        if coord[0] == 1 and (0, coord[1]) in values:
            return False
        if coord[0] == self.row_nr - 2 and (self.row_nr-1, coord[1]) in values:
            return False
        if coord[1] == 1 and (coord[0], 0) in values:
            return False
        if coord[1] == self.column_nr-1-size and (coord[0], self.column_nr-size) in values:
            return False
        return True

    def get_possible_places_for_all_groups(self, list_of_sizes):
        """Get all the possible places for each group."""
        group_sizes = self.get_all_group_sizes_list(list_of_sizes)  # list of all the group sizes
        # group_sizes.sort(reverse=True)
        possible_sizes = self.get_placement_possibilities()
        possiblities_groups = {}
        # print("sizes", possible_sizes)

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
                    for i in range(1, possiblility.size - g + 1):
                        c = possiblility.coordinates
                        group_places.append((c[0], c[1] + i))
            possiblities_groups[g] = group_places
        return possiblities_groups

    @staticmethod
    def print_score_grid(grid):
        """Print the scores of the grid."""
        score_grid = []
        for r in grid:
            row = []
            for c in r:
                row.append(c.score)
            score_grid.append(row)
        print(tabulate(score_grid))

    def get_number_of_eligible_seats(self):
        """Get the number of still eligible seats

        Returns:
            int: number of free seats
        """
        # scan through grid for eligible seats
        eligible = 0
        for row in self.seating_grid:
            for position in row:
                try:
                    if position.eligible:
                        eligible += 1
                except AttributeError:
                    if isinstance(position, Spacer):
                        pass
                    else:
                        raise
        return eligible

    def get_neighboors_from_coordinates(self, coordinates):
        """Generates a list with all neighboors for given coordinates

        Args:
            coordinates (tuple(int, int)): (row, column)

        Returns:
            list(position objects): every position that is neighbooring to the inputted coordinates. Excluding the input position
        """
        position = self.get_position(coordinates)
        return self.get_neighboors_from_position(position)

    def get_neighboors_from_position(self, position):
        """Generates a list with all neighboors for given position

        Args:
            position (tuple(int, int)): tuple(row, column)

        Returns:
            list(position objects): every position that is neighbooring to the inputted coordinates. Excluding the input position
        """
        position_container = self.seating_graph[position]
        return [position for position in position_container]

    def get_eligible_neighboors_from_position(self, position):
        all_neighboors = self.get_neighboors_from_position(position)

        eligible_positions = []
        for position in all_neighboors:
            try:
                is_position_eligible = position.eligible
            except AttributeError:
                if isinstance(position, Spacer):
                    continue
                else:
                    raise
            if is_position_eligible:
                eligible_positions.append(position)

        return eligible_positions

    def get_placement_position_coordinates(self):
        """Generates a list with tuples containing the coordinates of still eligible seats

        Returns:
            list(tuple): tuple(row, column)
        """
        # scan through grid for eligible seats
        eligible_coordinates = []
        for row in self.seating_grid:
            for position in row:
                try:
                    if position.eligible:
                        eligible_coordinates.append(position.get_coordinates())
                except AttributeError:
                    if isinstance(position, Spacer):
                        pass
                    else:
                        raise
        return eligible_coordinates

    def get_placement_possibilities(self):
        """Returns a list with dictionaries in which as keys the max group size that can be placed for that item, and as value the position coordinates of the lefter seat of that item.

        Returns:
            list(dict): dict(number_of_uninterrupted_seats: position_most_lefter_seat(row, column))
        """
        coord_list = self.get_placement_position_coordinates()

        result = []
        for row in groupby(coord_list, lambda x: x[0]):  # Group by row
            coords = list(row[1])
            row_number = coords[0][0]
            col_numbers_sorted = sorted([coord[1] for coord in coords])

            # Creates a seperate list of each uninterrupted seats next to each other that are available -> single placement possibility
            series_list = [
                list(map(itemgetter(1), g))
                for k, g in groupby(
                    enumerate(col_numbers_sorted), lambda x: x[0] - x[1]
                )
            ]
            # For each of this placement possibility, return a dict item with as key the number of seats in that possibility, and as value the most lefter seat belonging to that possibility
            for serie in series_list:
                result.append(PlacementPossibility(len(serie), (row_number, serie[0])))

        return result

    def place_group(self, coordinates, size, group_id=None):
        """Occupies the places in the seating grid

        Args:
            coordinates (tuple(int, int)): first int denotes row, second int denotes lefter occupied seat
            size (int): number of seats that will be taken
            group_id (?, optional): Group id, to later determine which group occupies these seats. Defaults to None.
        """
        # Gather position objects
        positions = []
        for n in range(size):
            row = int(coordinates[0])
            column = int(coordinates[1]) + n
            positions.append(self.get_position((row, column)))
        self.occupy_seats(positions, group_id)

        # Gather all neighboors for position objects
        eligible_neighboors = []
        for position in positions:
            eligible_neighboors = (
                eligible_neighboors
                + self.get_eligible_neighboors_from_position(position)
            )
        # Remove duplicates
        eligible_neighboors = set(eligible_neighboors)

        # Make neighbooring seats unavailble
        self.make_seats_unavailable(eligible_neighboors)

    @staticmethod
    def occupy_seats(position_list: list, group_id=None):
        """Occupies seats for positions in input

        Args:
            position_list (list): A list with position objects to be set to occupied
            group_id (?, optional): Group id, to later determine which group occupies these seats. Defaults to None.

        Raises:
            Exception: If seat that will be occupied is not eligible
            Exception: If position that will be occupied is a spacer instead of a seat
        """
        for position in position_list:
            try:
                if not position.eligible:
                    raise Exception(
                        "Position that is trying to be occupied is not eligible:",
                        position.get_coordinates(),
                    )
                position.occupy_seat(group_id)
            except AttributeError:
                raise Exception(
                    "Position that is tried to be occupied is no Seat, but a Spacer. Coordinates:",
                    position.get_coordinates(),
                )

    @staticmethod
    def make_seats_unavailable(position_list):
        """Sets the seats to unavailable

        Args:
            position_list (list): list with position objects to be set to unavailable

        """
        for position in position_list:
            try:
                position.make_seat_unavailable()
            # A spacer can be ignored
            except AttributeError:
                if isinstance(position, Spacer):
                    continue
                else:
                    raise


class Node:
    def __init__(self, coordinate, group, grid, lg, t, e):
        self.coord_node = coordinate
        self.size_group = group
        self.grid = grid
        self.list_of_groups = lg
        self.nr_taken = t
        self.nr_eligible = e

    def __str__(self) -> str:
        return f"Score: {self.nr_taken}, Coords: {self.coord_node}, Size: {self.size_group}"


PlacementPossibility = namedtuple("PlacementPossibility", ["size", "coordinates"])

