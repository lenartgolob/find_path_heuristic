import time
import sys
import matplotlib.pyplot as plt
import tracemalloc

def read_file(file):
    labyrinth = []
    for line in open(file).readlines():
        labyrinth.append([int(x) for x in line[:-1].split(",")])
    return labyrinth

def find_start_end_treasures(labyrinth):
    treasures = []
    for i in range(len(labyrinth)):
        for j in range(len(labyrinth[0])):
            if labyrinth[i][j] == -2:
                start = (i, j)
            elif labyrinth[i][j] == -4:
                end = (i, j)
            elif labyrinth[i][j] == -3:
                treasures.append((i, j))
    return (start, end, treasures)

class Node:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.previous = None
        self.obstacle = False

    def add_neighbors(self, grid, columns, rows):
        neighbor_x = self.x
        neighbor_y = self.y

        if neighbor_y > 0:
            self.neighbors.append(grid[neighbor_x][neighbor_y - 1])
        if neighbor_x < columns - 1:
            self.neighbors.append(grid[neighbor_x + 1][neighbor_y])
        if neighbor_y < rows - 1:
            self.neighbors.append(grid[neighbor_x][neighbor_y + 1])
        if neighbor_x > 0:
            self.neighbors.append(grid[neighbor_x - 1][neighbor_y])

