import diagrams
import importlib
import yaml
import sys


def make_nodes(x: dict):
    for k, v in x.items():
        if type(v) is dict:
            with diagrams.Cluster(k):
                make_nodes(v)
        if type(v) is list:
            module = v[0].rpartition(".")
            method = getattr(importlib.import_module(module[0]), module[-1])
            shapes[k] = method(k)


def connect_nodes(x: dict, k=False):
    for k, v in x.items():
        if type(v) is dict:
            connect_nodes(v, k)
        if type(v) is list:
            src = shapes[k]
            for i in v[1:]:
                if type(i) is list:
                    src >> diagrams.Edge(
                        color=colors.pop(0), style="bold", ltail=src._cluster.name, lhead=shapes[i[0]]._cluster.name) >> shapes[i[0]]
                else:
                    src >> diagrams.Edge(color=colors.pop(0), style="bold") >> shapes[i]


graph_attr = {"layout": "dot", "compound": "true", "splines": "spline", "concentrate": "true"}
colors = ['blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral',
          'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod',
          'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange',
          'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray',
          'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey',
          'dodgerblue', 'firebrick', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite',
          'gold', 'goldenrod', 'gray', 'grey', 'green', 'greenyellow', 'lightsalmon', 'lightseagreen',
          'lightskyblue', 'lightslategray', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen',
          'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid']

with open(r'inventory.yml', "r") as file:
    data = yaml.load(file, Loader=yaml.FullLoader)

# node_attr = {"shape": "ellipse", "height": "0.8", "labelloc": "c"}
# curvestype = ("ortho", "curved")  # direction = "TB", "BT", "LR", "RL"
with diagrams.Diagram(data.pop("diagram_name"), show=True, direction="TB", graph_attr=graph_attr) as diag:

    shapes = {}
    make_nodes(data)
    connect_nodes(data)
