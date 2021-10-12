#!/usr/bin/env python3
import sys
import diagrams
import importlib
import yaml

COLOR = None

if len(sys.argv) >= 2:
    FILE_SOURCE = sys.argv[1]
else:
    FILE_SOURCE = "/Users/perlejon/Documents/bitbucket/sre-docs/infrastructure/se-prod/inventory.yml"
    Exception("Specify yml file in arguemnt\n example: python3 main.py mydiag.yml")


def make_nodes(x: dict):
    for k, v in x.items():
        if type(v) is dict:
            with diagrams.Cluster(k):
                make_nodes(v)
        if type(v) is list:
            module = v[0].rpartition(".")
            method = getattr(importlib.import_module(module[0]), module[-1])
            shapes[k] = method(k, **common_node_attr)


def connect_nodes(x: dict, k=False):
    for k, v in x.items():
        if type(v) is dict:
            connect_nodes(v, k)
        if type(v) is list:
            edge_color = colors.pop(0)
            src = shapes[k]
            for i in v[1:]:
                if type(i) is list:
                    (
                        src
                        >> diagrams.Edge(
                            color=edge_color,
                            style="bold",
                            ltail=src._cluster.name,
                            lhead=shapes[i[0]]._cluster.name,
                            minlen="1"
                        )
                        >> shapes[i[0]]
                    )

                elif type(i) is str:
                    if i == "host1":
                        print()
                    src >> diagrams.Edge(color=edge_color, style="bold", minlen="1") >> shapes[i]

                elif type(i) is dict:
                    for key, value in i.items():
                        (
                            src
                            >> diagrams.Edge(
                                color=edge_color, xlabel=value, style="bold", minlen="1"
                            )
                            >> shapes[key]
                        )


common_node_attr = {
    # "fixedsize": "true",            # true | false
    # "imagescale": "true",           # true | false | width | height | both
    # "labelloc":"b",                 # t | c | b
    # "penwidth": "0",
}

graph_attr = {
    "layout": "dot",
    "nodesep": "0.9",
    # "ranksep": "2",
    "compound": "true",
    "splines": "spline",
    "concentrate": "true",
    "penwidth": "0  ",
    "fixedsize": "true",
    "imagescale": "true",
    "width": "3",
    "height": "3",
    # "labelloc": "b",

}
colors = [
    "blueviolet",
    "brown",
    "burlywood",
    "cadetblue",
    "chartreuse",
    "chocolate",
    "coral",
    "cornflowerblue",
    "crimson",
    "cyan",
    "darkblue",
    "darkcyan",
    "darkgoldenrod",
    "darkgray",
    "darkgreen",
    "darkkhaki",
    "darkmagenta",
    "darkolivegreen",
    "darkorange",
    "darkorchid",
    "darkred",
    "darksalmon",
    "darkseagreen",
    "darkslateblue",
    "darkslategray",
    "darkslategrey",
    "darkturquoise",
    "darkviolet",
    "deeppink",
    "deepskyblue",
    "dimgray",
    "dimgrey",
    "dodgerblue",
    "firebrick",
    "forestgreen",
    "fuchsia",
    "gainsboro",
    "gold",
    "goldenrod",
    "grey",
    "green",
    "greenyellow",
    "lightsalmon",
    "lightseagreen",
    "lightskyblue",
    "lightslategray",
    "lightsteelblue",
    "lightyellow",
    "lime",
    "limegreen",
    "linen",
    "magenta",
    "maroon",
    "mediumaquamarine",
    "mediumblue",
    "mediumorchid",
]


with open(FILE_SOURCE, "r") as file:
    data = yaml.load(file, Loader=yaml.FullLoader)

# node_attr = {"shape": "ellipse", "height": "0.8", "labelloc": "c"}
# curvestype = ("ortho", "curved")  # direction = "TB", "BT", "LR", "RL"
with diagrams.Diagram(
    data["diagram_name"], show=False, direction="TB", graph_attr=graph_attr
) as diag:

    shapes = {}
    make_nodes(data)
    connect_nodes(data)
