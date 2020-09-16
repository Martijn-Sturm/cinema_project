from problem.problem import Online
from logger.complete_logger import get_logger


class OnlineAlgorithm:
    def __init__(self, filepath) -> None:
        self.problem = Online(filepath)

    def get_total_seats(self):
        return len(self.problem.cinema.get_placement_position_coordinates())

    def run_naive1(self, logging_folder):
        print("Logs will be saved in:", logging_folder)
        problem = self.problem
        counter = 0
        places_filled = 0
        running = True
        while running:
            counter += 1
            logger = get_logger(f"group{str(counter)}", subfolder=logging_folder)

            logger.info(problem.cinema)

            n_free_seats = len(problem.cinema.get_placement_position_coordinates())
            logger.info(f"Number of free seats: {n_free_seats}")

            group_size = problem.groups.get_next_group()
            logger.info(f"Group size to be placed: {group_size}")

            options = problem.cinema.get_placement_possibilities()
            logger.info(f"Number of remaining options: {len(options)}")

            candidates = {}
            for option in options:
                if option.size >= group_size:
                    if option.size not in candidates:
                        candidates.update({option.size: [option]})
                    else:
                        candidates[option.size].append(option)
            option_sizes = [size for size in candidates.keys()]
            logger.info(f"Sizes of options are: {option_sizes}")

            if candidates:
                placement = candidates[min(candidates.keys())][0]
                problem.cinema.place_group(
                    placement.coordinates, group_size, str(counter)
                )
                logger.info(
                    f"Group of size: {group_size} is placed at placement {placement.coordinates} of size {placement.size}"
                )
                places_filled += group_size

            else:
                logger.warning(
                    f"The {counter}th group cannot be placed in cinema. Program exitting"
                )
                running = False
        return places_filled

