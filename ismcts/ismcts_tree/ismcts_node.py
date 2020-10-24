from __future__ import annotations

from typing import List

import numpy as np

from ismcts.ismcts_tree.ismcts_node_state import ISMCTSNodeState
from ismcts.jass_stuff.hands import Hands
from ismcts.jass_stuff.valid_card_holder import ValidCardHolder


class ISMCTSNode:

    def __init__(self,  node_state: ISMCTSNodeState, parent_node: ISMCTSNode = None):
        self._node_state = node_state
        self._parent_node = parent_node
        self._is_explored = False
        self._possible_child_nodes: List[ISMCTSNode] = []
        self._nbr_of_node_was_played = 0
        self._payoff = 0
        self._nbr_of_node_was_visible = 0

    def _determine_possible_child_nodes(self) -> List[ISMCTSNode]:
        valid_cards = [i for i, card in enumerate(self._node_state.get_valid_cards_of_current_player())]
        child_nodes = []
        for valid_card in valid_cards:
            copy_node_state = self._node_state.copy()
            copy_node_state.remove_card(valid_card)
            child_nodes.append(ISMCTSNode(copy_node_state))
        return child_nodes

    def update(self, payoff: np.ndarray) -> None:
        self._nbr_of_node_was_played += 1
        self._payoff += payoff
        if self._parent_node is not None:
            self._parent_node.update(payoff)

    def has_child_nodes(self) -> bool:
        return len(self.get_child_nodes()) != 0

    def get_child_nodes(self) -> List[ISMCTSNode]:
        return self._possible_child_nodes

    def has_visible_child_nodes(self, valid_card_holder: ValidCardHolder) -> bool:
        return len(self.get_visible_child_nodes(valid_card_holder)) != 0

    def get_visible_child_nodes(self, valid_card_holder: ValidCardHolder) -> List[ISMCTSNode]:
        return list(filter(lambda child: child.is_visible(valid_card_holder), self._possible_child_nodes))

    def has_visible_explored_child_nodes(self, valid_card_holder: ValidCardHolder) -> bool:
        return len(self.get_visible_explored_child_nodes(valid_card_holder)) != 0

    def get_visible_explored_child_nodes(self, valid_card_holder: ValidCardHolder) -> List[ISMCTSNode]:
        return list(filter(lambda child: child.is_visible(valid_card_holder) and child.is_explored,
                           self._possible_child_nodes))

    def has_visible_unexplored_child_nodes(self, valid_card_holder: ValidCardHolder) -> bool:
        return len(self.get_visible_unexplored_child_nodes(valid_card_holder)) != 0

    def get_visible_unexplored_child_nodes(self, valid_card_holder: ValidCardHolder) -> List[ISMCTSNode]:
        return list(filter(lambda child: child.is_visible(valid_card_holder) and not child.is_explore,
                           self._possible_child_nodes))

    def is_visible(self, valid_card_holder: ValidCardHolder) -> bool:
        return self._node_state.information_set.does_contain(valid_card_holder.get_hands())

    def mark_as_explored(self):
        self._is_explored = True

    @property
    def parent_node(self):
        return self._parent_node

    @property
    def is_explored(self):
        return self._is_explored

    @property
    def nbr_of_node_was_played(self):
        return self._nbr_of_node_was_played

    @property
    def nbr_of_node_had_won(self):
        return self.payoff[0]

    @property
    def nbr_of_node_was_visible(self):
        return self._nbr_of_node_was_visible

    @nbr_of_node_was_visible.setter
    def nbr_of_node_was_visible(self, value):
        self._nbr_of_node_was_visible = value

    @property
    def payoff(self) -> np.ndarray:
        return self._node_state.payoff

    @property
    def last_played_card(self) -> int:
        return self._node_state.last_played_card

    def copy(self) -> ISMCTSNode:
        return ISMCTSNode(self._node_state.copy())