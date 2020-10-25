from __future__ import annotations

from typing import List

import numpy as np
from jass.game.rule_schieber import RuleSchieber

from ismcts.ismcts_tree.ismcts_node_state import ISMCTSNodeState
from ismcts.jass_stuff.const import EMPTY_TRICK, EXISTING_CARD
from ismcts.jass_stuff.valid_card_holder import ValidCardHolder


class ISMCTSNode:

    def __init__(self, node_state: ISMCTSNodeState, parent_node: ISMCTSNode = None):
        self._node_state = node_state
        self._parent_node = parent_node
        self._is_explored = False
        self._child_nodes: List[ISMCTSNode] = None
        self._nbr_of_node_was_played = 0
        self._win_los_ration = np.array([0, 0])
        self._nbr_of_node_was_visible = 0
        self._rule = RuleSchieber()

    def update(self, payoff: np.ndarray) -> None:
        self._nbr_of_node_was_played += 1
        self._win_los_ration += payoff
        if self._parent_node is not None:
            self._parent_node.update(payoff)

    def has_child_nodes(self) -> bool:
        return len(self.get_child_nodes()) != 0

    def get_child_nodes(self) -> List[ISMCTSNode]:
        if self._child_nodes is None:
            self._child_nodes = self._determine_child_nodes()
        return self._child_nodes

    def _determine_child_nodes(self) -> List[ISMCTSNode]:
        cards = [i for i, card in enumerate(self._node_state.get_cards_of_current_player())
                 if card == 1]
        child_nodes = []
        for card in cards:
            copy_node_state = self._node_state.copy()
            copy_node_state.remove_card(card)
            child_nodes.append(ISMCTSNode(copy_node_state, self))
        return child_nodes

    def has_visible_child_nodes(self, valid_card_holder: ValidCardHolder) -> bool:
        return len(self.get_visible_child_nodes(valid_card_holder)) != 0

    def get_visible_child_nodes(self, valid_card_holder: ValidCardHolder) -> List[ISMCTSNode]:
        return list(filter(lambda child: child.is_visible(valid_card_holder), self.get_child_nodes()))

    def has_visible_explored_child_nodes(self, valid_card_holder: ValidCardHolder) -> bool:
        return len(self.get_visible_explored_child_nodes(valid_card_holder)) != 0

    def get_visible_explored_child_nodes(self, valid_card_holder: ValidCardHolder) -> List[ISMCTSNode]:
        return list(filter(lambda child: child.is_visible(valid_card_holder) and child.is_explored,
                           self.get_child_nodes()))

    def has_visible_unexplored_child_nodes(self, valid_card_holder: ValidCardHolder) -> bool:
        return len(self.get_visible_unexplored_child_nodes(valid_card_holder)) != 0

    def get_visible_unexplored_child_nodes(self, valid_card_holder: ValidCardHolder) -> List[ISMCTSNode]:
        return list(filter(lambda child: child.is_visible(valid_card_holder) and not child.is_explored,
                           self.get_child_nodes()))

    def is_visible(self, valid_card_holder: ValidCardHolder) -> bool:
        return self._node_state.information_set.covered_by(valid_card_holder.get_hands()) and \
               self._does_node_represent_valid_card(valid_card_holder)

    def _does_node_represent_valid_card(self, valid_card_holder: ValidCardHolder) -> bool:
        parent_jass_carpet = self._parent_node._node_state.jass_carpet
        sampled_hand = valid_card_holder.get_hand(parent_jass_carpet.current_player).copy()
        parent_jass_carpet.remove_already_played_card_from(sampled_hand)
        current_trick = parent_jass_carpet.last_trick
        if current_trick.is_completed:
            return self._rule.get_valid_cards(sampled_hand.asArray(), EMPTY_TRICK, 0,
                                              parent_jass_carpet.trump)[self.last_played_card] == EXISTING_CARD

        else:
            return self._rule.get_valid_cards(sampled_hand.asArray(), current_trick.asArray(),
                                              current_trick.index_of_next_missing_card,
                                              parent_jass_carpet.trump)[self.last_played_card] == EXISTING_CARD

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
        return self.win_los_ration[0]

    @property
    def nbr_of_node_was_visible(self):
        return self._nbr_of_node_was_visible

    @nbr_of_node_was_visible.setter
    def nbr_of_node_was_visible(self, value):
        self._nbr_of_node_was_visible = value

    @property
    def win_los_ration(self) -> np.ndarray:
        return self._win_los_ration

    @property
    def payoff(self) -> np.ndarray:
        return self._node_state.payoff

    @property
    def last_played_card(self) -> int:
        return self._node_state.last_played_card

    def copy(self) -> ISMCTSNode:
        return ISMCTSNode(self._node_state.copy(), self._parent_node)
