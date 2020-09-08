"""Assignment New-Normal Cinema Seating Planning - Offline made by Anne Lycia Cate, Esmee Dekker, Lucas Meijer,
Zoril Oláh and Martijn Sturm."""


class Problem:
    def __init__(self):
        self.grid = []
        self.number_of_groups = []
        self.rows = 0
        self.cols = 0

    def input_data(self):
        """"Read input."""
        file = open("offline_input.txt", "r")  # open file
        self.rows = int(file.readline())    # read number of rows
        self.cols = int(file.readline())    # read number of seats on the rows

        for i in range(self.rows):  # read all the rows
            r = list(file.readline().strip())   # split each character on the row in a list
            self.grid.append(r)     # add the list of the row to the grid

        self.number_of_groups = [int(n) for n in file.readline().split()]  # read number of groups for each group size
        file.close()

    def print_grid(self):
        """Print grid."""
        for i in range(len(self.grid)):
            print(self.grid[i])
        print(self.number_of_groups)


p = Problem()
p.input_data()
p.print_grid()
