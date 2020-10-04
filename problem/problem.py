from .entities.input import Input
from .entities.cinema import Cinema
from .entities.groups import OnlineGroups
from problem.offline_problem import Problem
from datetime import datetime


class Offline:
    def __init__(self, filepath) -> None:
        # Read file
        file_input = Input(filepath, "offline")
        self.rows = file_input.row_nr
        self.cols = file_input.column_nr
        self.grid = file_input.grid
        self.groups = file_input.groups

        start = datetime.now()

        self.taken = 0
        self.check_for_balconies()
        """
        p = Problem(self.grid, self.groups, self.rows, self.cols)
        grid = p.get_solution()
        self.output(grid, self.rows, self.cols)
        self.taken = p.get_taken_seats()
        p.output()
        """
        print()
        print("Taken", self.taken)
        print("Time:", datetime.now() - start)

    def check_for_balconies(self):
        balcony = self.get_balconies()
        if len(balcony) == 0:
            p = Problem(self.grid, self.groups, self.rows, self.cols)
            p.get_solution()
            self.output()
            self.taken = p.get_taken_seats()
            p.output()
        else:
            self.get_best_balcony(balcony, self.groups)

    def output(self):
        for r in range(self.rows):
            row = ""
            for c in range(self.cols):
                row += str(self.grid[r][c])
            print(row)

    def get_best_balcony(self, balcony, sizes):
        best_score = 0
        sol_balcony = None
        for i in balcony:
            grid_copy = [x[:] for x in self.grid]
            p = Problem(grid_copy[i.begin:i.end], sizes.copy(), i.end - i.begin, self.cols)
            grid = p.get_solution()
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
        for i, o in enumerate(bal_list):
            if o.begin == b:
                del bal_list[i]
                break

    def update_grid(self, part_of_grid):
        index = 0
        for i in range(part_of_grid.begin, part_of_grid.end):
            self.grid[i] = part_of_grid.grid[index]
            index += 1

    def find_best_balcony(self, balcony, sizes):
        if len(balcony) == 1:
            i = balcony[0]
            p = Problem(self.grid[i.begin:i.end], sizes, i.end - i.begin, self.cols)
            grid = p.get_solution()
            i.grid = grid
            self.update_grid(i)
            self.output()
            p.output()
            self.taken += p.get_taken_seats()
        else:
            self.get_best_balcony(balcony, sizes)

    def get_balconies(self):
        balcony_row = []
        begin = 0
        end = 0
        balcony = False
        for r in range(self.rows):
            c = 0
            while True:
                if self.grid[r][c] != 0:
                    break
                if self.cols-1 == c:
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


class Balcony:
    def __init__(self, b, e):
        self.name = b
        self.begin = b
        self.end = e
        self.seats_taken = None
        self.sizes = None
        self.grid = None


class Online:
    def __init__(self, filepath) -> None:
        # Read file
        file_input = Input(filepath, "online")

        # From file input, initialize cinema and groups object
        self.cinema = Cinema(file_input.grid, file_input.row_nr, file_input.column_nr)
        self.groups = OnlineGroups(file_input.groups)
