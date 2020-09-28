from abc import abstractmethod
from problem.problem import Online
from logger.complete_logger import get_logger
import abc


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
    NO_PLACE_INDICATION = "0 0"

    def __init__(self, filepath) -> None:
        self.filepath = filepath
        self._init_state()

    def _init_state(self):
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

    def set_new_randomized_groups(self, group_list: list):
        from collections import deque

        self.groups = deque(group_list)

    def get_next_group(self):
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
        self.logger.info(self.cinema)

        options = self.cinema.get_placement_possibilities()
        self.logger.info(f"Number of remaining options: {len(options)}")
        return options

    @abstractmethod
    def choose_candidate(self):
        pass

    def place_candidate(self, placement):
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

    def execute(self, logging_folder, log_grid=True):
        print("Logs will be saved in:", logging_folder)
        self.counter = 0
        self.filled_seats = 0
        while True:
            self.counter += 1
            self.logger = get_logger(
                f"{self.__class__.__name__}-{str(self.counter)}",
                subfolder=logging_folder + "/groups",
            )
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


class BestFit(OnlineAlgorithm):
    def choose_candidate(self, options):

        candidates = select_placement_possibilities_of_minimum_size(
            options, self.group_size
        )
        if not candidates:
            raise NoPlacementFoundError(self.group_size)

        option_sizes = [size for size in candidates.keys()]
        self.logger.info(f"Sizes of options are: {option_sizes}")

        return candidates[min(candidates.keys())][0]


class FirstFit(OnlineAlgorithm):
    def choose_candidate(self, options):

        found_placement = False
        for option in options:
            if option.size >= self.group_size:
                return option

        if not found_placement:
            raise NoPlacementFoundError(self.group_size)


class WorstFit(OnlineAlgorithm):
    def choose_candidate(self, options):

        candidates = select_placement_possibilities_of_minimum_size(
            options, self.group_size
        )
        if not candidates:
            raise NoPlacementFoundError(self.group_size)

        option_sizes = [size for size in candidates.keys()]
        self.logger.info(f"Sizes of options are: {option_sizes}")

        return candidates[max(candidates.keys())][0]


class MinCovidChairs(OnlineAlgorithm):
    def choose_candidate(self, options):
        # loop through all options
        candidates = {}
        for option in options:
            size = self.group_size
            if option.size >= size:
                coordinates = option[1]
                positions = []
                # Convert to positions
                for n in range(size):
                    row = int(coordinates[0])
                    column = int(coordinates[1]) + n
                    positions.append(self.cinema.get_position((row, column)))
                covid_chairs = []
                # Count number of covid chairs this option would add
                for position in positions:
                    covid_chairs = (
                        covid_chairs
                        + self.cinema.get_eligible_neighboors_from_position(position)
                    )
                covid_chairs = set(covid_chairs)
                # Also the to be occupied chairs were counted if groups are bigger than 1.
                if self.group_size > 1:
                    number_covid_chairs = len(covid_chairs) - int(self.group_size)
                else:
                    number_covid_chairs = len(covid_chairs)
                # Add candidate to candidates
                if number_covid_chairs not in candidates:
                    candidates.update({number_covid_chairs: [option]})
                else:
                    candidates[number_covid_chairs].append(option)
        return candidates[min(candidates.keys())][0]


def select_placement_possibilities_of_minimum_size(options, size: int):
    candidates = {}
    for option in options:
        if option.size >= size:
            if option.size not in candidates:
                candidates.update({option.size: [option]})
            else:
                candidates[option.size].append(option)
    return candidates
