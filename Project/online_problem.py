"""Assignment New-Normal Cinema Seating Planning - Online made by Anne Lycia Cate, Esmee Dekker, Lucas Meijer,
Zoril Oláh and Martijn Sturm."""


class Problem:
    def __init__(self):
        self.grid = []  # list of lists
        self.group_size = []
        self.rows = 0
        self.cols = 0

    def input_data(self):
        """"Read input."""
        file = open("online_input.txt", "r")  # open file
        self.rows = int(file.readline())    # read number of rows
        self.cols = int(file.readline())    # read number of seats on the rows

        for i in range(self.rows):  # read all the rows
            r = list(file.readline().strip())   # split each character on the row in a list
            self.grid.append(r)     # add the list of the row to the grid

        number = int(file.readline())
        while number != 0:      # read all group numbers one by one until a 0 is reached
            self.insert_group(number)
            number = int(file.readline())
        file.close()

    def insert_group(self, n):
        """Algorithm that inserts a group in the grid."""
        print(n)

    def print_grid(self):
        """Print grid."""
        for i in range(len(self.grid)):
            print(self.grid[i])


p = Problem()
p.input_data()
p.print_grid()
