from __future__ import annotations

from abc import abstractmethod
from typing import List

from montecarlo.monte_carlo_node import MonteCarloNode


class TreePolicy:

    @abstractmethod
    def selection(self, nodes: List[MonteCarloNode]) -> MonteCarloNode:
        pass