class GreedyBestSearch:

    def __init__(self, cols, rows, start, end, labyrinth, treasures):
        self.cols = cols
        self.rows = rows
        self.start = start
        self.end = end
        self.labyrinth = labyrinth
        self.treasures = treasures
        self.final_price = 0
        self.nodes_accounted = 0
        self.searched_nodes = 0

    @staticmethod
    def clean_open_set(open_set, current_node):
        for i in range(len(open_set)):
            if open_set[i] == current_node:
                open_set.pop(i)
                break
        return open_set

    @staticmethod
    def h_score(current_node, end):
        distance = abs(current_node.x - end.x) + abs(current_node.y - end.y) # Manhattan distance
        return distance

    @staticmethod
    def create_grid(cols, rows):
        grid = []
        for _ in range(cols):
            grid.append([])
            for _ in range(rows):
                grid[-1].append(0)
        return grid

    @staticmethod
    def fill_grids(grid, cols, rows, labyrinth):
        for i in range(cols):
            for j in range(rows):
                grid[i][j] = Node(i, j)
                if labyrinth[i][j] == -1:
                    grid[i][j].obstacle = True
        return grid

    @staticmethod
    def get_neighbors(grid, cols, rows):
        for i in range(cols):
            for j in range(rows):
                # Add neighbours for all nodes in grid
                grid[i][j].add_neighbors(grid, cols, rows)
        return grid

    @staticmethod
    def start_path(self, open_set, closed_set, current_node, end):
        self.searched_nodes += 1
        best_way = 0
        # Find the node with the best f in open_set
        for i in range(len(open_set)):
            if open_set[i].f < open_set[best_way].f:
                best_way = i

        current_node = open_set[best_way]
        final_path = []
        # Check if its the last node
        if current_node == end:
            temp = current_node
            final_path.append(temp)
            while temp.previous:
                final_path.append(temp.previous)
                temp = temp.previous

        # Remove current_node from open_set
        open_set = GreedyBestSearch.clean_open_set(open_set, current_node)
        # Add the current_node to closed_set
        closed_set.append(current_node)
        # Go through all neighbours of current_node
        neighbors = current_node.neighbors
        for neighbor in neighbors:
            # Skip node if its closed or an obstacle
            if (neighbor in closed_set) or (neighbor.obstacle):
                continue
            else:
                if labyrinth[neighbor.x][neighbor.y] > 0:
                    temp_g = current_node.g + labyrinth[neighbor.x][neighbor.y]
                else:
                    temp_g = current_node.g
                control_flag = 0
                for k in range(len(open_set)):
                    # Checks if neighbour is in open_set
                    if neighbor.x == open_set[k].x and neighbor.y == open_set[k].y:
                        control_flag = 1

                # Control flag -> 1: The node is already in open_set and there's a better path than the current one
                # Control flag -> 2: The node isn't in open_set or it's in, but the current path is better
                if control_flag == 1:
                    pass
                else:
                    neighbor.g = temp_g
                    neighbor.h = GreedyBestSearch.h_score(neighbor, end)
                    neighbor.f = neighbor.h
                    neighbor.previous = current_node
                    open_set.append(neighbor)

        return open_set, closed_set, current_node, final_path[:-1]

    @staticmethod
    def find_treasures(self, open_set, closed_set, current_node, treasures_list):
        self.searched_nodes += 1
        best_way = 0
        # Find the node with the best f in open_set
        for i in range(len(open_set)):
            if open_set[i].f < open_set[best_way].f:
                best_way = i

        current_node = open_set[best_way]
        final_path = []
        price = 0
        #print("(", current_node.x, ", ", current_node.y, ")")
        if((current_node.x, current_node.y) in treasures_list):
            price = current_node.g
            temp = current_node
            final_path.append(temp)
            #print("Treasure ", (current_node.x, current_node.y))
            while temp.previous:
                #print("working")
                #print((temp.previous.x, temp.previous.y))
                final_path.append(temp.previous)
                temp = temp.previous

        # Remove current_node from open_set
        open_set = GreedyBestSearch.clean_open_set(open_set, current_node)
        # Add the current_node to closed_set
        closed_set.append(current_node)
        # Go through all neighbours of current_node
        neighbors = current_node.neighbors
        for neighbor in neighbors:
            # Skip node if its closed or an obstacle
            if (neighbor in closed_set) or (neighbor.obstacle):
                continue
            else:
                if labyrinth[neighbor.x][neighbor.y] > 0:
                    temp_g = current_node.g + labyrinth[neighbor.x][neighbor.y]
                else:
                    temp_g = current_node.g
                control_flag = 0
                for k in range(len(open_set)):
                    # Checks if neighbour is in open_set
                    if neighbor.x == open_set[k].x and neighbor.y == open_set[k].y:
                        # Checks if the current path is better (smaller g)
                        control_flag = 1

                # Control flag -> 1: The node is already in open_set and there's a better path than the current one
                # Control flag -> 0: The node isn't in open_set or it's in, but the current path is better
                if control_flag == 1:
                    pass
                else:
                    neighbor.g = temp_g
                    # Calculate the lowest h_score of all treasures
                    min_h = sys.maxsize
                    for treasure in treasures:
                        temp_h = GreedyBestSearch.h_score(neighbor, Node(treasure[0], treasure[1]))
                        if temp_h < min_h:
                            min_h = temp_h
                    neighbor.h = min_h
                    neighbor.f = neighbor.h
                    neighbor.previous = current_node
                    open_set.append(neighbor)

        return open_set, closed_set, current_node, final_path[:-1], price

    @staticmethod
    def treasure_path(self, startNode, treasures_list): # Finds the path to the nearest and least costly treasure
        open_set = []
        closed_set = []
        current_node = None
        final_path = []
        self.nodes_accounted = 100
        open_set.append(startNode)
        while len(open_set) > 0:
            open_set, closed_set, current_node, final_path, price = GreedyBestSearch.find_treasures(self, open_set, closed_set, current_node, treasures_list)
            if len(final_path) > 0:
                break
        return final_path, price


    def main(self):
        # Create empty grid
        grid = GreedyBestSearch.create_grid(self.cols, self.rows)
        # Fill the grid with nodes
        grid = GreedyBestSearch.fill_grids(grid, self.cols, self.rows, self.labyrinth)
        # Set neighbours for every node in grid
        grid = GreedyBestSearch.get_neighbors(grid, self.cols, self.rows)
        startNode = grid[self.start[0]][self.start[1]]
        final_path = [startNode]
        final_price = 0
        treasures_list = treasures
        # Finds the path to all the treasures
        for _ in range(len(treasures)):
            # Finds the path to the closest treasure and saves it to final_path
            path, price = GreedyBestSearch.treasure_path(self, startNode, treasures_list)
            final_path = path + final_path
            final_price += price
            first_element = final_path[0]
            treasures_list.remove((first_element.x, first_element.y))
            startNode = Node(first_element.x, first_element.y)
            startNode.add_neighbors(grid, self.cols, self.rows)
        open_set = []
        closed_set = []
        current_node = None
        end_path = []
        self.end = grid[self.end[0]][self.end[1]]
        # Add the starting node to open_set
        open_set.append(startNode)
        # Set end as a node instead of coordinates
        while len(open_set) > 0:
            open_set, closed_set, current_node, end_path = GreedyBestSearch.start_path(self, open_set, closed_set, current_node, self.end)
            if len(end_path) > 0:
                break
        final_path = end_path + final_path
        final_price += final_path[0].g
        return final_path[::-1], final_price

