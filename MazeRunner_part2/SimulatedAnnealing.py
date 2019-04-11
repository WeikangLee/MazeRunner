import random
import math
import part1


class SimulatedAnnealing:
    def __init__(self, a_maze):
        """
        :param a_maze: Maze object
        """
        self.a_maze = a_maze

    def sa(self, temperature, cool, threshold,  prob, algorithm, objective):
        # def sa(self,temperature,cool, prob,algorithms,target):
        """
        :param temperature: Temperature
        :param cool: coefficient
        :param prob: probability of an empty node to be filled or a filled node to become empty
        :param algorithm: search algorithms
        :param objective: Objective function
        :param threshold: threshold
        :return:
        """
        # count how many times that we want to take risks
        taking_risks = 0

        # number of total iterations
        i = 0

        # difference of cost between original cost and new cost
        dE = 0

        # To make sure that the maze is solvable, if not, create a new one, until the maze is solvable
        test_solver = part1.SolveMaze(self.a_maze)
        test_solver.a_star_euclidean()
        while self.a_maze.solution['path_length'] == 0:
            another_maze = part1.Maze(self.a_maze.size, self.a_maze.prob)
            self.a_maze.maze = another_maze.maze.copy()
            test_solver.a_star_euclidean()
            print('this is a new maze may be solvable!')

        new_maze = part1.Maze(self.a_maze.size, 0)

        while temperature > threshold:

            # # original maze，cost
            # a_solver = part1.SolveMaze(self.a_maze)
            # a_solver.dfs()
            # a_cost = self.a_maze.solution['path_length']
            #
            # # next step (new maze that changed from former one)
            new_maze.maze = self.new_maze_to_one_or_zero(prob)
            #
            # # make a new step (new maze) and new cost
            # new_solver = part1.SolveMaze(new_maze)
            # new_solver.dfs()
            # new_cost = new_maze.solution['path_length']

            a_cost, new_cost = self.cost_calculator(new_maze, algorithm, objective)

            # strategy of taking next step
            if new_cost > 0:   # to make sure that new maze is solvable
                dE = a_cost - new_cost

                if dE < 0:     # which means that new maze is harder to solve
                    self.a_maze.maze = new_maze.maze.copy()

                # which means that new maze is easier to solve, but we still want to take a risk in some cases
                elif dE > 0 and math.exp((-dE)/temperature) >= random.uniform(0, 1):
                    self.a_maze.maze = new_maze.maze.copy()
                    taking_risks = taking_risks + 1
                    print('take risks time: ', taking_risks)
                    print('the possibility is', 100 * math.exp((-dE) / temperature), '% ')
                    print('Iteration:', i, ' current cost: ', a_cost)

            # to cool the temperature
            temperature = temperature - cool

            # print the maze to show the path, and the cost
            if i % 400 == 0:
                self.a_maze.print_path()
                print('Iteration:', i, ' current cost: ', a_cost)

            i = i + 1
        print('Total number of iterations:', i)

    def cost_calculator(self, new_maze, algorithm, objective):
        """
        to calculate the cost of different algorithms and properties
        :param new_maze:  new maze
        :param algorithm: search algorithms
        :param objective: properties
        :return:
        """
        # solver
        a_solver = part1.SolveMaze(self.a_maze)
        new_solver = part1.SolveMaze(new_maze)

        if algorithm == 'dfs':
            a_solver.dfs()
            new_solver.dfs()
            if objective == 'path_length':
                a_cost = self.a_maze.solution['path_length']
                new_cost = new_maze.solution['path_length']

            elif objective == 'number_of_nodes_visited':
                a_cost = self.a_maze.solution['number_of_nodes_visited']
                new_cost = new_maze.solution['number_of_nodes_visited']
            elif objective == 'max_fringe_size':
                a_cost = self.a_maze.solution['max_fringe_size']
                new_cost = new_maze.solution['max_fringe_size']
            else:
                raise Exception('Wrong properties!')

        elif algorithm == 'bfs':
            a_solver.bfs()
            new_solver.bfs()
            if objective == 'path_length':
                a_cost = self.a_maze.solution['path_length']
                new_cost = new_maze.solution['path_length']

            elif objective == 'number_of_nodes_visited':
                a_cost = self.a_maze.solution['number_of_nodes_visited']
                new_cost = new_maze.solution['number_of_nodes_visited']
            elif objective == 'max_fringe_size':
                a_cost = self.a_maze.solution['max_fringe_size']
                new_cost = new_maze.solution['max_fringe_size']
            else:
                raise Exception('Wrong properties!')

        elif algorithm == 'a_star_euclidean':
            a_solver.a_star_euclidean()
            new_solver.a_star_euclidean()
            if objective == 'path_length':
                a_cost = self.a_maze.solution['path_length']
                new_cost = new_maze.solution['path_length']

            elif objective == 'number_of_nodes_visited':
                a_cost = self.a_maze.solution['number_of_nodes_visited']
                new_cost = new_maze.solution['number_of_nodes_visited']
            elif objective == 'max_fringe_size':
                a_cost = self.a_maze.solution['max_fringe_size']
                new_cost = new_maze.solution['max_fringe_size']
            else:
                raise Exception('Wrong properties!')

        elif algorithm == 'a_star_manhattan':
            a_solver.a_star_manhattan()
            new_solver.a_star_manhattan()
            if objective == 'path_length':
                a_cost = self.a_maze.solution['path_length']
                new_cost = new_maze.solution['path_length']

            elif objective == 'number_of_nodes_visited':
                a_cost = self.a_maze.solution['number_of_nodes_visited']
                new_cost = new_maze.solution['number_of_nodes_visited']
            elif objective == 'max_fringe_size':
                a_cost = self.a_maze.solution['max_fringe_size']
                new_cost = new_maze.solution['max_fringe_size']
            else:
                raise Exception('Wrong properties!')

        else:
            raise Exception('No Such Algorithms, May Be Next Year!')

        return a_cost, new_cost

    def new_maze_to_one(self, prob):
        """
        :param old_maze: maze to be changed
        :param prob: probability of an empty node to be filled
        :return:new generated maze
        """
        new_maze = self.a_maze.maze.copy()
        x, y = self.random_location()

        if random.randint(1, 100) <= prob:
            new_maze[x][y] = 1

        possible_neighbor = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        for (x1, y1) in possible_neighbor:
            if self.in_maze((x1, y1)):
                if self.is_empty((x1, y1)):
                    if random.randint(1, 100) <= prob:
                        new_maze[x1][y1] = 1

        return new_maze

    def new_maze_to_one_or_zero(self, prob):
        """
        :param prob: probability of an empty node to be filled or a filled node to become empty
        :return: new generated maze
        """
        new_maze = self.a_maze.maze.copy()
        x, y = self.random_location()

        if self.is_empty((x, y)):
            if random.randint(1, 100) <= prob:
                new_maze[x][y] = 1
        else:
            if random.randint(1, 100) <= prob:
                new_maze[x][y] = 0

        possible_neighbor = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        for (x1, y1) in possible_neighbor:
            if self.in_maze((x1, y1)):
                if self.is_empty((x1, y1)):
                    if self.is_empty((x1, y1)):
                        if random.randint(1, 100) <= prob:
                            new_maze[x1][y1] = 1
                    else:
                        if random.randint(1, 100) <= prob:
                            new_maze[x1][y1] = 0
        return new_maze

    def random_location(self):
        """
        to find a random location that not start or end point
        :return:
        """
        x = random.randint(0, self.a_maze.size - 1)
        y = random.randint(0, self.a_maze.size - 1)

        while x == y == 0 or x == y == (self.a_maze.size - 1):
            x = random.randint(0, self.a_maze.size - 1)
            y = random.randint(0, self.a_maze.size - 1)

        return x, y

    def in_maze(self, node):
        """
        check if neighbors are in the maze and not start and end point
        :param node: the coordinate of the node
        :return: True or False
        """
        if (0 <= node[0] < len(self.a_maze.maze)) and (0 <= node[1] < self.a_maze.size):
            if not (node[0] == node[1] == 0 or node[0] == node[1] == self.a_maze.size-1):
                return True
        return False

    def is_empty(self, node):
        """
        check if the node is empty
        :param node: the coordinate of the node
        :param maze: Maze object
        :return: True of False
        """
        return self.a_maze.maze[node[0], node[1]] == 0

    def num_filled(self, maze):
        """
        the percentage of node that has been filled
        :return: percentage
        """
        num = 0
        for x1 in range(self.a_maze.size):
            for y1 in range(self.a_maze.size):
                if maze.maze[x1][y1] == 1:
                    num = num + 1

        return num/(self.a_maze.size * self.a_maze.size)


if __name__ == "__main__":
    maze = part1.Maze(30, 0.3)

    sa = SimulatedAnnealing(maze)
    sa.sa(0.05, 0.000002, 0.007145, 80, 'a_star_manhattan', 'max_fringe_size')

    # 0.5, 0.00002, 0.1429  dfs  number_of_nodes_visited

    # 1, 0.0001, 0.1429, 60, is a good choice for dfs and path length path_length
    """
    0.05, 0.000002, 0.007145 max_fringe_size
    """





