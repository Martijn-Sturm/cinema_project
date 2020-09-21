"""Assignment New-Normal Cinema Seating Planning - Offline made by Anne Lycia Cate, Esmee Dekker, Lucas Meijer,
Zoril Oláh and Martijn Sturm."""

from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable, GLPK
import math

class Problem:
    def __init__(self):
        self.grid = []
        self.number_of_groups = []
        self.rows = 0
        self.cols = 0

    def input_data(self):
        """"Read input."""
        file = open("/Users/clazinasteunenberg/Documents/GitHub/cinema_project/input/offline_challengingInput.txt", "r")  # open file
        self.rows = int(file.readline())    # read number of rows
        self.cols = int(file.readline())    # read number of seats on the rows

        for i in range(self.rows):  # read all the rows
            r = list(file.readline().strip())   # split each character on the row in a list
            self.grid.append(r)     # add the list of the row to the grid

        self.number_of_groups = [int(n) for n in file.readline().split()]  # read number of groups for each group size
        file.close()

    def print_grid(self):
        """Print grid."""
        print(self.rows)
        print(self.cols)
        for i in range(len(self.grid)):
            print(self.grid[i])
        print(self.number_of_groups)


p = Problem()
p.input_data()
p.print_grid()

# Create the model
model = LpProblem(name="Cinema_Seating_Problem", sense=LpMaximize)

# Initialize the decision variables
x = {i: LpVariable(name=f"x{i}", lowBound=0, cat="Binary") for i in range(1, p.rows * p.cols + 1)}
left = {i: LpVariable(name=f"left{i}", lowBound=0, cat="Binary") for i in range(1, p.rows * p.cols - p.rows + 1)}
right = {i: LpVariable(name=f"right{i}", lowBound=0, cat="Binary") for i in range(1, p.rows * p.cols - p.rows + 1)}

# Group size decision variables
one = {i: LpVariable(name=f"one{i}", lowBound=0, cat="Binary") for i in range(1, p.rows * p.cols + 1)}
two = {i: LpVariable(name=f"two{i}", lowBound=0, cat="Binary") for i in range(1, p.rows * p.cols - p.rows + 1)}
three = {i: LpVariable(name=f"three{i}", lowBound=0, cat="Binary") for i in range(1, p.rows * p.cols - 2 * p.rows + 1)}
four = {i: LpVariable(name=f"four{i}", lowBound=0, cat="Binary") for i in range(1, p.rows * p.cols - 3 * p.rows + 1)}
five = {i: LpVariable(name=f"five{i}", lowBound=0, cat="Binary") for i in range(1, p.rows * p.cols - 4 * p.rows + 1)}
six = {i: LpVariable(name=f"six{i}", lowBound=0, cat="Binary") for i in range(1, p.rows * p.cols - 5 * p.rows + 1)}
seven = {i: LpVariable(name=f"seven{i}", lowBound=0, cat="Binary") for i in range(1, p.rows * p.cols - 6 * p.rows + 1)}
eight = {i: LpVariable(name=f"eight{i}", lowBound=0, cat="Binary") for i in range(1, p.rows * p.cols - 7 * p.rows + 1)}
nine = {i: LpVariable(name=f"nine{i}", lowBound=0, cat="Binary") for i in range(1, p.rows * p.cols - 8 * p.rows + 1)}

for key in left:
    xKey = key + math.floor((key - 1) / (p.cols - 1))
    model += (left[key] <= x[xKey], f"1Left{key}_Separation")
    model += (left[key] <= 1 - x[xKey + 1], f"2Left{key}_Separation")
    model += (left[key] >= x[xKey] - x[xKey + 1], f"zLeft{key}_Separation")
    model += (right[key] <= 1 - x[xKey], f"1Right{key}_Separation")
    model += (right[key] <= x[xKey + 1], f"2Right{key}_Separation")
    model += (right[key] >= x[xKey + 1] - x[xKey], f"zRight{key}_Separation")
    
# Add the constraints to the model
for key in x:
    xCoor = (key - 1) % p.cols
    yCoor = math.floor((key - 1) / p.cols)

    sideKey = key - yCoor

    max = 4 + int(p.grid[yCoor][xCoor])

    constraint = 5 * x[key] <= max
    if(xCoor > 0):
        constraint += 4 * left[sideKey - 1]
    if(xCoor < p.cols - 1):
        constraint += 4 * right[sideKey]
    if(yCoor > 0):
        constraint += 2 * x[key - p.cols]
    if(yCoor < p.rows - 1):
        constraint += 2 * x[key + p.cols]
    model += (constraint, f"x{key}_Crowdedness")

