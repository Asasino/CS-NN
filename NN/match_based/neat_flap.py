import os
import time
import pickle
import copy

from Games.FlappyBird.flappybirdapi import FlappyBirdAPI
from Games.FlappyBird.multiplegenomeagent import MultipleGenomeAgent
from neat import nn, population, config
from sequence import Sequence
from graphviz import Digraph

speed = 0.01
game_sequence = None
BGCOLOR = '#D9D9D9'
min_weight = -100
max_weight = 100


def drawImage(best):

    try:
        os.remove("current_nn.gif")
    except FileNotFoundError:
        pass
    input_nodes = [ng.ID for ng in best.node_genes.values() if ng.type == 'INPUT']
    output_nodes = [ng.ID for ng in best.node_genes.values() if ng.type == 'OUTPUT']
    connections = [(cg.in_node_id, cg.out_node_id, cg.weight) for cg in best.conn_genes.values() if cg.enabled]
    layers = nn.find_feed_forward_layers(input_nodes, [(a, b) for (a, b, c) in connections])
    graph = Digraph(node_attr={'shape': 'circle', 'fixedsize': 'true', 'width': '.3'}, graph_attr={'rankdir': 'LR', 'bgcolor': BGCOLOR},
                    filename="current_nn", format="gif")
    sub_graphs = [Digraph(name="cluster_in", node_attr={'label': 'I'},
                          graph_attr={'label': 'Input Layer', 'color': BGCOLOR}),
                  Digraph(name="cluster_out", node_attr={'label': 'O'},
                          graph_attr={'label': 'Output Layer', 'color': BGCOLOR})]

    nodes = {}
    inp_count = 0
    output_count = 0
    for node in best.node_genes.values():
        if node.type == 'INPUT':
            sub_graphs[0].node('i' + str(inp_count))
            nodes[str(node.ID)] = 'i' + str(inp_count)
            inp_count += 1
        elif node.type == 'OUTPUT':
            sub_graphs[-1].node('o' + str(output_count))
            nodes[str(node.ID)] = 'o' + str(output_count)
            output_count += 1

    layer_depth = 0
    for layer in layers:
        layer_node_count = 0
        sub_graphs.insert(-1, Digraph(name='cluster_h{}'.format(layer_depth + 1), node_attr={'label': 'H'},
                                      graph_attr={'label': "Hidden Layer {0}".format(layer_depth + 1),
                                                  'color': BGCOLOR}))
        for hidden_node in layer:
            if hidden_node in output_nodes:  # Except output layer
                continue
            sub_graphs[-2].node('h{0}{1}'.format(layer_depth + 1, layer_node_count))
            nodes[str(hidden_node)] = 'h' + str(layer_depth + 1) + str(layer_node_count)
            layer_node_count += 1
        layer_depth += 1
    for g in sub_graphs:
        graph.subgraph(g)
    weight_diff = (max_weight - min_weight)
    for inID, outID, w in connections:
        normalized_weight = (float(w) - min_weight) / weight_diff
        graph.edge(nodes[str(inID)], nodes[str(outID)],
                   _attributes={"penwidth": str(normalized_weight),
                                "label": str(w), "color": "#%02x0000" % int(normalized_weight * 255)})
    graph.render()


def flappy_fitness(population):
    try:
        drawImage(max([g for g in population if isinstance(g.fitness, float)]))
    except ValueError:
        pass
    genome_ids = [str(g.ID) for g in population]

    # CREATE NETWORK FOR EACH GENOME
    networks = [(str(g.ID), nn.create_feed_forward_phenotype(g)) for g in population]

    game_sequence.game.changeGenomes(genome_ids)  # PUSH GENOMES
    game_sequence.change_agent(MultipleGenomeAgent(networks))

    start_time = time.time()
    game_sequence.create()

    seq = game_sequence.seq
    elapsed_time = -1
    alive_player = -1

    for g, is_alive in seq[len(seq) - 1][1].playerAlive.items():
        if is_alive:
            alive_player = g  # Find only alive player
            break
    if seq[len(seq) - 1][1].playery[alive_player] <= 0:
        elapsed_time = 0
    for g in population:
        # GET EACH DEATH TIME AND CALCULATE ELAPSED TIME #
        elapsed_time = 0 if not elapsed_time else (seq[len(seq) - 1][1].deathTime[str(g.ID)] - start_time)
        g.fitness = seq[len(seq) - 1][1].deathScore[str(g.ID)] + elapsed_time
    game_sequence.resetSequence()


def main():
    global game_sequence, min_weight, max_weight
    game_path = os.path.join(os.path.join(os.getcwd(), "Games"), "FlappyBird")
    # genome_path = os.path.join(game_path, "genomes")
    config_path = os.path.join(game_path, 'flappy_config')
    pop_config = config.Config(config_path)
    pop_config.save_best = True
    min_weight, max_weight = pop_config.min_weight, pop_config.max_weight
    try:
        init_population = []
        pop_size = pop_config.pop_size

        genome_files = sorted([f for f in os.listdir() if f.startswith("best_genome_")],
                              key=lambda x: int(x.split("_")[-1]))
        for filename in genome_files[-pop_size:]:  # get best ones
            with open(os.path.join(os.getcwd(), filename), "rb") as f:
                genome = pickle.load(f)
            genome.ID = str(len(init_population))
            init_population.append(genome)
        best_genome = init_population[-1]
        for i in range(len(init_population), pop_size):  # Fill rest with best genome if there is not 50 genomes
            new_genome = copy.deepcopy(best_genome)
            new_genome.ID = str(i)
            init_population.append(new_genome)
        gen_number = int(genome_files[-1].split("_")[-1])  # in order not to override previous generations
    except IndexError:
        init_population = None
        gen_number = -1
    pop = population.Population(pop_config, init_population)
    pop.generation = gen_number

    game_sequence = Sequence(speed, FlappyBirdAPI(True), None, "flappybirdneat")

    pop.run(flappy_fitness, 200)


if __name__ == "__main__":
    main()
