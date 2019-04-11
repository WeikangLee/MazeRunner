from part1 import Maze, SolveMaze
from datetime import datetime

if __name__ == "__main__":
    size = 1000
    prob = 0.2
    turn = 0
    while True:
        maze = Maze(size, prob)

        print('using dfs ----------------------------------')
        start_time = datetime.now()
        maze.solution = SolveMaze(maze).dfs()
        end_time = datetime.now()
        dfs_last_seconds = (end_time - start_time).total_seconds()

        print('\nusing bfs ----------------------------------')
        start_time = datetime.now()
        maze.solution = SolveMaze(maze).bfs()
        end_time = datetime.now()
        bfs_last_seconds = (end_time - start_time).total_seconds()

        print('\nusing a_star_manhattan ----------------------------------')
        start_time = datetime.now()
        maze.solution = SolveMaze(maze).a_star_manhattan()
        end_time = datetime.now()
        asm_last_seconds = (end_time - start_time).total_seconds()

        print('\nusing a_star_euclidean ----------------------------------')
        start_time = datetime.now()
        maze.solution = SolveMaze(maze).a_star_euclidean()
        end_time = datetime.now()
        ase_last_seconds = (end_time - start_time).total_seconds()

        turn = turn + 1
        print('\n turn: ' + str(turn) + '\n')

        if dfs_last_seconds > 60 or bfs_last_seconds > 60 or asm_last_seconds > 60 or ase_last_seconds > 60:
            print("dfs costs: " + str(dfs_last_seconds))
            print("bfs costs: " + str(bfs_last_seconds))
            print("a_star_manhattan costs: " + str(asm_last_seconds))
            print("a_star_euclidean costs: " + str(ase_last_seconds))
            print(size)
            break

        size = size + 200
