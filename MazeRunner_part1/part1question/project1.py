import numpy as np
import queue
import math
import time
import matplotlib.pyplot as plt


class Maze:
    def __init__(self, size, prob):
        """
        Create a new maze
        param size(int): the size of maze
        param prob(double): the probability the cell to be occupied
        return: a maze(n by n matrix) with cells being filled or empty
        """
        self.size = size
        self.prob = prob

        # check if prob between 0 and 1
        if prob < 0 or prob > 1:
            raise ValueError('prob should between 0 and 1')

        # create a uniform distribution matrix
        self.maze = np.random.uniform(low=0, high=1, size=[size, size])
        # generate maze matrix, '0':empty '1':filled
        self.maze = (self.maze < prob).astype(int)

        self.maze[0, 0] = 0
        self.maze[size - 1, size - 1] = 0

        # dictionary of solution
        self.solution = dict(
            find_path_or_not='',
            number_of_nodes_visited=0,
            visited_nodes={},
            path_length=0,
            path=[]
        )

    def in_maze(self, node):
        """
        check if neighbors are in the maze
        param mode: the coordinate of the node
        return: True or False
        """
        return (0 <= node[0] < self.size) and (0 <= node[1] < self.size)

    def if_empty(self, node):
        """
        check if the node is empty
        param node: the coordinate of the node
        return: True of False
        """
        return self.maze[node[0], node[1]] == 0

    def neighbor(self, node):
        """
        find neighbor nodes
        param node: the coordinate of a node
        return: neighbors of the input node
        """
        # search directions: down > right > left > up
        possible_neighbor = [(node[0] + 1, node[1]), (node[0], node[1] - 1), (node[0] - 1, node[1]),
                             (node[0], node[1] + 1)]
        neighbors = set()
        for a_node in possible_neighbor:
            if self.in_maze(a_node) and self.if_empty(a_node):
                neighbors.add(a_node)
        return neighbors

    def print_maze(self):
        """
        print the maze as a matrix
        """
        print(self.maze)

    def print_path(self):
        '''
        print path and visited nodes on the maze
        2 means visited nodes and 3 means path
        '''
        _maze = self.maze.copy()
        for node in self.solution['visited_nodes']:
            _maze[node[0], node[1]] = 2

        for node in self.solution['path']:
            _maze[node[0], node[1]] = 3

        print(_maze)


