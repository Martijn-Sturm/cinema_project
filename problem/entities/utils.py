import networkx as nx


def get_horizontal_neighboors(rows):
    """Computes the neighboors (distance 1 and 2) of each item in the list

    Args:
        rows (list): a list with items representing seats situated next to each other

    Returns:
        list(tuple): a list with tuples of seats that are within the distance (2) and hence considered to be close neighboors
    """
    neighboor_list = []
    for i in range(len(rows) - 2):
        for j in range(i + 1, i + 3):
            neighboor_list.append((rows[i], rows[j]))
    neighboor_list.append((rows[-2], rows[-1]))
    return neighboor_list


def get_vertical_neighboors(columns):
    """Computes the neighboors (distance 1) of each item in the list

    Args:
        columns (list): a list with items representing seats situated next to each other

    Returns:
        list(tuple): a list with tuples of seats that are within the distance (1) and hence considered to be close neighboors
    """
    neigboor_list = []
    for i in range(len(columns) - 1):
        for j in range(i + 1, i + 2):
            neigboor_list.append((columns[i], columns[j]))
    return neigboor_list


def get_diagonal_neighboor(matrix):
    """Computes the diagonal neighboor of each seat in the matrix

    Args:
        matrix (list(list)): a list containing a list per row, in which the items denote column positions

    Returns:
        list(tuple): a list with tuples denoting which nodes are within the neighboor distance
    """
    neighboor_list = []
    row_nr = len(matrix)
    column_nr = len(matrix[0])
    # diagonal north west -> sout east
    # All rows except southest row
    for row in range(row_nr - 1):
        # All columns except eastest column
        for column in range(column_nr - 1):
            neighboor_list.append((matrix[row][column], matrix[row + 1][column + 1]))
    # diagonal sout west -> north east
    # All rows except the northest row
    for row in range(1, row_nr):
        # All columns except eastest column
        for column in range(column_nr - 1):
            neighboor_list.append((matrix[row][column], matrix[row - 1][column + 1]))
    return neighboor_list


def transpose_list_matrix(matrix):
    """Transposes the matrix[row][column] to matrix[column][row] so that the inner lists now represent the row position, and the outer list the column position.

    Args:
        matrix (list(list)): A matrix of nested lists

    Returns:
        list(list): A matrix of nested lists
    """
    return list(map(list, zip(*matrix)))


def get_neighboors_from_grid(matrix):
    """Generate all neighboors situated 2 horizontally, 1 vertically, and 1 diagonally distanced from the seat at hand.

    Args:
        matrix (list(list)): grid with matrix[row][column]

    Returns:
        list(tuple): a list with tuples denoting neighboors as defined above.
    """
    neighboor_list = []
    # horizontal neighboors
    for row in matrix:
        neighboor_list = neighboor_list + get_horizontal_neighboors(row)

    # vertical neighboors
    # First transpose, matrix, so that each column is in the inner list
    transpose_matrix = transpose_list_matrix(matrix)
    for column in transpose_matrix:
        neighboor_list = neighboor_list + get_vertical_neighboors(column)

    # diagonal neigboors
    neighboor_list = neighboor_list + get_diagonal_neighboor(matrix)

    return neighboor_list


def create_cinema_graph(nodes):
    """Creates a networkx graph with each node representing a position in the cinema, and each edge proximity close enough between the positions so that if either one of those positions is occupied, the other cannot be occupied anymore under corona regulations.

    Args:
        nodes (list(list)): a cinema grid with nodes[row][column]

    Returns:
        networkx.Graph: A graph with each node represented by a position (any object that was used in nodes) and the edges represent proximity under corona regulations
    """
    graph = nx.Graph()
    flat_nodes = [item for sublist in nodes for item in sublist]
    graph.add_nodes_from(flat_nodes)
    edges = get_neighboors_from_grid(nodes)
    graph.add_edges_from(edges)
    return graph

