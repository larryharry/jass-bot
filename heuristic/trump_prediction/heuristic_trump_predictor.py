from jass.game.const import *

from heuristic.trump_prediction.heuristic_up_down_trump_predictor import UpDownTrumpPrediction


class HeuristicTrumpPredictor:

    def __init__(self, hand: [int], color: int):
        self.color = color
        self._color_save_ticks = 0
        if color == UNE_UFE or color == OBE_ABE:
            up_down_prediction = UpDownTrumpPrediction(hand, color)
            self.could_be_trump = up_down_prediction.could_be_trump
            self.card_count = up_down_prediction.card_count
            self.save_ticks = up_down_prediction.save_tricks
        else:
            self.could_be_trump = self._could_color_be_trump(hand, color)
            self.card_count = self._get_color_count(hand, color)
            self.save_ticks = self._color_save_ticks

    def _could_color_be_trump(self, hand: [int], card_type: int) -> bool:
        if self._has_card(hand, self._card(card_type, J_offset)) \
                and self._has_card(hand, self._card(card_type, Nine_offset)):
            if self._has_card(hand, self._card(card_type, A_offset)) \
                    and self._has_card(hand, self._card(card_type, K_offset)):
                self._color_save_ticks = 4
                return True

        if self._has_card(hand, self._card(card_type, J_offset)) \
                and self._has_card(hand, self._card(card_type, Nine_offset)):
            if self._has_card(hand, self._card(card_type, A_offset)) \
                    or self._has_card(hand, self._card(card_type, K_offset)):
                self._color_save_ticks = 3
                return True

        if self._has_card(hand, self._card(card_type, J_offset)) \
                and self._has_card(hand, self._card(card_type, A_offset)):
            if self._has_card(hand, self._card(card_type, K_offset)) \
                    or self._has_card(hand, self._card(card_type, Q_offset)):
                self._color_save_ticks = 1
                return True

        return False

    def _get_color_count(self, hand: [int], card_type: int):
        cards_per_color = 9
        start = card_type * cards_per_color

        cards_on_hand = 0
        for x in range(cards_per_color):
            if self._has_card(hand, start + x):
                cards_on_hand = cards_on_hand + 1

        return cards_on_hand


    @staticmethod
    def _card(card_type: int, offset: int) -> int:
        return card_type * 9 + offset

    @staticmethod
    def _has_card(hand: [int], card: int) -> bool:
        return hand[card] == 1
