from __future__ import annotations

from typing import List

import numpy as np

from montecarlo.const import EXISTING_CARD
from montecarlo.jass_carpet import JassCarpet
from montecarlo.valid_card_holder import ValidCardHolder


class MonteCarloNode:

    def __init__(self, initial_player: int, jass_carpet: JassCarpet,
                 valid_card_holder: ValidCardHolder, parent_node: MonteCarloNode = None):
        self._initial_player = initial_player
        self._parent_node = parent_node
        self._child_nodes: List[MonteCarloNode] = None
        self._unexplored_child_nodes: List[MonteCarloNode] = None
        self._jass_carpet = jass_carpet
        self._valid_card_holder = valid_card_holder
        self._n = 0
        self._w = np.array([0, 0])

    def update(self, w: np.ndarray) -> None:
        self._w += w
        self._n += 1
        if self._parent_node is not None:
            self._parent_node.update(w)

    def has_unexplored_child_nodes(self):
        return len(self.get_unexplored_child_nodes()) != 0

    def get_unexplored_child_nodes(self) -> List[MonteCarloNode]:
        # lazy load unexplored nodes and child nodes
        if self._unexplored_child_nodes is None:
            self._unexplored_child_nodes = self.get_child_nodes()
        return self._unexplored_child_nodes

    def has_child_nodes(self):
        return len(self.get_child_nodes()) != 0

    def get_child_nodes(self) -> List[MonteCarloNode]:
        # lazy load child nodes and unexplored nodes
        if self._child_nodes is None:
            self._child_nodes = self._determine_child_nodes()
            if self._unexplored_child_nodes is None:
                self._unexplored_child_nodes = self._child_nodes.copy()
        return self._child_nodes

    def _determine_child_nodes(self) -> List[MonteCarloNode]:
        valid_cards = self._valid_card_holder.get_valid_cards(self._jass_carpet)
        if EXISTING_CARD in valid_cards:
            child_nodes: List[MonteCarloNode] = []
            for card in range(len(valid_cards)):
                if EXISTING_CARD == valid_cards[card]:
                    copy_jass_carpet = self._jass_carpet.copy()
                    copy_jass_carpet.add_card(card)
                    copy_valid_card_holder = self._valid_card_holder.copy()
                    copy_valid_card_holder.mark_card_as_invalid(self._jass_carpet.get_current_player(), card)
                    child_nodes.append(
                        MonteCarloNode(self._initial_player, copy_jass_carpet, copy_valid_card_holder, self))
            return child_nodes
        else:
            # player has no valid cards anymore
            return []

    def get_payoff(self) -> np.ndarray:
        return self._jass_carpet.calculate_heuristic(self._initial_player)

    @property
    def w(self):
        return self._w

    @property
    def n(self):
        return self._n

    @property
    def initial_player(self):
        return self._initial_player

    @property
    def jass_carpet(self):
        return self._jass_carpet

    @property
    def valid_card_holder(self):
        return self._valid_card_holder

    @property
    def played_card(self):
        return self._jass_carpet.get_last_played_card()