class AStar:

    def __init__(self, cols, rows, start, end, labyrinth, treasures):
        self.cols = cols
        self.rows = rows
        self.start = start
        self.end = end
        self.labyrinth = labyrinth
        self.treasures = treasures
        self.final_price = 0
        self.searched_nodes = 0

    @staticmethod
    def clean_open_set(open_set, current_node):
        for i in range(len(open_set)):
            if open_set[i] == current_node:
                open_set.pop(i)
                break
        return open_set

    @staticmethod
    def h_score(current_node, end):
        distance = abs(current_node.x - end.x) + abs(current_node.y - end.y) # Manhattan metoda
        return distance

    @staticmethod
    def create_grid(cols, rows):
        grid = []
        for _ in range(cols):
            grid.append([])
            for _ in range(rows):
                grid[-1].append(0)
        return grid

    @staticmethod
    def fill_grids(grid, cols, rows, labyrinth):
        for i in range(cols):
            for j in range(rows):
                grid[i][j] = Node(i, j)
                if labyrinth[i][j] == -1:
                    grid[i][j].obstacle = True
        return grid

    @staticmethod
    def get_neighbors(grid, cols, rows):
        for i in range(cols):
            for j in range(rows):
                # Add neighbours for all nodes in grid
                grid[i][j].add_neighbors(grid, cols, rows)
        return grid

    @staticmethod
    def start_path(self, open_set, closed_set, current_node, end):
        self.searched_nodes += 1
        best_way = 0
        # Find the node with the best f in open_set
        for i in range(len(open_set)):
            if open_set[i].f < open_set[best_way].f:
                best_way = i

        current_node = open_set[best_way]
        final_path = []
        # Check if its the last node
        if current_node == end:
            temp = current_node
            final_path.append(temp)
            while temp.previous:
                final_path.append(temp.previous)
                temp = temp.previous

        # Remove current_node from open_set
        open_set = AStar.clean_open_set(open_set, current_node)
        # Add the current_node to closed_set
        closed_set.append(current_node)
        # Go through all neighbours of current_node
        neighbors = current_node.neighbors
        for neighbor in neighbors:
            # Skip node if its closed or an obstacle
            if (neighbor in closed_set) or (neighbor.obstacle):
                continue
            else:
                if labyrinth[neighbor.x][neighbor.y] > 0:
                    temp_g = current_node.g + labyrinth[neighbor.x][neighbor.y]
                else:
                    temp_g = current_node.g
                control_flag = 0
                for k in range(len(open_set)):
                    # Checks if neighbour is in open_set
                    if neighbor.x == open_set[k].x and neighbor.y == open_set[k].y:
                        # Checks if the current path is better (smaller g)
                        if temp_g < open_set[k].g:
                            # Create f, g, h values
                            open_set[k].g = temp_g
                            open_set[k].h = AStar.h_score(open_set[k], end)
                            open_set[k].f = open_set[k].g + open_set[k].h
                            open_set[k].previous = current_node
                        else:
                            pass
                        control_flag = 1

                # Control flag -> 1: The node is already in open_set and there's a better path than the current one
                # Control flag -> 0: The node isn't in open_set or it's in, but the current path is better
                if control_flag == 1:
                    pass
                else:
                    neighbor.g = temp_g
                    neighbor.h = AStar.h_score(neighbor, end)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.previous = current_node
                    open_set.append(neighbor)

        return open_set, closed_set, current_node, final_path[:-1]

    @staticmethod
    def find_treasures(self, open_set, closed_set, current_node, treasures_list):
        self.searched_nodes += 1
        best_way = 0
        # Find the node with the best f in open_set
        for i in range(len(open_set)):
            if open_set[i].f < open_set[best_way].f:
                best_way = i

        current_node = open_set[best_way]
        final_path = []
        price = 0
        # Ends if current_node is a treasure
        if((current_node.x, current_node.y) in treasures_list):
            price = current_node.g
            temp = current_node
            final_path.append(temp)
            while temp.previous:
                final_path.append(temp.previous)
                temp = temp.previous

        # Remove current_node from open_set
        open_set = AStar.clean_open_set(open_set, current_node)
        # Add the current_node to closed_set
        closed_set.append(current_node)
        # Go through all neighbours of current_node
        neighbors = current_node.neighbors
        for neighbor in neighbors:
            # Skip node if its closed or an obstacle
            if (neighbor in closed_set) or (neighbor.obstacle):
                continue
            else:
                if labyrinth[neighbor.x][neighbor.y] > 0:
                    temp_g = current_node.g + labyrinth[neighbor.x][neighbor.y]
                else:
                    temp_g = current_node.g
                control_flag = 0
                for k in range(len(open_set)):
                    # Checks if neighbour is in open_set
                    if neighbor.x == open_set[k].x and neighbor.y == open_set[k].y:
                        # Checks if the current path is better (smaller g)
                        if temp_g < open_set[k].g:
                            # Create f, g, h values
                            open_set[k].g = temp_g
                            # Calculate the lowest h_score of all treasures
                            min_h = sys.maxsize
                            for treasure in treasures:
                                temp_h = AStar.h_score(neighbor, Node(treasure[0], treasure[1]))
                                if temp_h < min_h:
                                    min_h = temp_h
                            neighbor.h = min_h
                            open_set[k].f = open_set[k].g + open_set[k].h
                            open_set[k].previous = current_node
                        else:
                            pass
                        control_flag = 1

                # Control flag -> 1: The node is already in open_set and there's a better path than the current one
                # Control flag -> 0: The node isn't in open_set or it's in, but the current path is better
                if control_flag == 1:
                    pass
                else:
                    neighbor.g = temp_g
                    # Calculate the lowest h_score of all treasures
                    min_h = sys.maxsize
                    for treasure in treasures:
                        temp_h = AStar.h_score(neighbor, Node(treasure[0], treasure[1]))
                        if temp_h < min_h:
                            min_h = temp_h
                    neighbor.h = min_h
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.previous = current_node
                    open_set.append(neighbor)

        return open_set, closed_set, current_node, final_path[:-1], price

    @staticmethod
    def treasure_path(self, startNode, treasures_list): # Finds the path to the nearest and least costly treasure
        open_set = []
        closed_set = []
        current_node = None
        final_path = []
        open_set.append(startNode)
        while len(open_set) > 0:
            open_set, closed_set, current_node, final_path, price = AStar.find_treasures(self, open_set, closed_set, current_node, treasures_list)
            if len(final_path) > 0:
                break
        return final_path, price

    def main(self):
        # Create empty grid
        grid = AStar.create_grid(self.cols, self.rows)
        # Fill the grid with nodes
        grid = AStar.fill_grids(grid, self.cols, self.rows, self.labyrinth)
        # Set neighbours for every node in grid
        grid = AStar.get_neighbors(grid, self.cols, self.rows)
        startNode = grid[self.start[0]][self.start[1]]
        final_path = [startNode]
        treasures_list = treasures
        final_price = 0
        # Finds the path to all the treasures
        for _ in range(len(treasures)):
            # Finds the path to the closest treasure and saves it to final_path
            path, price = AStar.treasure_path(self, startNode, treasures_list)
            final_path = path + final_path
            final_price += price
            first_element = final_path[0]
            treasures_list.remove((first_element.x, first_element.y))
            startNode = Node(first_element.x, first_element.y)
            startNode.add_neighbors(grid, self.cols, self.rows)
        open_set = []
        closed_set = []
        current_node = None
        end_path = []
        self.end = grid[self.end[0]][self.end[1]]
        # Add the starting node to open_set
        open_set.append(startNode)
        # Set end as a node instead of coordinates
        while len(open_set) > 0:
            open_set, closed_set, current_node, end_path = AStar.start_path(self, open_set, closed_set, current_node, self.end)
            if len(end_path) > 0:
                break
        final_path = end_path + final_path
        final_price += final_path[0].g
        return final_path[::-1], final_price

