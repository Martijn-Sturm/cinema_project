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
            f"\nCinema with properties:\n\n"
            f"Number of rows: {self.row_nr}\n"
            f"Number of columns: {self.column_nr}\n"
            f"Seating grid: \n{print_grid}"
        )

    def get_position(self, coordinates):
        return self.seating_grid[coordinates[0]][coordinates[1]]

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


PlacementPossibility = namedtuple("PlacementPossibility", ["size", "coordinates"])

