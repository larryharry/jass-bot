from __future__ import annotations

import math
import sys
from abc import ABC
from typing import List

from montecarlo.monte_carlo_node import MonteCarloNode


class TreePolicyRandom(ABC):

    def __init__(self, c: int):
        self._c = c

    def selection(self, total_n: int, nodes: List[MonteCarloNode]) -> MonteCarloNode:
        node_with_highest_ucb1 = nodes[0]
        highest_ucb1 = -(sys.maxsize - 1)
        for node in nodes:
            ucb1 = self._calculate_ucb1(total_n, node)
            if ucb1 > highest_ucb1:
                highest_ucb1 = ucb1
                node_with_highest_ucb1 = node
        return node_with_highest_ucb1

    def _calculate_ucb1(self, total_n: int, node: MonteCarloNode) -> int:
        wi = node.w[0]
        ni = node.n
        np = total_n
        if ni == 0:
            ni = 1
        if np == 0:
            np = 1
        return (wi/ni) + (self._c * math.sqrt(math.log(np, math.e) / ni))
