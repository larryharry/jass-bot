from __future__ import annotations
import numpy as np
from ismcts.jass_stuff.hand import Hand


class InformationSetObservation:

    def __init__(self):
        self._view_player = 0
        self._view_hand_player = Hand.empty()
        self._nbr_of_cards_in_hands = np.full(4, 0)
        self._not_allocated_cards = np.full(36, 0)

    @property
    def view_player(self):
        return self._view_player

    @view_player.setter
    def view_player(self, value):
        self._view_player = value

    @property
    def view_player_hand(self):
        return self._view_hand_player

    @view_player_hand.setter
    def view_player_hand(self, value):
        self._view_hand_player = value

    @property
    def not_allocated_cards(self) -> np.ndarray:
        return self._not_allocated_cards

    @not_allocated_cards.setter
    def not_allocated_cards(self, value):
        self._not_allocated_cards = value

    @property
    def nbr_of_cards_in_hands(self):
        return self._nbr_of_cards_in_hands

    @nbr_of_cards_in_hands.setter
    def nbr_of_cards_in_hands(self, value):
        self._nbr_of_cards_in_hands = value

    def copy(self) -> InformationSetObservation:
        info_set_obs = InformationSetObservation()
        info_set_obs.view_player = self._view_player
        info_set_obs.view_player_hand = self._view_hand_player.copy()
        info_set_obs.nbr_of_cards_in_hands = self._nbr_of_cards_in_hands.copy()
        info_set_obs.not_allocated_cards = self._not_allocated_cards.copy()
        return info_set_obs
