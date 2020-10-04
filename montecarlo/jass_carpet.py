from __future__ import annotations

from typing import List

import numpy as np
from jass.game.const import partner_player, next_player
from jass.game.game_state import GameState

from minimax.trick import Trick


class JassCarpet:

    def __init__(self, tricks: np.ndarray, current_player: int, trump: int) -> None:
        self._tricks = tricks
        self._current_player = current_player
        self._trump = trump

    @classmethod
    def from_game_state(cls, game_state: GameState) -> JassCarpet:
        tricks = np.array([])
        for trick_index in range(game_state.nr_tricks+1):
            trick = Trick.with_played_cards(game_state.tricks[trick_index],
                                            game_state.trick_first_player[trick_index],
                                            game_state.trump, trick_index >= 8)
            tricks = np.append(tricks, trick)
            if not trick.is_completed:
                break
        return cls(tricks, game_state.player, game_state.trump)

    def add_card(self, card: int) -> None:
        last_trick = self.get_last_trick()
        if last_trick.is_completed():
            # winner of last trick is first player on new trick
            first_player = last_trick.get_winner()
            new_trick = Trick.without_played_cards(first_player, self._trump, len(self._tricks) >= 8)
            new_trick.add_card(card)
            self._tricks = np.append(self._tricks, [new_trick])
            self._current_player = next_player[first_player]
        else:
            last_trick.add_card(card)
            self._current_player = next_player[self._current_player]

    def get_last_trick(self) -> Trick:
        return self._tricks[len(self._tricks) - 1]

    def calculate_heuristic(self, player_view: int) -> np.ndarray:
        heuristic_value = np.array([0, 0])
        for trick in self._tricks:
            winner = trick.get_winner()
            if player_view == winner or partner_player[player_view] == winner:
                heuristic_value[0] += 1
            else:
                heuristic_value[1] += 1
        return heuristic_value

    def copy(self) -> JassCarpet:
        copy_tricks = np.array([])
        for trick in self._tricks:
            copy_tricks = np.append(copy_tricks, trick.copy())
        return JassCarpet(copy_tricks, self._current_player, self._trump)

    def get_current_player(self) -> int:
        return self._current_player

    def get_last_played_card(self) -> int:
        return self.get_last_trick().get_last_played_card()

    def get_trump(self) -> int:
        return self._trump

    def __str__(self):
        str_representation = ""
        for trick in self._tricks:
            str_representation += str(trick)
        return str_representation