# one
for row in range(p.rows):
    for col in range(p.cols):
        key = row * p.cols + col + 1
        constraint = (one[key] >= 1)
        if(col > 0):
            model += (one[key] <= 1 - x[key - 1], f"One{key}_LeftGroupCheck")
            constraint += -(1 - x[key - 1]) + 1
        model += (one[key] <= x[key], f"One{key}_1GroupCheck")
        constraint += -(x[key]) + 1
        if(col + 1 < p.cols):
            model += (one[key] <= 1 - x[key + 1], f"One{key}_RightGroupCheck")
            constraint += -(1 - x[key + 1]) + 1
        model += (constraint, f"One{key}_TotalGroupCheck")

# variables:
## p.cols removed (for range & col)
## variable name
## constraint name
## i range

# two
for row in range(p.rows):
    for col in range(p.cols - 1):
        key = row * (p.cols - 1) + col + 1
        xKey = row * p.cols + col + 1
        constraint = (two[key] >= 1)
        if(col > 0):
            model += (two[key] <= 1 - x[xKey - 1], f"Two{key}_LeftGroupCheck")
            constraint += -(1 - x[xKey - 1]) + 1
        for i in range(2):
            model += (two[key] <= x[xKey + i], f"Two{key}_{i}GroupCheck")
            constraint += -(x[xKey + i]) + 1
        if(col + 2 < p.cols):
            model += (two[key] <= 1 - x[xKey + 2], f"Two{key}_RightGroupCheck")
            constraint += -(1 - x[xKey + 2]) + 1
        model += (constraint, f"Two{key}_TotalGroupCheck")

# three
for row in range(p.rows):
    for col in range(p.cols - 2):
        key = row * (p.cols - 2) + col + 1
        xKey = row * p.cols + col + 1
        constraint = (three[key] >= 1)
        if(col > 0):
            model += (three[key] <= 1 - x[xKey - 1], f"Three{key}_LeftGroupCheck")
            constraint += -(1 - x[xKey - 1]) + 1
        for i in range(3):
            model += (three[key] <= x[xKey + i], f"Three{key}_{i}GroupCheck")
            constraint += -(x[xKey + i]) + 1
        if(col + 3 < p.cols):
            model += (three[key] <= 1 - x[xKey + 3], f"Three{key}_RightGroupCheck")
            constraint += -(1 - x[xKey + 3]) + 1
        model += (constraint, f"Three{key}_TotalGroupCheck")

# four
for row in range(p.rows):
    for col in range(p.cols - 3):
        key = row * (p.cols - 3) + col + 1
        xKey = row * p.cols + col + 1
        constraint = (four[key] >= 1)
        if(col > 0):
            model += (four[key] <= 1 - x[xKey - 1], f"Four{key}_LeftGroupCheck")
            constraint += -(1 - x[xKey - 1]) + 1
        for i in range(4):
            model += (four[key] <= x[xKey + i], f"Four{key}_{i}GroupCheck")
            constraint += -(x[xKey + i]) + 1
        if(col + 4 < p.cols):
            model += (four[key] <= 1 - x[xKey + 4], f"Four{key}_RightGroupCheck")
            constraint += -(1 - x[xKey + 4]) + 1
        model += (constraint, f"Four{key}_TotalGroupCheck")

# five
for row in range(p.rows):
    for col in range(p.cols - 4):
        key = row * (p.cols - 4) + col + 1
        xKey = row * p.cols + col + 1
        constraint = (five[key] >= 1)
        if(col > 0):
            model += (five[key] <= 1 - x[xKey - 1], f"Five{key}_LeftGroupCheck")
            constraint += -(1 - x[xKey - 1]) + 1
        for i in range(5):
            model += (five[key] <= x[xKey + i], f"Five{key}_{i}GroupCheck")
            constraint += -(x[xKey + i]) + 1
        if(col + 5 < p.cols):
            model += (five[key] <= 1 - x[xKey + 5], f"Five{key}_RightGroupCheck")
            constraint += -(1 - x[xKey + 5]) + 1
        model += (constraint, f"Five{key}_TotalGroupCheck")

