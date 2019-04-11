from part1 import Maze, SolveMaze

if __name__ == "__main__":
    size = 100

    print('using dfs ----------------------------------')
    success_record = 0
    prob = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

    for p in prob:
        for i in range(1, 101):
            maze = Maze(size, p)
            maze.solution = SolveMaze(maze).dfs()
            if maze.solution.get("find_path_or_not") == "YES":
                success_record += 1
        print("When p is: " + str(p) + " , p0 is " + str(success_record / 100))
        success_record = 0

