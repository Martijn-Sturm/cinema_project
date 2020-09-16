import abc
from typing import Tuple


class InterfacePosition(abc.ABC):
    @abc.abstractmethod
    def get_coordinates(self):
        pass

    @abc.abstractmethod
    def __str__(self):
        pass


class Seat(InterfacePosition):
    def __init__(self, coordinates: Tuple) -> None:
        """Creates Seat object

        Args:
            coordinates (tuple): (row, column)
        """
        self._coordinates = coordinates
        self.eligible = True
        self.taken = False
        self.taken_by = None

    def occupy_seat(self, group_id=None):
        """Sets seat to be taken

        Args:
            group_id ([type], optional): ID of group that is assigned to this seat. Defaults to None.
        """
        self.eligible = False
        self.taken = True
        self.taken_by = group_id

    def free_seat(self):
        """Makes seat free again
        """
        self.eligible = True
        self.taken = False
        self.taken_by = None

    def make_seat_unavailable(self):
        """Makes seat unavailable: This seat is not taken, but not available due to neighbooring occupied seats.
        """
        self.eligible = False
        self.taken = False
        self.taken_by = None

    def get_coordinates(self):
        """Returns the coordinates of the seat

        Returns:
            tuple: tuple(row, column)
        """
        return self._coordinates

    def __str__(self) -> str:
        if self.eligible:
            return "F"
        else:
            if self.taken:
                return "T"
            else:
                return "U"

    def __repr__(self) -> str:
        return self.__str__()


class Spacer(InterfacePosition):
    def __init__(self, coordinates: Tuple) -> None:
        """Creates Spacer object. Which is the contrary of a seat.

        Args:
            coordinates (tuple): (row, column)
        """
        self._coordinates = coordinates

    def __str__(self) -> str:
        return "X"

    def __repr__(self) -> str:
        return "Spacer((row, column))"

    def get_coordinates(self):
        """get coordinates as tuple

        Returns:
            tuple: (row, column)
        """
        return self._coordinates
