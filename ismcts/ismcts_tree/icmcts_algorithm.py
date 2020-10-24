import numpy as np
from jass.game.game_observation import GameObservation

from ismcts.ismcts_tree.default_policy import DefaultPolicy
from ismcts.ismcts_tree.ismcts_node import ISMCTSNode
from ismcts.ismcts_tree.tree_policy import TreePolicy
from ismcts.jass_stuff.valid_card_holder import ValidCardHolder


class ISMCTSAlgorithm:

    def __init__(self, obs: GameObservation, root_node: ISMCTSNode, tree_policy: TreePolicy, default_policy: DefaultPolicy) -> None:
        self._obs = obs
        self._root_node = root_node
        self._tree_policy = tree_policy
        self._default_policy = default_policy

    def perform(self):
        valid_card_holder = self._sampling()
        selected_node_to_expand = self._selection(valid_card_holder)
        self._expansion(selected_node_to_expand, valid_card_holder)

    def _sampling(self) -> ValidCardHolder:
        return ValidCardHolder.random_from_obs(self._obs)

    def _selection(self, valid_card_holder: ValidCardHolder):
        node_to_expand = self._tree_policy.selection(self._root_node.get_possible_child_nodes())
        while not node_to_expand.has_unexplored_child_nodes(valid_card_holder) and \
                node_to_expand.has_explored_child_nodes(valid_card_holder):
            node_to_expand = self._tree_policy.selection(node_to_expand.get_explored_child_nodes(valid_card_holder))
        return node_to_expand

    def _expansion(self, node_to_expand: ISMCTSNode, valid_card_holder: ValidCardHolder):
        if node_to_expand.has_unexplored_child_nodes(valid_card_holder):
            node_to_explore = self._default_policy.selection(node_to_expand
                                                             .get_unexplored_child_nodes(valid_card_holder))
            payoff = self._simulation(node_to_explore, valid_card_holder)
            node_to_explore.mark_as_explored()
            node_to_expand.update(payoff)
        else:
            # node to expand without unexplored child's is a leaf node
            node_to_expand.update(node_to_expand.payoff)

    def _simulation(self, simulation_root_node: ISMCTSNode, valid_card_holder: ValidCardHolder) -> np.ndarray:
        child_node = simulation_root_node
        while child_node.has_child_nodes(valid_card_holder):
            child_node = self._default_policy.selection(child_node.get_child_nodes())
        return child_node.payoff
