import numpy as np
from jass.game.const import next_player
from jass.game.game_observation import GameObservation

from ismcts.const import MISSING_CARD
from ismcts.information_set.information_set_observation import InformationSetObservation


class InformationSetObservationFactory:

    def __init__(self, game_obs: GameObservation):
        self._game_obs = game_obs

    def create(self) -> InformationSetObservation:
        info_set_obs = InformationSetObservation()
        info_set_obs.view_player = self._game_obs.player
        info_set_obs.view_player_hand = self._game_obs.hand
        info_set_obs.current_player = self._game_obs.player
        info_set_obs.not_allocated_cards = self._get_undistributed_cards()
        info_set_obs.nbr_of_cards_in_hands = self._get_number_of_cards_in_hands()
        return info_set_obs

    def _get_undistributed_cards(self):
        undistributed_cards = np.full(36, 1)
        self._remove_cards_already_played(undistributed_cards)
        self._remove_view_player_hand(undistributed_cards)
        return undistributed_cards

    def _remove_cards_already_played(self, undistributed_cards: np.ndarray):
        for trick in self._game_obs.tricks:
            for card in trick:
                if card == MISSING_CARD:
                    return
                undistributed_cards[card] = 0

    def _remove_view_player_hand(self, undistributed_cards: np.ndarray):
        for card_index in range(36):
            if self._game_obs.hand[card_index] != 0:
                undistributed_cards[card_index] = 0

    def _get_number_of_cards_in_hands(self) -> int:
        number_of_cards_in_hands = np.full(4, 0)
        number_of_cards_in_player_view_hand = self._game_obs.hand.sum()
        player_index = self._game_obs.trick_first_player[self._game_obs.nr_tricks]
        player_already_played = True
        for i in range(4):
            if player_index == self._game_obs.player:
                player_already_played = False

            if player_already_played:
                number_of_cards_in_hands[player_index] = number_of_cards_in_player_view_hand - 1
            else:
                number_of_cards_in_hands[player_index] = number_of_cards_in_player_view_hand
            player_index = next_player[player_index]