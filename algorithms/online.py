from abc import abstractmethod
from problem.entities.cinema import PlacementPossibility
from problem.problem import Online
from problem.entities.groups import OnlineGroups
from logger.complete_logger import get_logger, dummy_logger
import abc
import random


class NoGroupsLeftError(Exception):
    def __str__(self):
        return "There are no groups to be placed anymore"


class NoPlacementFoundError(Exception):
    def __init__(self, group_size, message="No placement for this group was found."):
        self.group_size = group_size
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.group_size} -> {self.message}"


class OnlineAlgorithm(abc.ABC):
    """
    Base class for the variants of the online algorithms. It containts all the shared functionality used by each algorithm, and defines the interface.
    ...

    """

    NO_PLACE_INDICATION = "0 0"

    def __init__(self, filepath) -> None:
        self.filepath = filepath
        self._init_state()

    def _init_state(self):
        """Initiates the state of the online algorithm object. It sets the cinema and group attributes based on the filepath given during instantiation.
        """
        problem = Online(self.filepath)
        self.cinema = problem.cinema
        self.groups = problem.groups

    # def reset_state(self):
    #     """Resets the object's state to the original state when the object was instantiated
    #     """
    #     attrs = vars(self).keys()
    #     for attr in attrs:
    #         if attr == "filepath":
    #             continue
    #         delattr(self, attr)
    #     self._init_state()

    def set_new_groups(self, group_list: list):
        """Overrides the groups from the grid text file. Can be used to run the algorithm on user defined group sequence.

        Args:
            group_list (list[int]): A list of integers, left to right denotes the sequence in which they should be placed.
        """
        from collections import deque

        self.groups = OnlineGroups(group_list)

    def get_next_group(self):
        """Queries the next group to be placed in the cinema. Should only be used after previous placement is finished, to avoid cheating.

        Raises:
            NoGroupsLeftError: If there are no groups to be placed anymore, in the self.groups queue, this error is raised.

        Returns:
            int: The size of the group
        """
        try:
            group_size = self.groups.get_next_group()
            self.logger.info(f"Group size to be placed: {group_size}")

        except IndexError as err:
            self.logger.warning(f"No more groups in deque before 0 is reached")
            self.logger.debug(err)
            raise NoGroupsLeftError
        if group_size == 0:
            raise NoGroupsLeftError
        return group_size

    def get_remaining_free_seats(self):
        n_free_seats = len(self.cinema.get_placement_position_coordinates())
        return n_free_seats

    def get_placement_possibilities(self):
        """Gathers all the bins where groups can still be placed

        Returns:
            list(
                dict(
                    bin_size: list(PlacementPossibility)
                    )
                ): Returns a list containing dictionaries with as keys the bin size, and as values a list with all the placement possibilities with that specific bin size.
        """
        self.logger.info(self.cinema)

        options = self.cinema.get_placement_possibilities()
        self.logger.info(f"Number of remaining options: {len(options)}")
        return options

    @abstractmethod
    def choose_candidate(self) -> PlacementPossibility:
        """Chooses which placement possibility is used to place the current group. Must be implemented in each algorithm variant specifically.

        Returns:
            PlacementPossibility
        """
        pass

    def place_candidate(self, placement):
        """Places the current group at the given placementpossibility

        Args:
            placement (PlacementPossibility)
        """
        self.cinema.place_group(
            placement.coordinates, self.group_size, str(self.counter)
        )
        self.logger.info(
            f"Group of size: {self.group_size} is placed at placement {placement.coordinates} of size {placement.size}"
        )
        # Requirement: report where the group is placed:
        print(
            self.convert_position_coordinates_to_row_and_col_number(
                placement.coordinates
            )
        )

    @staticmethod
    def convert_position_coordinates_to_row_and_col_number(position_tuple):
        return f"{position_tuple[0] + 1} {position_tuple[1] + 1}"

    def log_end_results(self, folder):
        logger = get_logger(f"{self.__class__.__name__}_results", subfolder=folder)
        logger.info(
            f"Execution is stopped after an attempt to place the '{self.counter}' group"
        )
        logger.info(f"{self.filled_seats} number of seats were filled")
        remaining = self.get_remaining_free_seats()
        logger.info(f"{remaining} number of remaining free seats")

    def execute(self, logging_folder=None, log_grid=True):
        """Runs the algorithm

        Args:
            logging_folder (str, optional): Determines where the logs are stored in the log folder. If kept as 'None', no logs will be made. Defaults to None.
            log_grid (bool, optional): Determines if the grid prints will be saved in the logs. Defaults to True.

        Returns:
            Cinema
        """
        if logging_folder:
            print("Logs will be saved in:", logging_folder)
        self.counter = 0
        self.filled_seats = 0
        while True:
            self.counter += 1
            if logging_folder:
                self.logger = get_logger(
                    f"{self.__class__.__name__}-{str(self.counter)}",
                    subfolder=logging_folder + "/groups",
                )
            else:
                self.logger = dummy_logger()
            if log_grid:
                self.logger.info(self.cinema)
            try:
                self.group_size = self.get_next_group()
            except NoGroupsLeftError as err:
                print(err)
                break

            self.get_remaining_free_seats()

            free_seat_options = self.cinema.get_placement_possibilities()

            try:
                placement = self.choose_candidate(free_seat_options)
            except NoPlacementFoundError as err:
                self.logger.info(err)
                print(self.NO_PLACE_INDICATION)
                continue

            self.place_candidate(placement)
            self.filled_seats += self.group_size

        self.log_end_results(logging_folder)
        print(f"filled seats = {self.filled_seats}")
        return self.cinema

    def get_number_of_covid_seats_for_placement_possibility(
        self, placement_possibility: PlacementPossibility
    ) -> int:
        """Determines number of seats that would be within the covid distance of this placement possibility

        Args:
            placement_possibility (PlacementPossibility): -

        Returns:
            int: Number of seats that would be ineligible by placing this placement possibility
        """
        seat_coordinates = placement_possibility.get_list_of_seat_coordinates()
        covid_chairs = self.cinema.get_eligible_neighboors_from_group_of_coordinates(
            seat_coordinates
        )
        return len(covid_chairs)