class IDAStar:

    def __init__(self, cols, rows, start, end, labyrinth, treasures):
        self.cols = cols
        self.rows = rows
        self.start = start
        self.end = end
        self.labyrinth = labyrinth
        self.treasures = treasures
        self.final_price = 0
        self.depth = 0
        self.next_min_bound = sys.maxsize
        self.current_bound = 0
        self.searched_nodes = 0

    @staticmethod
    def h_score(current_node, end):
        distance = abs(current_node.x - end.x) + abs(current_node.y - end.y) # Manhattan metoda
        return distance

    @staticmethod
    def create_grid(cols, rows):
        grid = []
        for _ in range(cols):
            grid.append([])
            for _ in range(rows):
                grid[-1].append(0)
        return grid

    @staticmethod
    def fill_grids(grid, cols, rows, labyrinth):
        for i in range(cols):
            for j in range(rows):
                grid[i][j] = Node(i, j)
                if labyrinth[i][j] == -1:
                    grid[i][j].obstacle = True
        return grid

    @staticmethod
    def get_neighbors(grid, cols, rows):
        for i in range(cols):
            for j in range(rows):
                # Add neighbours for all nodes in grid
                grid[i][j].add_neighbors(grid, cols, rows)
        return grid

    @staticmethod
    def search(self, start_state, goal, visited, remove_treasure):
        visited.append(start_state)
        self.searched_nodes += 1
        #print("Current parent", start_state.x, start_state.y)

        if start_state.f > self.current_bound and start_state.f < self.next_min_bound:
            self.next_min_bound = start_state.f

        if start_state.f > self.current_bound:
            return False

        final_path = []
        if start_state == goal:
            temp = start_state
            final_path.append(temp)
            while temp.previous:
                final_path.append(temp.previous)
                if (labyrinth[temp.x][temp.y]>0):
                    self.final_price += labyrinth[temp.x][temp.y]
                temp = temp.previous
            return final_path[::-1]


        else:
            val = False
            neighbors = start_state.neighbors
            for neighbor in neighbors:
                if neighbor.obstacle:
                    continue
                if neighbor not in visited and val is False:
                    if (neighbor.x, neighbor.y) == remove_treasure:
                        continue
                    neighbor.g = start_state.g + labyrinth[neighbor.x][neighbor.y]
                    neighbor.h = IDAStar.h_score(neighbor, self.end)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.previous = start_state
                    val = IDAStar.search(self, neighbor, goal, visited, remove_treasure)
            if val:
                return val
            return False

    @staticmethod
    def search_treasures(self, start_state, treasures, visited, remove_treasure):
        visited.append(start_state)
        self.searched_nodes += 1
        #print("Current parent", start_state.x, start_state.y)

        if start_state.f > self.current_bound and start_state.f < self.next_min_bound:
            self.next_min_bound = start_state.f
            start_state.bound = True

        if start_state.f > self.current_bound:
            return False

        final_path = []
        if (start_state.x, start_state.y) in treasures:
            temp = start_state
            final_path.append(temp)
            while temp.previous:
                final_path.append(temp.previous)
                if (labyrinth[temp.x][temp.y]>0):
                    self.final_price += labyrinth[temp.x][temp.y]
                temp = temp.previous
            return final_path[::-1]

        else:
            val = False
            neighbors = start_state.neighbors
            for neighbor in neighbors:
                if neighbor.obstacle:
                    continue
                if neighbor not in visited and val is False:
                    if (neighbor.x, neighbor.y) == remove_treasure:
                        continue
                    neighbor.g = start_state.g + labyrinth[neighbor.x][neighbor.y]
                    min_h = sys.maxsize
                    # Check all treasures for the one with the best h_score
                    for treasure in treasures:
                        temp_h = IDAStar.h_score(neighbor, Node(treasure[0], treasure[1]))
                        if temp_h < min_h:
                            min_h = temp_h
                    neighbor.h = min_h
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.previous = start_state
                    val = IDAStar.search_treasures(self, neighbor, treasures, visited, remove_treasure)
            if val:
                return val
            return False

    def main(self):
        # Create empty grid
        grid = AStar.create_grid(self.cols, self.rows)
        # Fill the grid with nodes
        grid = AStar.fill_grids(grid, self.cols, self.rows, self.labyrinth)
        # Set neighbours for every node in grid
        grid = AStar.get_neighbors(grid, self.cols, self.rows)
        startNode = grid[self.start[0]][self.start[1]]
        self.end = grid[self.end[0]][self.end[1]]
        final_path = [startNode]
        visited = []
        treasures_list = treasures
        min_h = sys.maxsize
        for treasure in treasures:
            temp_h = IDAStar.h_score(startNode, Node(treasure[0], treasure[1]))
            if temp_h < min_h:
                min_h = temp_h
        startNode.h = min_h
        startNode.f = startNode.h
        self.current_bound = startNode.f
        startNode.bound = True
        # In first iteration checks for start
        remove_treasure = (startNode.x, startNode.y)
        # Finds the best path between all treasures
        for i in range(len(treasures_list)):
            print("Treasure n.", i+1)
            val = False
            while not val:
                self.depth += 1
                print("Current bound---------------------------------------------------------------------", self.current_bound)
                val = IDAStar.search_treasures(self, startNode, treasures_list, visited, remove_treasure)
                if not val:
                    visited = []
                self.current_bound = self.next_min_bound
                self.next_min_bound = sys.maxsize
            final_path += val[1:]
            first_element = val[-1]
            startNode = Node(first_element.x, first_element.y)
            startNode.add_neighbors(grid, self.cols, self.rows)
            self.current_bound = startNode.f
            remove_treasure = (first_element.x, first_element.y)
            treasures_list.remove(remove_treasure)
            min_h = sys.maxsize
            for treasure in treasures_list:
                temp_h = IDAStar.h_score(startNode, Node(treasure[0], treasure[1]))
                if temp_h < min_h:
                    min_h = temp_h
            startNode.h = min_h
            startNode.f = startNode.h
        print("Found all treasures, now searching the end")
        startNode.h = IDAStar.h_score(startNode, self.end)
        startNode.f = startNode.h
        val = False
        while not val:
            self.depth += 1
            print("Current bound---------------------------------------------------------------------", self.current_bound)
            val = IDAStar.search(self, startNode, self.end, visited, remove_treasure)
            if not val:
                visited = []
            self.current_bound = self.next_min_bound
            self.next_min_bound = sys.maxsize
        final_path += val[1:]
        return final_path

