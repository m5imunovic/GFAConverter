import os
from pathlib import Path
from typing import List, Tuple

import gfapy
from igraph import Graph
from icontract import require
from typeguard import typechecked


def inv_complement_name(name: str) -> str:
    if name.startswith("_"):
        return name[1:]
    else:
        return "_" + name


@typechecked
def names_from_orientation(link: gfapy.Line) -> Tuple[str, str, str, str]:
    orient = link.from_orient + link.to_orient
    inv_fid = inv_complement_name(link.from_name)
    inv_tid = inv_complement_name(link.to_name)
    if orient == "++":
        return (link.from_name, link.to_name, inv_tid, inv_fid)
    elif orient == "--":
        return (inv_fid, inv_tid, link.to_name, link.from_name)
    elif orient == "+-":
        return (link.from_name, inv_tid, link.to_name, inv_fid)
    elif orient == "-+":
        return (inv_fid, link.to_name, inv_tid, link.from_name)
    else:
        raise ValueError("Unknown orientation")


def load_gfa1(gfa: gfapy.Gfa) -> Graph:
    segments = []
    virtual_edges = []
    for s in gfa.segments:
        segments.append(s.sid)
        # Add reverse complement, for now don't save the sequence
        # We want to keep information about the orientation in case there is an
        # assembler that creates name with underscore by default
        inv_id = inv_complement_name(s.sid)
        segments.append(inv_id)
        virtual_edges.append((s.sid, inv_id))

    print("Loaded segments")
    edges = []
    for e in gfa.edges:
        fw_from, fw_to, rc_from, rc_to = names_from_orientation(e)
        # Forward string
        edges.append((fw_from, fw_to))
        # Reverse complement string
        edges.append((rc_from, rc_to))

    print("Loaded edges")

    graph = Graph(directed=True)
    graph.add_vertices(segments)
    graph.add_edges(edges)
    graph.add_edges(virtual_edges)

    print("Created graph")

    return graph


def load_gfa2(gfa: gfapy.Gfa) -> Graph:
    segments = []
    virtual_edges = []
    for s in gfa.segments:
        segments.append(s.sid)
        inv_id = inv_complement_name(s.sid)
        segments.append(inv_id)
        virtual_edges.append((s.sid, inv_id))

    edges = []
    for e in gfa.edges:
        fw_from, fw_to, rc_from, rc_to = names_from_orientation(e)
        # Forward string
        edges.append((fw_from, fw_to))
        # Reverse complement string
        edges.append((rc_from, rc_to))

    graph = Graph(directed=True)
    graph.add_vertices(segments)
    graph.add_edges(edges)
    graph.add_edges(virtual_edges)

    return graph


#@typechecked
@require(lambda gfa_path: gfa_path.exists(), description="Input path does not exist.")
def load_gfa(gfa_path: Path) -> Graph:
    try:
        gfa = gfapy.Gfa.from_file(gfa_path)
        if gfa.version == 'gfa1':
            return load_gfa1(gfa)
        if gfa.version == 'gfa2':
            return load_gfa2(gfa)
    except NotImplementedError:
        print("Not implemented")
        raise NotImplementedError
    except Exception as ex:
        # TODO: Analyze exception and return proper response
        print("Exception: ", ex)
        return [], [], []


if __name__ == "__main__":
    base_path = Path(__file__).parent.parent.absolute() / "examples"
    load_gfa(base_path / "example1.gfa")
    load_gfa(base_path / "example1.gfa2")
    load_gfa(base_path / "example_from_spec.gfa")
    load_gfa(base_path / "example_from_spec.gfa2")