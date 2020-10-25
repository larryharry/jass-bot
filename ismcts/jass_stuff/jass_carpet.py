from __future__ import annotations

import numpy as np
from jass.game.const import partner_player, next_player
from jass.game.game_observation import GameObservation

from ismcts.jass_stuff.const import MISSING_CARD_IN_TRICK
from ismcts.jass_stuff.hand import Hand
from ismcts.jass_stuff.trick import Trick


class JassCarpet:

    def __init__(self, tricks: np.ndarray, last_played_card: int, current_player: int, trump: int) -> None:
        self._tricks = tricks
        self._last_player = -1
        self._current_player = current_player
        self._trump = trump
        self._last_played_card = last_played_card

    @classmethod
    def from_obs(cls, obs: GameObservation) -> JassCarpet:
        tricks = np.array([])
        for trick_index in range(obs.nr_tricks + 1):
            trick = Trick.with_played_cards(obs.tricks[trick_index],
                                            obs.trick_first_player[trick_index],
                                            obs.trump, trick_index >= 8)
            tricks = np.append(tricks, trick)
            if not trick.is_completed:
                break
        last_played_card = obs.tricks[obs.nr_tricks][obs.nr_cards_in_trick - 1]
        return cls(tricks, last_played_card, obs.player, obs.trump)

    def add_card(self, card: int) -> None:
        self._last_player = self._current_player
        self._last_played_card = card

        last_trick = self.last_trick
        if last_trick.is_completed:
            # winner of last trick is first player on new trick
            first_player = last_trick.winner
            new_trick = Trick.without_played_cards(first_player, self._trump, len(self._tricks) >= 8)
            new_trick.add_card(card)
            self._tricks = np.append(self._tricks, [new_trick])
            self._current_player = next_player[first_player]
        else:
            last_trick.add_card(card)
            if last_trick.is_completed:
                self._current_player = last_trick.winner
            else:
                self._current_player = next_player[self._current_player]

    def calculate_heuristic(self, player_view: int) -> np.ndarray:
        heuristic_value = np.array([0, 0])
        for trick in self._tricks:
            winner = trick.winner
            if player_view == winner or partner_player[player_view] == winner:
                heuristic_value[0] += 1
            else:
                heuristic_value[1] += 1
        return heuristic_value

    def remove_already_played_card_from(self, hand: Hand):
        for trick in self._tricks:
            for card in trick.asArray():
                if card == MISSING_CARD_IN_TRICK:
                    return
                hand.remove_card(card)

    @property
    def last_trick(self) -> Trick:
        return self._tricks[len(self._tricks) - 1]

    @property
    def current_player(self) -> int:
        return self._current_player

    @property
    def last_player(self) -> int:
        return self._last_player

    @property
    def last_played_card(self) -> int:
        return self._last_played_card

    @property
    def trump(self) -> int:
        return self._trump

    def copy(self) -> JassCarpet:
        copy_tricks = np.array([])
        for trick in self._tricks:
            copy_tricks = np.append(copy_tricks, trick.copy())
        return JassCarpet(copy_tricks, self._last_played_card, self._current_player, self._trump)
