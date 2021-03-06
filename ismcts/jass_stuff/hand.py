from __future__ import annotations
from __future__ import annotations

from typing import List

import numpy as np

from ismcts.jass_stuff.const import EXISTING_CARD


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
    def by_cards(cls, cards: List[int] = None):
        hot_encoded_cards = np.full(36, 0)
        for card in cards:
            hot_encoded_cards[card] = 1
        return cls.by_hot_encoded(hot_encoded_cards)

    def add_card(self, card: int):
        if self._cards[card] == 1:
            raise Exception('The card {} is already in this hand!'.format(card))
        else:
            self._cards[card] = 1

    def remove_card(self, card: int):
        self._cards[card] = 0

    def is_fully_covered_by(self, hand: Hand) -> bool:
        for card in [i for i, card in enumerate(self._cards) if card == 1]:
            if hand._cards[card] == 0:
                return False
        return True

    @property
    def number_of_cards(self):
        return np.count_nonzero(self._cards == 1)

    def asArray(self):
        return self._cards

    def copy(self) -> Hand:
        return Hand.by_hot_encoded(self._cards.copy())

    def take_cards_from(self, cards) -> int:
        number_of_cards_removed = 0
        for card in [i for i, card in enumerate(self._cards) if card == 1]:
            if cards[card] == EXISTING_CARD:
                cards[card] = 0
                number_of_cards_removed += 1
        return number_of_cards_removed
