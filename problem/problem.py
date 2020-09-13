from .entities.input import Input
from .entities.cinema import Cinema
from .entities.groups import Groups


class Problem:
    def __init__(self, filepath) -> None:
        # Read file
        file_input = Input(filepath)

        # From file input, initialize cinema and groups object
        self.cinema = Cinema(file_input.grid, file_input.row_nr, file_input.column_nr)
        self.groups = Groups(file_input.groups)

