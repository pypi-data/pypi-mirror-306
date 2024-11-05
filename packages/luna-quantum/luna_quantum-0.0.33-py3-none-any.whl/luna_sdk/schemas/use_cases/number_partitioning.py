from typing import List, Literal

from luna_sdk.schemas.use_cases.base import UseCase


class NumberPartitioning(UseCase):
    """
    # Number Partitioning

    Description
    -----------

    The Number Partitioning problem partitions a set of numbers into two subsets such
    that the difference of the subset sums is minimized.

    Links
    -----

    [Wikipedia](https://en.wikipedia.org/wiki/Partition_problem)

    [Transformation](https://arxiv.org/pdf/1811.11538.pdf)

    Attributes
    ----------

    ### numbers: List[int]
        \n The set of numbers which has to be partitioned.
    """

    name: Literal["NP"] = "NP"
    numbers: List[int]
