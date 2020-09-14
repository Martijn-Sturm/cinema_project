from .entities.input import Input
from .entities.cinema import Cinema
from .entities.groups import OfflineGroups, OnlineGroups


class Offline:
    def __init__(self, filepath) -> None:
        # Read file
        file_input = Input(filepath, "offline")

        # From file input, initialize cinema and groups object
        self.cinema = Cinema(file_input.grid, file_input.row_nr, file_input.column_nr)
        self.groups = OfflineGroups(file_input.groups)


class Online:
    def __init__(self, filepath) -> None:
        # Read file
        file_input = Input(filepath, "online")

        # From file input, initialize cinema and groups object
        self.cinema = Cinema(file_input.grid, file_input.row_nr, file_input.column_nr)
        self.groups = OnlineGroups(file_input.groups)