class BestFit(OnlineAlgorithm):
    """Searches for the smallest bins that fits the group size. If multiple bins are present, the first found (left top in grid) is used"""

    def choose_candidate(self, options):

        candidates = filter_placement_possibilities_on_minimum_size(
            options, self.group_size
        )

        if not candidates:
            raise NoPlacementFoundError(self.group_size)

        option_sizes = [size for size in candidates.keys()]
        self.logger.info(f"Sizes of options are: {option_sizes}")

        return candidates[min(candidates.keys())][0]


class FirstFit(OnlineAlgorithm):
    """Will use the first bin size that the group fits in, starting from left top corner of cinema"""

    def choose_candidate(self, options):

        found_placement = False
        for option in options:
            if option.size >= self.group_size:
                return option

        if not found_placement:
            raise NoPlacementFoundError(self.group_size)


class WorstFit(OnlineAlgorithm):
    """Opposite of BestFit. It will use the largest bin size"""

    def choose_candidate(self, options):

        candidates = filter_placement_possibilities_on_minimum_size(
            options, self.group_size
        )
        if not candidates:
            raise NoPlacementFoundError(self.group_size)

        option_sizes = [size for size in candidates.keys()]
        self.logger.info(f"Sizes of options are: {option_sizes}")

        return candidates[max(candidates.keys())][0]


class Hybrid(OnlineAlgorithm):
    """
    A merge between the BestFit algorithm and the Greedy algorithm. Will perform BestFit first for each group. Then, it uses Greedy as tiebreaker for the best possibilities that BestFit found.
    """

    def choose_candidate(self, options):
        placement_possibilities = filter_placement_possibilities_on_minimum_size(
            options, self.group_size
        )

        if not placement_possibilities:
            raise NoPlacementFoundError(self.group_size)

        # Select best fitting first bin from possibilities:
        selected_bin = placement_possibilities[min(placement_possibilities.keys())][0]

        try:
            sub_possibilities = selected_bin.get_sub_possibilities(self.group_size)
        except Exception as err:
            if selected_bin.size < self.group_size:
                self.logger.debug(err)
                raise NoPlacementFoundError(self.group_size)
            else:
                raise

        # Determine for each sub possibility the number of covid chairs that it would result into
        candidates = {}
        for possibility in sub_possibilities:
            covid_chairs = self.get_number_of_covid_seats_for_placement_possibility(
                possibility
            )
            if covid_chairs not in candidates:
                candidates.update({covid_chairs: [possibility]})
            else:
                candidates[covid_chairs].append(possibility)

        if not candidates:
            raise NoPlacementFoundError(self.group_size)

        # Return the first candidate from the least covid chairs candidates
        return candidates[min(candidates.keys())][0]


class Greedy(OnlineAlgorithm):
    """
    Searches for a spot in the cinema for the group that leads to the list extra seats that are made unavaible due to corona distance.
    """

    def choose_candidate(self, options):

        # Gather all sub possibilities from which a super possibility consists:
        sub_possibilities = []
        for super_possibility in options:
            try:
                new_sub_possibilities = super_possibility.get_sub_possibilities(
                    self.group_size
                )
            except Exception as err:
                if super_possibility.size < self.group_size:
                    self.logger.debug(err)
                    continue
                else:
                    raise
            sub_possibilities = sub_possibilities + new_sub_possibilities

        # Determine for each sub possibility the number of covid chairs that it would result into
        candidates = {}
        for possibility in sub_possibilities:
            covid_chairs = self.get_number_of_covid_seats_for_placement_possibility(
                possibility
            )
            if covid_chairs not in candidates:
                candidates.update({covid_chairs: [possibility]})
            else:
                candidates[covid_chairs].append(possibility)

        if not candidates:
            raise NoPlacementFoundError(self.group_size)

        # Return the first candidate from the least covid chairs candidates
        return candidates[min(candidates.keys())][0]


def filter_placement_possibilities_on_minimum_size(options, minimum_size: int):
    """Can be used to filter all possibilities for placement of groups in a cinema for possibilities of minimum size, and orders  the result on size.   Generates dictionary with key=PlacementPossibility.size and values list(PlacementPosibilities)

    Args:
        options (list(PlacementPossbility)): A list with all placement possibilities (merged per row) remaining in the cinema. 
        minimum_size (int): The minimum size of seats next to each other, to filter the possibilities on.

    Returns:
        [type]: [description]
    """
    candidates = {}
    for option in options:
        if option.size >= minimum_size:
            if option.size not in candidates:
                candidates.update({option.size: [option]})
            else:
                candidates[option.size].append(option)
    return candidates
