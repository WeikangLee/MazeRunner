from part1 import Maze, SolveMaze

if __name__ == "__main__":
    size = 100
    print('using dfs ----------------------------------')
    nodes_record = 0
    num_record = 0

    prob = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4]
    for p in prob:
        for i in range(1, 101):
            maze = Maze(size, p)
            maze.solution = SolveMaze(maze).a_star_euclidean()
            if maze.solution.get("find_path_or_not") == "Yes":
                nodes_record += maze.solution['number_of_nodes_visited']
                num_record += 1
        print("When p is: " + str(p) + " , p0 is " + str(nodes_record / num_record))

        nodes_record = 0
        num_record = 0
