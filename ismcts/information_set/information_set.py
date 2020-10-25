from __future__ import annotations
from __future__ import annotations

from ismcts.information_set.information_set_observation import InformationSetObservation
from ismcts.jass_stuff.hands import Hands


class InformationSet:

    def __init__(self, info_set_obs: InformationSetObservation):
        self._info_set_obs = info_set_obs

    def covered_by(self, hands: Hands) -> bool:
        cards_to_distribute = self._info_set_obs.not_allocated_cards.copy()
        for player in range(4):
            hand = hands.get_hand(player)
            if self._info_set_obs.nbr_of_cards_in_hands[player] > hand.number_of_cards:
                return False

            if player == self._info_set_obs.view_player:
                if not self._info_set_obs.view_player_hand.is_fully_covered_by(hand):
                    return False
            else:
                number_of_removed_cards = hand.take_cards_from(cards_to_distribute)
                if number_of_removed_cards != self._info_set_obs.nbr_of_cards_in_hands[player]:
                    return False
        return True

    @property
    def info_set_obs(self):
        return self._info_set_obs

    def remove_card(self, player, card: int) -> None:
        if player == self._info_set_obs.view_player:
            self._info_set_obs.view_player_hand.remove_card(card)
        else:
            self._info_set_obs.not_allocated_cards[card] = 0
        self._info_set_obs.nbr_of_cards_in_hands[player] -= 1

    def copy(self) -> InformationSet:
        return InformationSet(self._info_set_obs.copy())
