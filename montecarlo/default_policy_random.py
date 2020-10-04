from random import randrange
from typing import List

from montecarlo.default_policy import DefaultPolicy
from montecarlo.monte_carlo_node import MonteCarloNode


class DefaultPolicyRandom(DefaultPolicy):

    def selection(self, nodes: List[MonteCarloNode]) -> MonteCarloNode:
        return nodes[randrange(len(nodes))]

    def selection_with_remove(self, nodes: List[MonteCarloNode]) -> MonteCarloNode:
        selected_node = self.selection(nodes)
        nodes.remove(selected_node)
        return selected_node
