from pathlib import Path
from typing import Tuple

from icontract import require
from igraph import Graph
from typeguard import typechecked


@typechecked
def format_choices() -> Tuple:
    return ("dot", "graphml", "gml")


@typechecked
def graph_to_file(g: Graph, path: Path, format: str):
    path = str(path)
    if format == "dot":
        g.write_dot(path)
    elif format == "graphml":
        g.write_graphml(path)
    elif format == "gml":
        g.write_gml(path)
    else:
        raise ValueError(f"Unsupported format {format}!")
