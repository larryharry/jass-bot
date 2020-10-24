from __future__ import annotations
from __future__ import annotations

import itertools

import numpy as np
from jass.game.game_observation import GameObservation

from ismcts.jass_stuff.hand import Hand
from ismcts.jass_stuff.hands import Hands
from ismcts.information_set.information_set import InformationSet
from ismcts.information_set.information_set_observation_factory import InformationSetObservationFactory


class InformationSetFactory:

    def __init__(self, game_obs: GameObservation):
        self._inf_set_obs = InformationSetObservationFactory(game_obs).create()
        self._not_allocated_cards_indices = [i for i, card in enumerate(self._inf_set_obs.not_allocated_cards)
                                             if card == 1]

    def create(self) -> InformationSet:
        possible_hands = set({})
        for permutation_of_card_indices in itertools.permutations(self._not_allocated_cards_indices):
            hands = Hands.empty()
            for player in range(4):
                if player == self._inf_set_obs.view_player:
                    hands.add_hand(player, self._inf_set_obs.view_player_hand)
                else:
                    hand = Hand.by_cards(permutation_of_card_indices[:self._inf_set_obs.nbr_of_cards_in_hands[player]])
                    hands.add_hand(player, hand)
                    permutation_of_card_indices = permutation_of_card_indices[
                                                  self._inf_set_obs.nbr_of_cards_in_hands[player]:]
            possible_hands.add(hands)
        return InformationSet(self._inf_set_obs, possible_hands)
