from copy import deepcopy
import random

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

import primitives
from turtle_simulator import TurtleSimulator


turtle = TurtleSimulator(100)

pset = gp.PrimitiveSet('MAIN', 0)
pset.addPrimitive(turtle.if_tower_next, 2)
pset.addPrimitive(turtle.if_gem_ahead, 2)
pset.addPrimitive(primitives.seq2, 2)
pset.addPrimitive(primitives.seq3, 3)
pset.addTerminal(turtle.move_forward)
pset.addTerminal(turtle.turn_left)
pset.addTerminal(turtle.turn_right)

creator.create('FitnessMax', base.Fitness, weights=(1.0, 0.3, 0.1))
creator.create('Individual', gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register('expr_init', gp.genFull, pset=pset, min_=1, max_=2)
toolbox.register('individual', tools.initIterate, creator.Individual, toolbox.expr_init)
toolbox.register('population', tools.initRepeat, list, toolbox.individual)

def evaluateTurtle(individual):
    routine = gp.compile(individual, pset)
    turtle.run(routine)
    return 1.0 if turtle.success else 0.0, turtle.moves * 1.0 / turtle.max_moves, turtle.distance

toolbox.register('evaluate', evaluateTurtle)
toolbox.register('select', tools.selTournament, tournsize=7)
toolbox.register('mate', gp.cxOnePoint)
toolbox.register('expr_mut', gp.genFull, min_=0, max_=2)
toolbox.register('mutate', gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

def main():
    random.seed(1)

    scenario_file = open('scenarios/towers.txt')
    turtle.parse_matrix(scenario_file)

    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register('avg', numpy.mean)
    stats.register('std', numpy.std)
    stats.register('min', numpy.min)
    stats.register('max', numpy.max)

    algorithms.eaSimple(pop, toolbox, 0.5, 0.2, 20, stats, halloffame=hof)

    return pop, hof, stats

if __name__ == '__main__':
    import pygraphviz as pgv
    pop, hof, stats = main()
    nodes, edges, labels = gp.graph(hof[0])

    g = pgv.AGraph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    g.layout(prog="dot")

    for i in nodes:
        n = g.get_node(i)
        n.attr["label"] = labels[i]

    g.draw("tree.pdf")
