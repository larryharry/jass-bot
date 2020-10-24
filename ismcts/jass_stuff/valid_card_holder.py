from __future__ import annotations

import numpy as np
from jass.game.game_observation import GameObservation
from jass.game.game_state import GameState
from jass.game.rule_schieber import RuleSchieber
from numpy import random

from ismcts.information_set.information_set_factory import InformationSetFactory
from ismcts.jass_stuff.const import EMPTY_TRICK
from ismcts.jass_stuff.hand import Hand
from ismcts.jass_stuff.hands import Hands
from ismcts.jass_stuff.jass_carpet import JassCarpet


class ValidCardHolder:

    def __init__(self, hands: Hands, trump: int):
        self._hands = hands
        self._trump = trump
        self._rule = RuleSchieber()

    @classmethod
    def from_game_state(cls, game_state: GameState):
        # 4 player, 36 hot encoded cards
        hands = Hands.by_hot_encoded(game_state.hands.copy())
        trump = game_state.trump
        return cls(hands, trump)

    def get_valid_cards(self, jass_carpet: JassCarpet) -> np.array:
        hand = self._hands.get_hand(jass_carpet.current_player)
        current_trick = jass_carpet.last_trick

        if current_trick.is_completed:
            return self._rule.get_valid_cards(hand.asArray(), EMPTY_TRICK, 0, self._trump)
        else:
            return self._rule.get_valid_cards(hand.asArray(), current_trick.asArray(),
                                              current_trick.index_of_next_missing_card, self._trump)

    def mark_card_as_invalid(self, player: int, card: int) -> None:
        self.get_hand(player)[card] = 0

    def copy(self) -> ValidCardHolder:
        return ValidCardHolder(self._hands.copy(), self._trump)

    def get_hand(self, player: int) -> Hand:
        return self._hands.get_hand(player)

    def get_hands(self) -> Hands:
        return self._hands

    @classmethod
    def random_from_obs(cls, obs: GameObservation):
        info_set = InformationSetFactory(obs).create()
        hands = random.choice(info_set.possible_hands)
        trump = obs.trump
        return cls(hands, trump)
