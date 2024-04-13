import copy

import networkx as nx
import matplotlib.pyplot as plt


class bayes_network():
    def __init__(self, package_graph):
        self.evidence = {}
        self.net = {"season": {
            'parents': [],
            'children': [],
            'prob': package_graph.season,
            'condprob': {}
        }}

        for v in package_graph.vertex:
            self.net[(v[0], v[1])] = {
                'parents': [],
                'children': [],
                'prob': -1,
                'condprob': {}
            }

        for f in package_graph.fragile_edges:
            self.net[tuple(f.points)] = {
                'parents': [],
                'children': [],
                'prob': -1,
                'condprob': {}
            }

        for v in package_graph.vertex:
            self.net["season"]["children"].append((v[0], v[1]))
            self.net[(v[0], v[1])]["parents"].append("season")
            self.net[(v[0], v[1])]["condprob"]["l"] = v[2]
            self.net[(v[0], v[1])]["condprob"]["m"] = 1 if v[2]*2 > 1 else round(v[2]*2, 2)
            self.net[(v[0], v[1])]["condprob"]["h"] = 1 if v[2]*2 > 1 else round(v[2]*3, 2)

        for f in package_graph.fragile_edges:
            for v in package_graph.vertex:
                if (f.points[0][0] == v[0] and f.points[0][1] == v[1]) or (f.points[1][0] == v[0] and f.points[1][1] == v[1]):
                    self.net[tuple(f.points)]["parents"].append((v[0], v[1]))
                    self.net[(v[0], v[1])]["children"].append(tuple(f.points))
                    self.net[tuple(f.points)]["condprob"][(False, False)] = package_graph.leakage
                    self.net[tuple(f.points)]["condprob"][(True, False)] = f.probability
                    self.net[tuple(f.points)]["condprob"][(False, True)] = f.probability
                    self.net[tuple(f.points)]["condprob"][(True, True)] = 1 - round((1-f.probability)*(1-f.probability), 2)

    def generate_init_probabilities(self, leake):
        self.probabilities = {}
        for node in self.net:
            if self.net[node]["prob"] != -1:
                self.probabilities[node] = self.net[node]["prob"]
            else:
                self.probabilities[node] = self.net[node]["condprob"]
        return self.probabilities

    def normalize(self, dist):
        return tuple(x * 1/(sum(dist)) for x in dist)


    def bearear_nodes(self,X ,e , vars):
        copy_net = copy.deepcopy(vars)
        not_exist_bearer_node = False
        while not not_exist_bearer_node:
            irelevant_vars = []
            found_one = False
            for node in copy_net:
                if node not in e and node != X and len(copy_net[node]["children"]) == 0:
                    irelevant_vars.append(node)
                    found_one = True
            if not found_one:
                not_exist_bearer_node = True
            copy_net = {key: value for key, value in copy_net.items() if key not in irelevant_vars}
            for node in copy_net:
                for child in copy_net[node]["children"]:
                    if child not in copy_net:
                        copy_net[node]["children"].remove(child)
        return copy_net

    def generate_probabilities(self, X, e):
        relevant_vars = self.bearear_nodes(X, e, vars=self.net)

        dist = []
        if X == "season":
            for x in ["l", "m", "h"]:
                e = copy.deepcopy(e)
                e[X] = x
                variables = list(relevant_vars)
                dist.append(self.enum_all(variables, e))
        else:
            for x in [False, True]:
                e = copy.deepcopy(e)
                e[X] = x
                variables = list(relevant_vars)
                dist.append(self.enum_all(variables, e))
        return self.normalize(dist)

    def query_given(self, Y, e):
        if self.net[Y]['prob'] != -1:
            evidence = e[Y]
            prob = self.net[Y]['prob'][evidence]
        else:
            if isinstance(list(self.net[Y]['condprob'].keys())[0], tuple):
                parents = tuple(e[p] for p in self.net[Y]['parents'])
                prob = self.net[Y]['condprob'][parents] if e[Y] else 1 - self.net[Y]['condprob'][parents]
            else:
                parent = e[self.net[Y]['parents'][0]]
                prob = self.net[Y]['condprob'][parent] if e[Y] else 1 - self.net[Y]['condprob'][parent]

        return prob

    def enum_all(self, variables, e):
        if len(variables) == 0:
            return 1.0
        Y = variables[0]
        if Y in e:
            ret = self.query_given(Y, e) * self.enum_all(variables[1:], e)
        else:
            probs = []
            e2 = copy.deepcopy(e)
            if Y == "season":
                for y in ["l", "m", "h"]:
                    e2[Y] = y
                    probs.append(self.query_given(Y, e2) * self.enum_all(variables[1:], e2))
            else:
                for y in [True, False]:
                    e2[Y] = y
                    probs.append(self.query_given(Y, e2) * self.enum_all(variables[1:], e2))
            ret = sum(probs)

        return ret



    def e_all(self, vars, e):
        if len(vars) == 0:
            return 1
        y = vars[0]
        if y in e:
            return

