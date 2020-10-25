from __future__ import annotations

import logging
from random import sample

import numpy as np
from jass.game.game_observation import GameObservation
from jass.game.game_state import GameState
from jass.game.rule_schieber import RuleSchieber

from ismcts.information_set.information_set_observation_factory import InformationSetObservationFactory
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
        self.get_hand(player).remove_card(card)

    def copy(self) -> ValidCardHolder:
        return ValidCardHolder(self._hands.copy(), self._trump)

    def get_hand(self, player: int) -> Hand:
        return self._hands.get_hand(player)

    def get_hands(self) -> Hands:
        return self._hands

    @classmethod
    def random_from_obs(cls, obs: GameObservation):
        inf_set_obs = InformationSetObservationFactory(obs).create()
        not_allocated_cards_indices = [i for i, card in enumerate(inf_set_obs.not_allocated_cards)
                                       if card == 1]
        sampled_not_allocated_cards = sample(not_allocated_cards_indices, len(not_allocated_cards_indices))
        random_hands = Hands.empty()
        for player in range(4):
            if player == inf_set_obs.view_player:
                random_hands.add_hand(player, inf_set_obs.view_player_hand)
            else:
                hand = Hand.by_cards(sampled_not_allocated_cards[:inf_set_obs.nbr_of_cards_in_hands[player]])
                random_hands.add_hand(player, hand)
                sampled_not_allocated_cards = sampled_not_allocated_cards[
                                              inf_set_obs.nbr_of_cards_in_hands[player]:]

        trump = obs.trump
        return cls(random_hands, trump)
