import random
import math
import part1
import copy
import numpy as np


class geneticalgorithm:

    def __init__(self,size,prob,num,properties,method,generation=3):
        self.size = size
        self.properties = properties
        self.prob = prob
        self.num = num
        self.child = part1.Maze(self.size,self.prob)
        self.generation = generation
        self.new_maze = []
        self.chromsome = []
        self.children = []
        self.method = method
        self.rep = 0

    def get_chromsome(self):

        for i in range(self.num):
            gen_maze = part1.Maze(self.size,self.prob)
            if self.fitness(gen_maze) > 0:
                self.chromsome.append(gen_maze)
        self.chromsome.sort(key=lambda x: x.solution[self.properties],reverse=False)
        self.chromsome = self.chromsome[-20:]

        '''
        for each in chromsome:
            print(each.maze)
            print(each.solution["path_length"])
            '''
        return self.chromsome

    def reproduce(self):
        self.chromsome.sort(key=lambda x: x.solution[self.properties],reverse=False)
        self.chromsome = self.chromsome[-20:]
        global rep
        # child=zeros(self.size,self.size)
        parents = copy.deepcopy(self.chromsome)
        for k in range(0,len(parents) - 1,2):
            cros = random.randint(1,self.size - 1)
            parent1 = copy.deepcopy(self.chromsome[k])
            parent2 = copy.deepcopy(self.chromsome[k + 1])
            childtemp = part1.Maze(self.size,self.prob)
            for i in range(0,cros):
                childtemp.maze[i] = parent1.maze[i]

            for i in range(cros,self.size - 1):
                childtemp.maze[i] = parent2.maze[i]

            mazetemp2 = copy.deepcopy(self.child.maze)

            for i in range(0,self.size):
                for j in range(0,random.randint(1,self.size - 1)):
                    self.child.maze[i][j] = mazetemp2[i][self.size - 1 - j]

            self.mutation(childtemp)
            fitness1 = self.fitness(childtemp)
            fitness2 = self.fitness(parent1)
            fitness3 = self.fitness(parent2)

            if (fitness1 <= fitness2 or fitness1 <= fitness3):
                if fitness2 >= fitness3:
                    self.children.append(parent1)
                else:
                    self.children.append(parent2)

            else:
                self.children.append(childtemp)
                self.chromsome.append(childtemp)

        self.children.sort(key=lambda x: x.solution[self.properties],reverse=False)
        # print(self.children)
        self.child = copy.deepcopy(self.children[len(self.children) - 1])
        print("*************************************")
        print(self.child.solution[self.properties])
        return self.child

    def mutation(self,maze):
        if random.random() < 0.3:
            x = random.randint(0,self.size - 1)
            y = random.randint(0,self.size - 1)

            while x == y == 0 or x == y == (self.size - 1):
                x = random.randint(0,self.size - 1)
                y = random.randint(0,self.size - 1)

            maze.maze[x][y] = 1

    def run(self):
        self.get_chromsome()
        for i in range(self.generation):
            print(i)
            self.get_chromsome()
            self.reproduce()

        print(self.child.maze)
        self.child.print_path()
        print(self.child.solution)
        print(self.fitness(self.child))

    def fitness(self,chromsome):
        # used to count fitness of each chromosome
        # choose the algorithm used to solve the mazes
        solution = part1.SolveMaze(chromsome)
        solutionout = solution.run(self.method)
        # print (chromsome.solution[self.properties])

        return chromsome.solution[self.properties]

if __name__ == "__main__":
    ga = geneticalgorithm(30,0.2,20,"max_fringe_size","dfs",2)
    ga.run()