from .entities.input import Input
from .entities.cinema import Cinema
from .entities.groups import OnlineGroups
from problem.offline_problem import Problem
from datetime import datetime


class Offline:
    def __init__(self, filepath) -> None:
        """
        Read the input file, create a Problem object then get the solution and print it.

        :param filepath: File name
        """
        file_input = Input(filepath, "offline")
        p = Problem(
            file_input.grid,
            file_input.groups,
            file_input.row_nr,
            file_input.column_nr,
            file_input.vips,
        )
        p.get_solution()
        p.output()


class Onfline:
    def __init__(self, filepath) -> None:
        """
        Read the input file, create a Problem object then get the solution and print it.

        :param filepath: File name
        """
        file_input = Input(filepath, "onfline")
        p = Problem(
            file_input.grid,
            file_input.groups,
            file_input.row_nr,
            file_input.column_nr,
            file_input.vips,
        )
        p.get_solution()
        p.output()
        self.result = p.model.objective.value()

    def __result__():
        return self.result


class Online:
    def __init__(self, filepath) -> None:
        # Read file
        file_input = Input(filepath, "online")

        # From file input, initialize cinema and groups object
        try:
            self.cinema = Cinema(
                file_input.grid, file_input.row_nr, file_input.column_nr
            )
            self.groups = OnlineGroups(file_input.groups)
        except Exception as err:
            raise type(err)(str(err), "filepath:", str(filepath))


class BalconyProblem:
    def __init__(self, filepath) -> None:
        """
        Read the input file. Then initialize some variables, find a solution and print it.

        :param filepath: File name
        """
        file_input = Input(filepath, "offline")
        self.rows = file_input.row_nr
        self.cols = file_input.column_nr
        self.grid = file_input.grid
        self.groups = file_input.groups
        self.vips = file_input.vips

        start = datetime.now()

        self.taken = 0
        self.check_for_balconies()

        print()
        print("Taken", self.taken)
        print("Time:", datetime.now() - start)

    def check_for_balconies(self):
        """
        Check if the grid has balconies. If so then solve the problem for each balcony.
        If not then solve the problem for the entire grid.
        """
        balcony = self.get_balconies()
        if len(balcony) == 0:
            p = Problem(self.grid, self.groups, self.rows, self.cols, self.vips)
            p.get_solution()
            self.output()
            self.taken = p.get_taken_seats()

        else:
            self.get_best_balcony(balcony, self.groups)

    def get_balconies(self):
        """
        Check if the grid contains balconies. If so return all the balconies.

        :return: List of Balconies
        """
        balcony_row = []
        begin = 0
        end = 0
        balcony = False
        for r in range(self.rows):
            c = 0
            while True:
                if self.grid[r][c] != 0:
                    break
                if self.cols - 1 == c:
                    if r != self.rows - 1:
                        if r != 0:
                            if begin != r:
                                balcony_row.append(Balcony(begin, r))
                                balcony = True
                        begin = r + 1
                        end = self.rows
                    else:
                        end = r
                    break
                c += 1
        if balcony and begin != end:
            balcony_row.append(Balcony(begin, end))
        return balcony_row

    def get_best_balcony(self, balcony, sizes):
        """
        With the remaining balconies get the balcony which can seed the most visitors.
        Update the grid and the list of group sizes with the solution for this balcony
        and find a solution for the remaining balconies.

        :param balcony: List of Balconies
        :param sizes: List of the group sizes
        """
        best_score = 0
        sol_balcony = None
        for i in balcony:
            grid_copy = [x[:] for x in self.grid[i.begin : i.end]]
            p = Problem(grid_copy, sizes.copy(), i.end - i.begin, self.cols, self.vips)
            p.get_solution()
            p.update_grid()
            p.update_group_sizes()
            grid = p.grid
            i.seats_taken = p.get_taken_seats()
            if i.seats_taken > best_score:
                i.sizes = p.number_of_groups
                i.grid = grid
                sol_balcony = i
                best_score = i.seats_taken
        self.update_grid(sol_balcony)
        self.remove_balcony(balcony, sol_balcony.begin)
        self.taken += best_score
        self.find_best_balcony(balcony, sol_balcony.sizes)

    @staticmethod
    def remove_balcony(bal_list, b):
        """
        Remove a balcony from the given list of balconies.

        :param bal_list: List of balconies
        :param b: First row of the balconies that needs to be removed from the list
        """
        for i, o in enumerate(bal_list):
            if o.begin == b:
                del bal_list[i]
                break

    def update_grid(self, part_of_grid):
        """
        Update the grid with the found solution for a balcony.

        :param part_of_grid: A balconies object containing the grid
        """
        index = 0
        for i in range(part_of_grid.begin, part_of_grid.end):
            self.grid[i] = part_of_grid.grid[index]
            index += 1

    def find_best_balcony(self, balcony, sizes):
        """
        Check how many balconies are left. If one is left find a solution for it and stop the recursion.
        If more than one is left recursively find a solution for all of them.

        :param balcony: List of balconies
        :param sizes: List of group sizes
        """
        if len(balcony) == 1:
            i = balcony[0]
            p = Problem(
                self.grid[i.begin : i.end], sizes, i.end - i.begin, self.cols, self.vips
            )
            p.get_solution()
            p.update_grid()
            p.update_group_sizes()
            grid = p.grid
            i.grid = grid
            self.update_grid(i)
            self.output()
            self.taken += p.get_taken_seats()
        else:
            self.get_best_balcony(balcony, sizes)

    def output(self):
        """Print the grid."""
        for r in range(self.rows):
            row = ""
            for c in range(self.cols):
                row += str(self.grid[r][c])
            print(row)


class Balcony:
    def __init__(self, b, e):
        """Initialize variables."""
        self.name = b
        self.begin = b
        self.end = e
        self.seats_taken = None
        self.sizes = None
        self.grid = None
