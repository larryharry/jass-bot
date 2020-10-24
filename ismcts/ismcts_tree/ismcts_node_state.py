from __future__ import annotations

import numpy as np
from jass.game.rule_schieber import RuleSchieber

from ismcts.jass_stuff.jass_carpet import JassCarpet
from ismcts.information_set.information_set import InformationSet
from ismcts.jass_stuff.const import EMPTY_TRICK


class ISMCTSNodeState:

    def __init__(self, info_set_obs: InformationSet, jass_carpet: JassCarpet):
        self._info_set = info_set_obs
        self._jass_carpet = jass_carpet
        self._rule = RuleSchieber()

    def get_valid_cards_of_current_player(self) -> np.ndarray:
        playable_cards = self._info_set.info_set_obs.not_allocated_cards
        if self._jass_carpet.current_player == self._info_set.info_set_obs.view_player:
            playable_cards = self._info_set.info_set_obs.view_player_hand

        current_trick = self._jass_carpet.last_trick
        if current_trick.is_completed:
            return self._rule.get_valid_cards(playable_cards, EMPTY_TRICK, 0, self._jass_carpet.trump)
        else:
            return self._rule.get_valid_cards(playable_cards, current_trick.asArray(),
                                              current_trick.index_of_next_missing_card,
                                              self._jass_carpet.trump)

    def remove_card(self, card: int):
        self._info_set.remove_card(card)
        self._jass_carpet.add_card(card)

    @property
    def information_set(self):
        return self._info_set

    @property
    def payoff(self) -> np.ndarray:
        return self._jass_carpet.calculate_heuristic(self._info_set.info_set_obs.view_player)

    @property
    def last_played_card(self) -> int:
        return self._jass_carpet.last_played_card

    def copy(self) -> ISMCTSNodeState:
        information_set = self._info_set.copy()
        jass_carpet = self._jass_carpet.copy()
        return ISMCTSNodeState(information_set, jass_carpet)