class SolveMaze:
    def __init__(self, maze):

        self.maze = maze
        self.start_point = (0, 0)
        self.end_point = (maze.size - 1, maze.size - 1)

    def buildpath(self, parent):
        """
        build a path form end to start
        param parent: dictionary of parents
        return: a path
        """
        path = []

        current_node = self.end_point

        while current_node != self.start_point:
            path.append(current_node)
            current_node = parent[current_node]
        path.append(current_node)
        return path[::-1]

    def dfs(self):
        """
        using depth first search to find a path
        store result in maze.solution dictionary
        """
        visited = set()  # to record visited nodes
        parent = {}  # to record the parent of each visited node
        path = []

        stack = []
        stack.append(self.start_point)
        visited.add(self.start_point)
        while stack:
            curnode = stack.pop()
            # visited.add(curnode)
            if (curnode == self.end_point):
                path = self.buildpath(parent)
                # print(visited)
                self.maze.solution = dict(find_path_or_not="YES",
                                          number_of_nodes_visited=len(visited),
                                          visited_nodes=visited,
                                          path_length=len(path),
                                          path=path)
                return self.maze.solution

            direction = [(0, 1), (1, 0), (-1, 0), (0, -1)]
            for x, y in direction:
                nextnode = (curnode[0] + x, curnode[1] + y)
                if (self.maze.in_maze(nextnode) and nextnode not in visited and self.maze.if_empty(nextnode)):
                    # print(nextnode)
                    parent[nextnode] = curnode
                    stack.append(nextnode)
                    visited.add(nextnode)

        self.maze.solution = dict(find_path_or_not="NO",
                                  number_of_nodes_visited=len(visited),
                                  visited_nodes=visited,
                                  path_length=len(path),
                                  path=path)
        return self.maze.solution

    def bfs(self):
        """
        using breath first search to find a path
        store result in maze.solution dictionary
        """
        visited = set()  # to record visited nodes
        parent = {}  # to record the parent of each visited node
        path = []

        stack = []
        stack.append(self.start_point)
        # visited.add(self.start_point)
        while stack:
            curnode = stack.pop(0)
            # visited.add(curnode)
            if (curnode == self.end_point):
                path = self.buildpath(parent)
                # print(visited)
                self.maze.solution = dict(find_path_or_not="YES",
                                          number_of_nodes_visited=len(visited),
                                          visited_nodes=visited,
                                          path_length=len(path),
                                          path=path)
                return

            direction = [(0, 1), (1, 0), (-1, 0), (0, -1)]
            for x, y in direction:
                nextnode = (curnode[0] + x, curnode[1] + y)
                if (self.maze.in_maze(nextnode) and nextnode not in visited and self.maze.if_empty(nextnode)):
                    # print(nextnode)
                    parent[nextnode] = curnode
                    stack.append(nextnode)
                    visited.add(nextnode)

        self.maze.solution = dict(find_path_or_not="NO",
                                  number_of_nodes_visited=len(visited),
                                  visited_nodes=visited,
                                  path_length=len(path),
                                  path=path)
        return self.maze.solution

    def a_star_euclidean(self):
        """
        using A* with Euclidean Distance to be heuristic to find a path
        store result in maze.solution dictionary
        """
        visited = set()
        parent = {}
        path = []

        _queue = queue.PriorityQueue()
        current_cost = {}

        _queue.put((0, self.start_point))
        visited.add(self.start_point)
        current_cost[self.start_point] = 0

        while not _queue.empty():
            current_node = _queue.get()
            coordinate_current_node = current_node[1]
            if coordinate_current_node == self.end_point:
                path = self.buildpath(parent)
                self.maze.solution = dict(find_path_or_not="YES",
                                          number_of_nodes_visited=len(visited),
                                          visited_nodes=visited,
                                          path_length=len(path),
                                          path=path)
                return
            for child_node in self.maze.neighbor(coordinate_current_node):
                next_cost = current_cost[coordinate_current_node] + 1
                if child_node not in visited:
                    current_cost[child_node] = next_cost
                    parent[child_node] = coordinate_current_node
                    visited.add(child_node)
                    # cost so far + h
                    h = math.sqrt(
                        (child_node[0] - self.end_point[0]) ** 2 +
                        (child_node[1] - self.end_point[1]) ** 2
                    )

                    total_cost = h + next_cost
                    _queue.put((total_cost, child_node))

        self.maze.solution = dict(find_path_or_not="NO",
                                  number_of_nodes_visited=len(visited),
                                  visited_nodes=visited,
                                  path_length=len(path),
                                  path=path)
        return self.maze.solution

    def a_star_manhattan(self):
        """
        using A* with Manhattan Distance to be heuristic to find a path
        store result in maze.solution dictionary
        """
        visited = set()
        parent = {}
        path = []

        _queue = queue.PriorityQueue()
        current_cost = {}

        _queue.put((0, self.start_point))
        visited.add(self.start_point)
        current_cost[self.start_point] = 0

        while not _queue.empty():
            current_node = _queue.get()
            coordinate_current_node = current_node[1]
            if coordinate_current_node == self.end_point:
                path = self.buildpath(parent)
                self.maze.solution = dict(find_path_or_not="YES",
                                          number_of_nodes_visited=len(visited),
                                          visited_nodes=visited,
                                          path_length=len(path),
                                          path=path)
                return
            for child_node in self.maze.neighbor(coordinate_current_node):
                next_cost = current_cost[coordinate_current_node] + 1
                if child_node not in visited:
                    current_cost[child_node] = next_cost
                    parent[child_node] = coordinate_current_node
                    visited.add(child_node)
                    # cost so far + h
                    h = abs(child_node[0] - self.end_point[0]) + abs(child_node[1] - self.end_point[1])
                    total_cost = h + next_cost
                    _queue.put((total_cost, child_node))

        self.maze.solution = dict(find_path_or_not="NO",
                                  number_of_nodes_visited=len(visited),
                                  visited_nodes=visited,
                                  path_length=len(path),
                                  path=path)
        return self.maze.solution

    def run(self, method):
        if method == "dfs":
            print("dfs:")

            # t0 = time.clock()
            self.dfs()
            # print(self.maze.solution)
            # self.maze.print_path()
            # print("consumed time:")
            # print(time.clock() - t0)

        elif method == "bfs":
            print("bfs:")

            # t0 = time.clock()
            self.bfs()
            print(self.maze.solution)
            self.maze.print_path()
            # print("consumed time:")
            # print(time.clock() - t0)

        elif method == "a_stareuclidean":
            print("a_stareuclidean:")

            # t0 = time.clock()
            self.a_star_euclidean()
            print(self.maze.solution)
            self.maze.print_path()
            # print("consumed time:")
            # print(time.clock() - t0)
        elif method == "a_starmanhnttan":
            print("a_starmanhnttan:")

            # t0 = time.clock()
            self.a_star_manhattan()
            print(self.maze.solution)
            self.maze.print_path()
            # print("consumed time:")
            # print(time.clock() - t0)
        else:
            raise ValueError("wrong method")

        return self.maze.solution


if __name__ == "__main__":
    maze1 = Maze(15, 0.2)
    # maze1.print_maze()
    solution = SolveMaze(maze1)
    solution.run("dfs")
    solution.run("bfs")
    solution.run("a_stareuclidean")
    solution.run("a_starmanhnttan")
