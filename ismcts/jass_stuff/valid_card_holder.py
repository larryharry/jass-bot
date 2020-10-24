from __future__ import annotations

import numpy as np
from jass.game.game_observation import GameObservation
from jass.game.game_state import GameState
from jass.game.rule_schieber import RuleSchieber

from ismcts.hands_simulator import HandsSimulator
from minimax.jass_carpet import JassCarpet


class ValidCardHolder:

    def __init__(self, hands: np.array, trump: int):
        self._hands = hands
        self._trump = trump
        self._rule = RuleSchieber()

    @classmethod
    def from_game_state(cls, game_state: GameState):
        # 4 player, 36 hot encoded cards
        hands = game_state.hands.copy()
        trump = game_state.trump
        return cls(hands, trump)

    def get_valid_cards(self, jass_carpet: JassCarpet) -> np.array:
        hand = self._hands[jass_carpet.get_current_player()]
        current_trick = jass_carpet.get_last_trick()

        if current_trick.is_completed():
            return self._rule.get_valid_cards(hand, [-1, -1, -1, -1], 0, self._trump)
        else:
            return self._rule.get_valid_cards(hand, current_trick.asArray(),
                                              current_trick.get_index_of_next_missing_card(), self._trump)

    def mark_card_as_invalid(self, player: int, card: int) -> None:
        self.get_hand(player)[card] = 0

    def copy(self) -> ValidCardHolder:
        return ValidCardHolder(self._hands.copy(), self._trump)

    def get_hand(self, player: int) -> np.ndarray:
        return self._hands[player]

    def get_hands(self) -> np.ndarray:
        return self._hands

    @classmethod
    def random_from_obs(cls, obs: GameObservation):
        # 4 player, 36 hot encoded cards
        hands = HandsSimulator(obs).simulate_hand()
        trump = obs.trump
        return cls(hands, trump)
