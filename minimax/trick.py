from __future__ import annotations

import numpy as np
from jass.game.rule_schieber import RuleSchieber

from minimax.const import MISSING_CARD, NBR_OF_CARDS_IN_ONE_TRICK


class Trick:

    def __init__(self, played_cards: np.ndarray, first_player: int, trump: int, is_last_round: bool = False) -> None:
        self._rule = RuleSchieber()
        self._played_cards = played_cards
        self._first_player = first_player
        self._trump = trump
        self._is_last_round = is_last_round

    @classmethod
    def with_played_cards(cls, played_cards: np.ndarray, first_player: int, trump: int,
                          is_last_round: bool = False) -> Trick:
        return Trick(played_cards, first_player, trump, is_last_round)

    @classmethod
    def without_played_cards(cls, first_player: int, trump: int, is_last_round: bool = False) -> Trick:
        played_cards = np.full(NBR_OF_CARDS_IN_ONE_TRICK, MISSING_CARD)
        return Trick(played_cards, first_player, trump, is_last_round)

    def get_winner(self) -> int:
        return self._rule.calc_winner(self._played_cards, self._first_player, self._trump)

    def get_points(self) -> int:
        return self._rule.calc_points(self._played_cards, self._is_last_round)

    def add_card(self, card: int):
        self._played_cards[self._get_index_of_next_missing_card()] = card

    def _get_index_of_next_missing_card(self):
        for index in range(len(self._played_cards)):
            if self._played_cards[index] == MISSING_CARD:
                return index
        return -1

    def is_completed(self) -> bool:
        return MISSING_CARD not in self._played_cards

    def is_in_process(self) -> bool:
        return self._get_index_of_next_missing_card() > 0

    def get_last_played_card(self) -> int:
        if self.is_completed():
            return self._played_cards[NBR_OF_CARDS_IN_ONE_TRICK - 1]
        elif self.is_in_process():
            return self._played_cards[self._get_index_of_next_missing_card() - 1]
        return -1

    def copy(self) -> Trick:
        return Trick(self._played_cards.copy(), self._first_player, self._trump, self._is_last_round)

    def __str__(self) -> str:
        return str(self._played_cards)
