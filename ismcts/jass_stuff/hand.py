from __future__ import annotations
from __future__ import annotations

from typing import List

import numpy as np


class Hand:

    def __init__(self, hot_encoded_cards: np.ndarray):
        if len(hot_encoded_cards) != 36:
            raise Exception('There should be 36 cards in jass not {} !'.format(hot_encoded_cards))
        self._cards = hot_encoded_cards

    @classmethod
    def by_hot_encoded(cls, hot_encoded_cards: np.ndarray):
        return cls(hot_encoded_cards)

    @classmethod
    def empty(cls):
        return cls(np.full(36, 0))

    @classmethod
    def by_indices(cls, cards_indices: List[int] = None):
        cards = cls.empty()
        cards[cards_indices] = 1
        return cls(cards)

    def add_card(self, card: int):
        if self._cards[card] == 1:
            raise Exception('The card {} is already in this hand!'.format(card))
        else:
            self._cards[card] = 1

    def remove_card(self, card: int):
        if self._cards[card] == 0:
            raise Exception('You cant remove an non existing card! card {}'.format(card))
        else:
            self._cards[card] = 0

    def is_fully_covered_by(self, hand: Hand) -> bool:
        for card in hand._cards:
            if card not in self._cards:
                return False
        return True

    def copy(self) -> Hand:
        return Hand.by_hot_encoded(self._cards.copy())
