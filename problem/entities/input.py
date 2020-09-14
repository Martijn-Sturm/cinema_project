class Input:
    """
    Object to process and store the data from the input text file
    ...
    
    Attributes
    ----------
    file_content : str
        The raw text from the input file
    row_nr : int
        The number of rows in the cinema
    column_nr: int
        The number of columns in the cinema
    grid: list(list)
        The seating grid of the cinema: grid[row][column]. 1 is seat, 0 is no seat (spacer)
    groups: list(int)
        The groups to be placed in the cinema. The index of each item represents the group size. The item value is the count of that group size
    """

    GRID_BEGIN_LINE_INDEX = 2

    def __init__(self, file_path, type) -> None:

        self.file_content = self._read_input_file(file_path)
        self.row_nr = self._get_row_nr_from_file_content(self.file_content)
        self.column_nr = self._get_column_nr_from_file_content(self.file_content)
        self.grid = self._get_grid_from_file_content(self.file_content, self.row_nr)

        if type == "offline":
            self.groups = self._get_offline_groups_from_file_content(self.file_content)
        elif type == "online":
            self.groups = self._get_online_groups_from_file_content(
                self.file_content, self.row_nr
            )
        else:
            raise ValueError(
                "type argument should either be 'offline' or 'online' string, depending on the problem at hand."
            )

    def _read_input_file(self, file_path):
        with open(file_path, mode="r") as file:
            return file.read().splitlines()

    def _get_row_nr_from_file_content(self, file_content):
        return int(file_content[0])

    def _get_column_nr_from_file_content(self, file_content):
        return int(file_content[1])

    def _get_grid_from_file_content(self, file_content, row_nr):
        grid = []
        end_index = Input.GRID_BEGIN_LINE_INDEX + row_nr
        for file_content_index in range(Input.GRID_BEGIN_LINE_INDEX, end_index):
            row = file_content[file_content_index]
            grid.append([int(position) for position in row])
        return grid

    def _get_offline_groups_from_file_content(self, file_content):
        # last list in file_content
        return [int(group) for group in file_content[-1].split(" ")]

    def _get_online_groups_from_file_content(self, file_content, row_nr):
        groups = []
        for group_index in range(
            # First line after grid to the last line
            Input.GRID_BEGIN_LINE_INDEX + row_nr,
            len(file_content),
        ):
            groups.append(file_content[group_index])
        return groups
