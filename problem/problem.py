from .entities.input import Input
from .entities.cinema import Cinema
from .entities.groups import OnlineGroups
from problem.offline_problem import Problem


class Offline:
    def __init__(self, filepath) -> None:
        # Read file
        file_input = Input(filepath, "offline")
        p = Problem(file_input.grid, file_input.groups, file_input.row_nr, file_input.column_nr, file_input.vips)
        # p.print_grid()
        p.get_solution()

class Onfline:
    def __init__(self, filepath) -> None:
        # Read file
        file_input = Input(filepath, "onfline")
        p = Problem(file_input.grid, file_input.groups, file_input.row_nr, file_input.column_nr, file_input.vips)
        # p.print_grid()
        p.get_solution()
        self.result = p.model.objective.value()
    def __result__():
        return self.result

class Online:
    def __init__(self, filepath) -> None:
        # Read file
        file_input = Input(filepath, "online")

        # From file input, initialize cinema and groups object
        self.cinema = Cinema(file_input.grid, file_input.row_nr, file_input.column_nr)
        self.groups = OnlineGroups(file_input.groups)