class IDDFS:

    def __init__(self, cols, rows, start, end, labyrinth, treasures):
        self.cols = cols
        self.rows = rows
        self.start = start
        self.end = end
        self.labyrinth = labyrinth
        self.treasures = treasures
        self.final_price = 0
        self.depth = 0
        self.searched_nodes = 0

    @staticmethod
    def create_grid(cols, rows):
        grid = []
        for _ in range(cols):
            grid.append([])
            for _ in range(rows):
                grid[-1].append(0)
        return grid

    @staticmethod
    def fill_grids(grid, cols, rows, labyrinth):
        for i in range(cols):
            for j in range(rows):
                grid[i][j] = Node(i, j)
                if labyrinth[i][j] == -1:
                    grid[i][j].obstacle = True
        return grid

    @staticmethod
    def get_neighbors(grid, cols, rows):
        for i in range(cols):
            for j in range(rows):
                # Add neighbours for all nodes in grid
                grid[i][j].add_neighbors(grid, cols, rows)
        return grid

    @staticmethod
    def search(self, start_state, goal, depth, visited, remove_treasure):
        visited.append(start_state)
        self.searched_nodes += 1
        #print("Current parent", start_state.x, start_state.y)

        final_path = []
        if start_state == goal:
            temp = start_state
            final_path.append(temp)
            while temp.previous:
                final_path.append(temp.previous)
                if (labyrinth[temp.x][temp.y]>0):
                    self.final_price += labyrinth[temp.x][temp.y]
                temp = temp.previous
            return final_path[::-1]
        elif depth == 0:
            return False

        else:
            val = False
            neighbors = start_state.neighbors
            for neighbor in neighbors:
                if neighbor.obstacle:
                    continue
                if neighbor not in visited and val is False:
                    if (neighbor.x, neighbor.y) == remove_treasure:
                        continue
                    neighbor.previous = start_state
                    val = IDDFS.search(self, neighbor, goal, depth - 1, visited, remove_treasure)
            if val:
                return val
            return False

    @staticmethod
    def search_treasures(self, start_state, treasures, depth, visited, remove_treasure):
        visited.append(start_state)
        self.searched_nodes += 1
        #print("Current parent", start_state.x, start_state.y)

        final_path = []
        if (start_state.x, start_state.y) in treasures:
            temp = start_state
            final_path.append(temp)
            while temp.previous:
                final_path.append(temp.previous)
                if (labyrinth[temp.x][temp.y]>0):
                    self.final_price += labyrinth[temp.x][temp.y]
                temp = temp.previous
            return final_path[::-1]
        elif depth == 0:
            return False

        else:
            val = False
            neighbors = start_state.neighbors
            for neighbor in neighbors:
                if neighbor.obstacle:
                    continue
                if neighbor not in visited and val is False:
                    if (neighbor.x, neighbor.y) == remove_treasure:
                        continue
                    else:
                        neighbor.previous = start_state
                    val = IDDFS.search_treasures(self, neighbor, treasures, depth - 1, visited, remove_treasure)
            if val:
                return val
            return False

    def main(self):
        # Create empty grid
        grid = AStar.create_grid(self.cols, self.rows)
        # Fill the grid with nodes
        grid = AStar.fill_grids(grid, self.cols, self.rows, self.labyrinth)
        # Set neighbours for every node in grid
        grid = AStar.get_neighbors(grid, self.cols, self.rows)
        startNode = grid[self.start[0]][self.start[1]]
        self.end = grid[self.end[0]][self.end[1]]
        final_path = [startNode]
        visited = []
        depth = 1
        treasures_list = treasures
        # In first iteration checks for start
        remove_treasure = (startNode.x, startNode.y)
        for _ in range(len(treasures_list)):
            val = False
            while not val:
                self.depth += 1
                print("Depth---------------------------------------------------------------------", self.depth)
                val = IDDFS.search_treasures(self, startNode, treasures_list, depth, visited, remove_treasure)
                if not val:
                    visited = []
                depth += 1
            depth = 1
            final_path += val[1:]
            first_element = val[-1]
            startNode = Node(first_element.x, first_element.y)
            startNode.add_neighbors(grid, self.cols, self.rows)
            remove_treasure = (first_element.x, first_element.y)
            treasures_list.remove(remove_treasure)
        val = False
        while not val:
            self.depth += 1
            print("Depth---------------------------------------------------------------------", self.depth)
            val = IDDFS.search(self, startNode, self.end, depth, visited, remove_treasure)
            if not val:
                visited = []
            depth += 1
        final_path += val[1:]
        return final_path

