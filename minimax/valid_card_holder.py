from __future__ import annotations

import numpy as np
from jass.game.game_state import GameState
from jass.game.game_state_util import observation_from_state
from jass.game.rule_schieber import RuleSchieber


class ValidCardHolder:

    def __init__(self, valid_cards: np.array):
        self._valid_cards = valid_cards

    @classmethod
    def from_game_state(cls, game_state: GameState):
        rule: RuleSchieber = RuleSchieber()
        # 4 player, 16 hot encoded cards
        valid_cards = np.zeros(shape=(4, 36))
        valid_cards[0] = rule.get_valid_cards_from_obs(observation_from_state(game_state, 0))
        valid_cards[1] = rule.get_valid_cards_from_obs(observation_from_state(game_state, 1))
        valid_cards[2] = rule.get_valid_cards_from_obs(observation_from_state(game_state, 2))
        valid_cards[3] = rule.get_valid_cards_from_obs(observation_from_state(game_state, 3))
        return cls(valid_cards)

    def get_valid_cards(self, player: int) -> np.array:
        return self._valid_cards[player]

    def mark_card_as_invalid(self, player, card) -> None:
        self._valid_cards[player][card] = 0

    def copy(self) -> ValidCardHolder:
        return ValidCardHolder(self._valid_cards.copy())
