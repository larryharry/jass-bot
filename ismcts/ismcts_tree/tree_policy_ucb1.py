from __future__ import annotations

import logging
import math
import sys
from typing import List

from ismcts.ismcts_tree.ismcts_node import ISMCTSNode
from ismcts.ismcts_tree.tree_policy import TreePolicy


def _mark_nodes_as_visited(nodes: List[ISMCTSNode]) -> None:
    for node in nodes:
        node.nbr_of_node_was_visible += 1


class TreePolicyUCB1(TreePolicy):

    def __init__(self, c: int = 5):
        self._c = c
        self._logger = logging.getLogger(__name__)

    def selection(self, nodes: List[ISMCTSNode]) -> ISMCTSNode:
        node_with_highest_ucb1 = self._determine_node_with_highest_ucb1(nodes)
        _mark_nodes_as_visited(nodes)
        return node_with_highest_ucb1

    def _determine_node_with_highest_ucb1(self, nodes: List[ISMCTSNode]) -> ISMCTSNode:
        self._logger.info("nodes_tree_policy " + str(len(nodes)))
        node_with_highest_ucb1 = nodes[0]
        highest_ucb1 = -(sys.maxsize - 1)
        for node in nodes:
            ucb1 = self._calculate_ucb1(node)
            if ucb1 > highest_ucb1:
                highest_ucb1 = ucb1
                node_with_highest_ucb1 = node
        return node_with_highest_ucb1

    def _calculate_ucb1(self, node: ISMCTSNode) -> int:
        wi = node.nbr_of_node_had_won
        ni = node.nbr_of_node_was_played
        np = node.nbr_of_node_was_visible
        if ni == 0:
            ni = 1
        if np == 0:
            np = 1
        return (wi/ni) + (self._c * math.sqrt(math.log(np, math.e) / ni))
