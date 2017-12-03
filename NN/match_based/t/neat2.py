from neat import nn, config, population
import itertools
import os
import pickle
import copy
from graphviz import Digraph

X_train = []
y_train = []

# with open("match_prepared.dat", 'r') as f:
#     with open("match_out_prepared.dat", 'r') as f2:
#         for line_tr, line_te in itertools.izip(f, f2):
#             X_train.append([float(num) for num in line_tr.strip().split()])
#             y_train.append([int(line_te.strip())])
min_weight = -100
max_weight = 100
BGCOLOR = '#D9D9D9'


def drawImage(best):
    best_genome = pickle.load(open(best, 'rb'))
    try:
        os.remove("current_nn.gif")
    except:
        pass
    input_nodes = [ng.ID for ng in best_genome.node_genes.values() if ng.type == 'INPUT']
    output_nodes = [ng.ID for ng in best_genome.node_genes.values() if ng.type == 'OUTPUT']
    connections = [(cg.in_node_id, cg.out_node_id, cg.weight) for cg in best_genome.conn_genes.values() if cg.enabled]
    layers = nn.find_feed_forward_layers(input_nodes, [(a, b) for (a, b, c) in connections])
    graph = Digraph(node_attr={'shape': 'circle', 'fixedsize': 'true', 'width': '.3'},
                    graph_attr={'rankdir': 'LR', 'bgcolor': BGCOLOR},
                    filename="current_nn", format="gif")
    sub_graphs = [Digraph(name="cluster_in", node_attr={'label': 'I'},
                          graph_attr={'label': 'Input Layer', 'color': BGCOLOR}),
                  Digraph(name="cluster_out", node_attr={'label': 'O'},
                          graph_attr={'label': 'Output Layer', 'color': BGCOLOR})]

    nodes = {}
    inp_count = 0
    output_count = 0
    for node in best_genome.node_genes.values():
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

def cs_fitness(genomes):
    for g in genomes:
        print(g.ID)
        fit = 0
        tot = 0.0
        net = nn.create_recurrent_phenotype(g)
        with open("match_prepared.dat", 'r') as f, open("match_out_prepared.dat", 'r') as f2:
            for line_tr, line_te in itertools.izip(f, f2):
                if tot > 14000:
                    break
                res = int(net.activate([float(num) for num in line_tr.strip().split()])[0])
                if res == int(line_te.strip()):
                    fit += 1
                tot += 1
        g.fitness = fit/tot
        print "Correct guesses {0}, in total of {1} matches.\n".format(str(fit), str(tot))


conf = config.Config('flappy_config')
conf.save_best = True

try:
    init_population = []
    pop_size = conf.pop_size

    genome_files = sorted([f for f in os.listdir('.') if f.startswith("best_genome_")],
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

pop = population.Population(conf, init_population)
pop.run(cs_fitness, 50000)