labyrinth = read_file("labyrinth_9.txt")
start_end_treasures = find_start_end_treasures(labyrinth)
start = start_end_treasures[0]
end = start_end_treasures[1]
treasures = start_end_treasures[2]

start_time = time.time()
tracemalloc.start()

# a_star = AStar(len(labyrinth[0]),  len(labyrinth), (start[0], start[1]), (end[0], end[1]), labyrinth, treasures)
# final_path, final_price = a_star.main()
# searched_nodes = a_star.searched_nodes

# greedy_best_search = GreedyBestSearch(len(labyrinth[0]),  len(labyrinth), (start[0], start[1]), (end[0], end[1]), labyrinth, treasures)
# final_path, final_price = greedy_best_search.main()
# searched_nodes = greedy_best_search.searched_nodes

# iddfs = IDDFS(len(labyrinth[0]),  len(labyrinth), (start[0], start[1]), (end[0], end[1]), labyrinth, treasures)
# final_path = iddfs.main()
# final_price = iddfs.final_price
# searched_nodes = iddfs.searched_nodes


ida_star = IDAStar(len(labyrinth[0]), len(labyrinth), (start[0], start[1]), (end[0], end[1]), labyrinth, treasures)
final_path = ida_star.main()
final_price = ida_star.final_price
searched_nodes = ida_star.searched_nodes


