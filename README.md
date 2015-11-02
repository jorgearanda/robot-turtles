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
