from __future__ import annotations
from __future__ import annotations

import numpy as np

from ismcts.jass_stuff.hand import Hand


class Hands:

    def __init__(self, hands: np.ndarray):
        self._hands = hands

    @classmethod
    def empty(cls):
        return cls(np.full(4, -1))

    @classmethod
    def by_hot_encoded(cls, hot_encoded_hands: np.ndarray) -> Hands:
        hands = cls.empty()
        for player, hot_encoded_hand in enumerate(hot_encoded_hands):
            hands._add_hand(player, Hand.by_hot_encoded(hot_encoded_hand))
        return hands

    def _add_hand(self, player: int, hand: Hand) -> None:
        if self._hands[player] == -1:
            self._hands[player] = hand
        else:
            raise Exception('There is already added hand for user {} '.format(player))

    def is_fully_covered_by(self, hands: Hands) -> bool:
        for player in range(4):
            if not hands._get_hand(player).is_fully_covered_by(self._hands[player]):
                return False
        return True

    def _get_hand(self, player: int) -> Hand:
        if self._hands[player] == -1:
            raise Exception('There is no hand for user {} '.format(player))
        else:
            return self._hands[player]

    def does_player_has_card(self, player: int, card: int) -> bool:
        return card in self._hands[player]

    def remove_card_for_player(self, player: int, card: int) -> None:
        self._hands[player].remove_card(card)

    def copy(self) -> Hands:
        hands = Hands.empty()
        for i in range(4):
            hands._add_hand(i, self._hands[i])
        return hands