# six
for row in range(p.rows):
    for col in range(p.cols - 5):
        key = row * (p.cols - 5) + col + 1
        xKey = row * p.cols + col + 1
        constraint = (six[key] >= 1)
        if(col > 0):
            model += (six[key] <= 1 - x[xKey - 1], f"Six{key}_LeftGroupCheck")
            constraint += -(1 - x[xKey - 1]) + 1
        for i in range(6):
            model += (six[key] <= x[xKey + i], f"Six{key}_{i}GroupCheck")
            constraint += -(x[xKey + i]) + 1
        if(col + 6 < p.cols):
            model += (six[key] <= 1 - x[xKey + 6], f"Six{key}_RightGroupCheck")
            constraint += -(1 - x[xKey + 6]) + 1
        model += (constraint, f"Six{key}_TotalGroupCheck")

# seven
for row in range(p.rows):
    for col in range(p.cols - 6):
        key = row * (p.cols - 6) + col + 1
        xKey = row * p.cols + col + 1
        constraint = (seven[key] >= 1)
        if(col > 0):
            model += (seven[key] <= 1 - x[xKey - 1], f"Seven{key}_LeftGroupCheck")
            constraint += -(1 - x[xKey - 1]) + 1
        for i in range(7):
            model += (seven[key] <= x[xKey + i], f"Seven{key}_{i}GroupCheck")
            constraint += -(x[xKey + i]) + 1
        if(col + 7 < p.cols):
            model += (seven[key] <= 1 - x[xKey + 3], f"Seven{key}_RightGroupCheck")
            constraint += -(1 - x[xKey + 7]) + 1
        model += (constraint, f"Seven{key}_TotalGroupCheck")

# eight
for row in range(p.rows):
    for col in range(p.cols - 7):
        key = row * (p.cols - 7) + col + 1
        xKey = row * p.cols + col + 1
        constraint = (eight[key] >= 1)
        if(col > 0):
            model += (eight[key] <= 1 - x[xKey - 1], f"Eight{key}_LeftGroupCheck")
            constraint += -(1 - x[xKey - 1]) + 1
        for i in range(8):
            model += (eight[key] <= x[xKey + i], f"Eight{key}_{i}GroupCheck")
            constraint += -(x[xKey + i]) + 1
        if(col + 8 < p.cols):
            model += (eight[key] <= 1 - x[xKey + 8], f"Eight{key}_RightGroupCheck")
            constraint += -(1 - x[xKey + 8]) + 1
        model += (constraint, f"Eight{key}_TotalGroupCheck")

# nine
for row in range(p.rows):
    for col in range(p.cols - 8):
        key = row * (p.cols - 8) + col + 1
        xKey = row * p.cols + col + 1
        constraint = (nine[key] >= 1)
        for i in range(9):
            model += (nine[key] <= x[xKey + i], f"Nine{key}_{i}GroupCheck")
            constraint += -(x[xKey + i]) + 1
        model += (constraint, f"Nine{key}_TotalGroupCheck")

model += (lpSum(one) <= p.number_of_groups[0], "GroupCheck_One")
model += (lpSum(two) <= p.number_of_groups[1], "GroupCheck_Two")
model += (lpSum(three) <= p.number_of_groups[2], "GroupCheck_Three")
model += (lpSum(four) <= p.number_of_groups[3], "GroupCheck_Four")
model += (lpSum(five) <= p.number_of_groups[4], "GroupCheck_Five")
model += (lpSum(six) <= p.number_of_groups[5], "GroupCheck_Six")
model += (lpSum(seven) <= p.number_of_groups[6], "GroupCheck_Seven")
model += (lpSum(eight) <= p.number_of_groups[7], "GroupCheck_Eight")
model += (lpSum(nine) <= 0, "GroupCheck_Large")

# Add the objective function to the model
model += lpSum(x)

# Solve the problem
status = model.solve()
# solver=GLPK(msg=False)

result = [[0]*p.cols for _ in range(p.rows)]
for var in model.variables():
    if(var.name[0:1] == 'x' and var.value() == 1):
        coor = int(var.name[1:])
        xCoor = (coor - 1) % p.cols
        yCoor = math.floor((coor - 1) / p.cols)
        result[yCoor][xCoor] = 1
    
print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
      for row in result]))

for name, constraint in model.constraints.items():
    if(name[0:5] == 'Group'):
        print(f"{name}: {constraint.value()}")

## SUCCESS!!