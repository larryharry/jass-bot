from random import randrange
from typing import List

from ismcts.ismcts_tree.default_policy import DefaultPolicy
from ismcts.ismcts_tree.ismcts_node import ISMCTSNode


class DefaultPolicyRandom(DefaultPolicy):

    def selection(self, nodes: List[ISMCTSNode]) -> ISMCTSNode:
        return nodes[randrange(len(nodes))]
