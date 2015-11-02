## Robot Turtles - genetic programming sandbox

This is a toy example of genetic programming inspired by the [robot turtles](http://www.robotturtles.com/) boardgame and using the [DEAP](https://github.com/DEAP) Python library.

### Installation

Fork this repo, then `pip install -r requirements.txt`. You might need to install `graphviz` in advance.

### Usage

    Usage: robot_turtles.py [-h] --scenario <scenario> [--population <population>] [--generations <generations>] [--seed <seed>]

    -h --help                                      Show this
    -d <seed>, --seed <seed>                       Random seed. [default: 3]
    -g <generations>, --generations <generations>  Number of generations to run. [default: 50]
    -p <population>, --population <population>     Population size. [default: 1000]
    -s <scenario>, --scenario <scenario>           Path to scenario file to run

There is a number of scenarios under the `scenarios/` directory

### Scenario notation

A scenario is a text file where each line has the same number of columns, forming a matrix. Each cell of the matrix may be one of the following:

* `.` for an empty cell
* `T` for an impassable tower
* `B` for a box. Boxes can be pushed, provided the cell to which they are being moved is empty
* `I` for a block of ice. Ice can be melted with a blaster
* `G` for a gem, which the turtle attempts to reach
* `S` for the starting spot. The turtle is assumed to start here pointing east (right)

The border of the matrix is treated as a wall.

See `scenarios/all_together.txt` for a scenario that includes all of these elements.

### Affordances

A turtle can currently:

* See if the gem is straight ahead, even if not in line of sight (due to obstacles)
* See if there is ice in line of sight straight ahead
* See if the path ahead is blocked
* Move forward
* Turn left
* Turn right
* Shoot blaster (to melt ice blocks)

### Fitness

Fitness of the algorithms is weighed as such:

* Collecting the gem, 1.0
* Number of moves until collection (lower is better), 0.3
* Distance to the gem at the end (lower is better), 0.1

If the turtles have a complicated maze, they may not find the gem initially, so the only criterion in that case will be the distance to the gem after all moves are out.
Afterwards, the system rewards finding the gem much more, and any further discrimination happens by minimizing the number of moves to get there.

### Output

The script will output the number of moves to success for each generation. Additionally, you can view the best-performing algorithm by opening the resulting `tree.pdf` file.
