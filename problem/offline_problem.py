"""Assignment New-Normal Cinema Seating Planning - Offline made by Anne Lycia Cate, Esmee Dekker, Lucas Meijer,
Zoril Oláh and Martijn Sturm."""

from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable, GLPK
from termcolor import colored
import math


class Problem:
    def __init__(self, g, ng, r, c):
        self.grid = g
        self.number_of_groups = ng
        self.rows = r
        self.cols = c

        # Create the model
        self.model = LpProblem(name="Cinema_Seating_Problem", sense=LpMaximize)
        # Initialize the decision variables
        self.x = {i: LpVariable(name=f"x{i}", lowBound=0, cat="Binary") for i in range(1, self.rows * self.cols + 1)}
        self.left = {i: LpVariable(name=f"left{i}", lowBound=0, cat="Binary") for i in
                     range(1, self.rows * self.cols - self.rows + 1)}
        self.right = {i: LpVariable(name=f"right{i}", lowBound=0, cat="Binary") for i in
                      range(1, self.rows * self.cols - self.rows + 1)}
        # Group size decision variables
        self.one = self.get_group_size_dict(0, "one")
        self.two = self.get_group_size_dict(1, "two")
        self.three = self.get_group_size_dict(2, "three")
        self.four = self.get_group_size_dict(3, "four")
        self.five = self.get_group_size_dict(4, "five")
        self.six = self.get_group_size_dict(5, "six")
        self.seven = self.get_group_size_dict(6, "seven")
        self.eight = self.get_group_size_dict(7, "eight")
        self.nine = self.get_group_size_dict(8, "nine")

    def print_grid(self):
        """Print grid."""
        print(self.rows)
        print(self.cols)
        for i in range(len(self.grid)):
            print(self.grid[i])
        print(self.number_of_groups)

    def get_solution(self):
        self.update_model_with_decision_variables()
        self.add_constraints_to_model()

        size_string_list = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight"]
        size_dict_list = [self.one, self.two, self.three, self.four, self.five, self.six, self.seven, self.eight]

        self.update_all_models(size_string_list, size_dict_list)
        self.determine_biggest_sum(size_string_list, size_dict_list)

        # Add the objective function to the model
        self.model += lpSum(self.x)

        # Solve the problem
        self.model.solve()
        # solver=GLPK(msg=False)

        self.output()

    def output(self):
        """
        for var in self.model.variables():
            if var.name[0:1] == 'x':
                coor = int(var.name[1:])
                xCoor = (coor - 1) % self.cols
                yCoor = math.floor((coor - 1) / self.cols)
                if self.grid[yCoor][xCoor] == 0:
                    self.grid[yCoor][xCoor] = "0"
                    continue
                if var.value() == 1:
                    self.grid[yCoor][xCoor] = "x"
                else:
                    self.grid[yCoor][xCoor] = "1"

        for r in range(self.rows):
            row = ""
            for c in range(self.cols):
                row += self.grid[r][c]
            print(row)
        """
        result = [['red'] * self.cols for _ in range(self.rows)]
        for var in self.model.variables():
            if var.name[0:1] == 'x':
                coor = int(var.name[1:])
                xCoor = (coor - 1) % self.cols
                yCoor = math.floor((coor - 1) / self.cols)
                if self.grid[yCoor][xCoor] == '0':
                    result[yCoor][xCoor] = 'grey'
                if var.value() == 1:
                    result[yCoor][xCoor] = 'green'

        print('\n'.join([''.join(['{:4}'.format(colored('■ ', item)) for item in row])
                         for row in result]))
        for name, constraint in self.model.constraints.items():
            if name[0:5] == 'Group':
                print(f"{name}: {constraint.value()}")


    def determine_biggest_sum(self, strings, dicts):
        for i in range(len(strings)):
            self.model += (lpSum(dicts[i]) <= self.number_of_groups[i], f"GroupCheck_{strings[i]}")
        self.model += (lpSum(self.nine) <= 0, "GroupCheck_Large")

    def update_all_models(self, strings, dicts):
        # update the model for group sizes one to eight
        for i in range(len(strings)):
            self.update_model(dicts[i], i+1, strings[i])
        self.check_for_bigger_group_sizes()

    def check_for_bigger_group_sizes(self):
        for row in range(self.rows):
            for col in range(self.cols - 8):
                key = row * (self.cols - 8) + col + 1
                xKey = row * self.cols + col + 1
                constraint = (self.nine[key] >= 1)
                for i in range(9):
                    self.model += (self.nine[key] <= self.x[xKey + i], f"Nine{key}_{i}GroupCheck")
                    constraint += -(self.x[xKey + i]) + 1
                self.model += (constraint, f"Nine{key}_TotalGroupCheck")

    def update_model_with_decision_variables(self):
        for key in self.left:
            xKey = key + math.floor((key - 1) / (self.cols - 1))
            self.model += (self.left[key] <= self.x[xKey], f"1Left{key}_Separation")
            self.model += (self.left[key] <= 1 - self.x[xKey + 1], f"2Left{key}_Separation")
            self.model += (self.left[key] >= self.x[xKey] - self.x[xKey + 1], f"zLeft{key}_Separation")
            self.model += (self.right[key] <= 1 - self.x[xKey], f"1Right{key}_Separation")
            self.model += (self.right[key] <= self.x[xKey + 1], f"2Right{key}_Separation")
            self.model += (self.right[key] >= self.x[xKey + 1] - self.x[xKey], f"zRight{key}_Separation")

    def get_group_size_dict(self, s, size_string):
        return {i: LpVariable(name=f"{size_string}{i}", lowBound=0, cat="Binary") for i in
                range(1, self.rows * self.cols - s * self.rows + 1)}

    def add_constraints_to_model(self):
        # Add the constraints to the model
        for key in self.x:
            xCoor = (key - 1) % self.cols
            yCoor = math.floor((key - 1) / self.cols)
            sideKey = key - yCoor
            max = 4 + int(self.grid[yCoor][xCoor])
            constraint = 5 * self.x[key] <= max

            if xCoor > 0:
                constraint += 4 * self.left[sideKey - 1]
            if xCoor < self.cols - 1:
                constraint += 4 * self.right[sideKey]
            if yCoor > 0:
                constraint += 2 * self.x[key - self.cols]
            if yCoor < self.rows - 1:
                constraint += 2 * self.x[key + self.cols]
            self.model += (constraint, f"x{key}_Crowdedness")

    def update_model(self, size_dict, size, size_string):
        size_minus = size - 1
        for row in range(self.rows):
            for col in range(self.cols - size_minus):
                key = row * (self.cols - size_minus) + col + 1
                xKey = row * self.cols + col + 1
                constraint = (size_dict[key] >= 1)
                if col > 0:
                    self.model += (size_dict[key] <= 1 - self.x[xKey - 1], f"{size_string}{key}_LeftGroupCheck")
                    constraint += -(1 - self.x[xKey - 1]) + 1
                for i in range(size):
                    self.model += (size_dict[key] <= self.x[xKey + i], f"{size_string}{key}_{i + 1}GroupCheck")
                    constraint += -(self.x[xKey + i]) + 1
                if col + size < self.cols:
                    self.model += (size_dict[key] <= 1 - self.x[xKey + size], f"{size_string}{key}_RightGroupCheck")
                    constraint += -(1 - self.x[xKey + size]) + 1
                self.model += (constraint, f"{size_string}{key}_TotalGroupCheck")

# SUCCESS!!