memory_consumption = tracemalloc.get_tracemalloc_memory()
end_time = time.time()

tracemalloc.stop()

x_values = []
y_values = []
if len(final_path) > 0:
    print("Path:")
    price = 0
    for node in final_path:
        price += node.g
        x_values.append(node.x + 0.5)
        y_values.append(node.y + 0.5)
        print(f"({node.x}, {node.y})")
    print("Price:", final_price)
    print("Moves:", len(final_path)-1)
    print("Searched nodes:", searched_nodes)
    print("Used memory:", memory_consumption, "bytes")
    print("Search time:", end_time - start_time)
else:
    print("There is no legal way...")


# Display labyrinth
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_aspect('equal', adjustable='box')

plt.plot(y_values, x_values, label='Path')

maze = []
for i, line in enumerate(labyrinth):
    row = []
    for j, c in enumerate(line):
        if c == -1:
            row.append(0)  # walls are 0s
        else:
            row.append(1)  # walkable are 1s
            if c > 0:
                plt.text(j+0.3, i+0.6, c)

    maze.append(row)
point1 = [1.5, 1.5]
point2 = [1.5, 3.5]

treasures = find_start_end_treasures(labyrinth)[2]
x_treasures = []
y_treasures = []

for treasure in treasures:
    x_treasures.append(treasure[0] + 0.5)
    y_treasures.append(treasure[1] + 0.5)

x2 = 9.5
y2 = 3.5

plt.xticks([]) # remove the tick marks by setting to an empty list
plt.yticks([]) # remove the tick marks by setting to an empty list
plt.plot(final_path[0].y+0.5, final_path[0].x+0.5, "o", label='Start')
plt.plot(final_path[-1].y+0.5, final_path[-1].x+0.5, 'o', label='End')
ax=plt.gca()
ax.invert_yaxis()
plt.plot(y_treasures, x_treasures, 'o', label='Treasure')

plt.pcolormesh(maze)
plt.legend()
plt.show()


