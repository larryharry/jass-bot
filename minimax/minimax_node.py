from __future__ import annotations

from typing import List

from jass.game.game_state import GameState
from jass.game.rule_schieber import RuleSchieber

from minimax.jass_carpet import JassCarpet
from minimax.const import EXISTING_CARD
from minimax.valid_card_holder import ValidCardHolder


class MinimaxNode:

    def __init__(self, jass_carpet: JassCarpet, valid_card_holder: ValidCardHolder):
        self._rule = RuleSchieber()
        self._jass_carpet = jass_carpet
        self._valid_card_holder = valid_card_holder
        self._child_nodes = None
        self._heuristic_value = None

    def is_leaf_node(self) -> bool:
        """Does node have child elements => is last node in search tree"""
        return len(self.get_child_nodes()) == 0

    def calculate_heuristic(self, player_view: int) -> int:
        return self._jass_carpet.calculate_heuristic(player_view)

    def get_child_nodes(self) -> List[MinimaxNode]:
        # lazy load child nodes
        if self._child_nodes is None:
            self._child_nodes = self._determine_child_nodes()
        return self._child_nodes

    def _determine_child_nodes(self) -> List[MinimaxNode]:
        valid_cards = self._valid_card_holder.get_valid_cards(self._jass_carpet.get_current_player())
        if EXISTING_CARD in valid_cards:
            child_nodes: List[MinimaxNode] = []
            for card in range(len(valid_cards)):
                if EXISTING_CARD == valid_cards[card]:
                    copy_jass_carpet = self._jass_carpet.copy()
                    copy_jass_carpet.add_card(card)
                    copy_valid_card_holder = self._valid_card_holder.copy()
                    copy_valid_card_holder.mark_card_as_invalid(self._jass_carpet.get_current_player(), card)
                    child_nodes.append(MinimaxNode(copy_jass_carpet, copy_valid_card_holder))
            return child_nodes
        else:
            # player has no valid cards anymore
            return []

    def get_card(self) -> int:
        return self._jass_carpet.get_last_played_card()
