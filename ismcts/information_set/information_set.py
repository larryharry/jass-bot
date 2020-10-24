from __future__ import annotations
from __future__ import annotations

from typing import Set

from ismcts.jass_stuff.hands import Hands
from ismcts.information_set.information_set_observation import InformationSetObservation


class InformationSet:

    def __init__(self, info_set_obs: InformationSetObservation, possible_hands: Set[Hands]):
        self._info_set_obs = info_set_obs
        self._possible_hands = possible_hands

    def does_contain(self, hands: Hands) -> bool:
        for possible_hands in self._possible_hands:
            if possible_hands.is_fully_covered_by(hands):
                return True
        return False

    @property
    def possible_hands(self):
        return self._possible_hands

    @property
    def info_set_obs(self):
        return self._info_set_obs

    def remove_card(self, card: int) -> InformationSet:
        possible_hands = set({})
        for hands in self._possible_hands:
            if hands.does_player_has_card(self._info_set_obs.current_player, card):
                copy_hands = hands.copy()
                copy_hands.remove_card_for_player(self._info_set_obs.current_player, card)
                possible_hands.add(copy_hands)
        return InformationSet(self._info_set_obs.copy(), possible_hands)

    def copy(self) -> InformationSet:
        info_set_obs = self._info_set_obs.copy()
        possible_hands = self._possible_hands
        return InformationSet(info_set_obs, possible_hands)
