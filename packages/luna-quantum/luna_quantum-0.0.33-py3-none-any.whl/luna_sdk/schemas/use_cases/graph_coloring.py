from typing import Dict, Literal

from pydantic import Field

from luna_sdk.schemas.use_cases.base import UseCase


class GraphColoring(UseCase):
    """
    # Graph Coloring

    Description
    -----------

    The Graph Coloring problem tries to color the nodes of a graph with a given number
    of different colors so that no adjacent nodes have the same color.

    Links
    -----

    [Wikipedia](https://en.wikipedia.org/wiki/Graph_coloring)

    [Transformation](https://arxiv.org/pdf/1811.11538.pdf)

    Attributes
    ----------

    ### graph: Dict[int, Dict[int, Dict[str, float]]]
        \n Problem graph for the graph coloring problem in form of nested dictionaries.
        \n (e.g. fully connected graph with 3 nodes:
        \n _{0: {1: {}, 2: {}}, 1: {0: {}, 2: {}}, 2: {0: {}, 1: {}}}_
        \n or _networkx.to_dict_of_dicts(networkx.complete_graph(3))_ )

    ### n_colors: int
        \n Number of different colors.
    """

    name: Literal["GC"] = "GC"
    graph: Dict[str, Dict[str, Dict[str, float]]] = Field(name="graph")  # type: ignore
    n_colors: int
    P: int = 4
