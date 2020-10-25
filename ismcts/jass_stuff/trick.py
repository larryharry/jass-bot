from __future__ import annotations

import numpy as np
from jass.game.rule_schieber import RuleSchieber

from ismcts.jass_stuff.const import MISSING_CARD_IN_TRICK, NBR_OF_CARDS_IN_ONE_TRICK


class Trick:

    def __init__(self, played_cards: np.ndarray, first_player: int, trump: int, is_last_round: bool = False) -> None:
        self._played_cards = played_cards
        self._first_player = first_player
        self._trump = trump
        self._is_last_round = is_last_round
        self._rule = RuleSchieber()

    @classmethod
    def with_played_cards(cls, played_cards: np.ndarray, first_player: int, trump: int,
                          is_last_round: bool = False) -> Trick:
        return Trick(played_cards, first_player, trump, is_last_round)

    @classmethod
    def without_played_cards(cls, first_player: int, trump: int, is_last_round: bool = False) -> Trick:
        played_cards = np.full(NBR_OF_CARDS_IN_ONE_TRICK, MISSING_CARD_IN_TRICK)
        return Trick(played_cards, first_player, trump, is_last_round)

    @property
    def winner(self) -> int:
        return self._rule.calc_winner(self._played_cards, self._first_player, self._trump)

    def add_card(self, card: int):
        self._played_cards[self.index_of_next_missing_card] = card

    @property
    def index_of_next_missing_card(self):
        if not self.is_completed:
            return np.argwhere(self._played_cards == MISSING_CARD_IN_TRICK)[0]
        else:
            return -1

    @property
    def is_completed(self) -> bool:
        return MISSING_CARD_IN_TRICK not in self._played_cards

    @property
    def is_in_process(self) -> bool:
        return self.index_of_next_missing_card > 0

    def asArray(self) -> np.ndarray:
        return self._played_cards

    def copy(self) -> Trick:
        return Trick(self._played_cards.copy(), self._first_player, self._trump, self._is_last_round)

