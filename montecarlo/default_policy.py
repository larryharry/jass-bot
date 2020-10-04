from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from montecarlo.monte_carlo_node import MonteCarloNode


class DefaultPolicy(ABC):

    @abstractmethod
    def selection(self, nodes: List[MonteCarloNode]) -> MonteCarloNode:
        pass

    @abstractmethod
    def selection_with_remove(self, nodes: List[MonteCarloNode]) -> MonteCarloNode:
        pass
