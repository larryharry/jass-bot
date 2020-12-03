from jass.game.const import *


class CardCheckResult:

    def __init__(self, color: int, success: bool):
        self.color = color
        self.success = success


class UpDownTrumpPrediction:

    def __init__(self, hand: [int], color: int):
        self._colors = [DIAMONDS, HEARTS, SPADES, CLUBS]
        self._hand = hand
        self.could_be_trump = self._determine_trump(color == UNE_UFE)
        self.save_tricks = 0
        self.card_count = 0

    def _determine_trump(self, is_une_ufe: bool) -> bool:
        # Alle 6
        if is_une_ufe:
            if self._has_all(Six_offset):
                self.save_tricks = 4
                self.card_count = 4
                return True
            # 6-9 eine farbe
            if self._has_four_same_color([Six_offset, Seven_offset, Eight_offset, Nine_offset]):
                self.card_count = 4
                self.save_tricks = 4
                return True
            # # 6-8 eine farbe + 1 / 2 6 andere farbe
            if self._three_and_one_other([Six_offset, Seven_offset, Eight_offset], [Six_offset]):
                self.save_tricks = 4
                self.card_count = 4
                return True
            # 6-7 eine farbe + 2 6 andere farbe
            if self._two_and_two_other([Six_offset, Seven_offset], [Six_offset]):
                self.save_tricks = 4
                self.card_count = 4
                return True
        else:
            # Alle A
            if self._has_all(A_offset):
                self.save_tricks = 4
                self.card_count = 4
                return True
            # A-J eine farbe
            if self._has_four_same_color([A_offset, K_offset, Q_offset, J_offset]):
                self.save_tricks = 4
                self.card_count = 4
                return True
            # A-Q eine farbe + 1 / 2 A andere farbe
            if self._three_and_one_other([A_offset, K_offset, Q_offset], [A_offset]):
                self.save_tricks = 4
                self.card_count = 4
                return True
            # A-K eine farbe + 2 A andere farbe
            if self._two_and_two_other([A_offset, K_offset], [A_offset]):
                self.save_tricks = 4
                self.card_count = 4
                return True
        return False

    def _has_all(self, card_offset_to_check: int) -> bool:
        results: [CardCheckResult] = []
        offsets_to_check = [card_offset_to_check]
        for color in self._colors:
            results.append(self._get_result(self._hand, color, offsets_to_check))
        if all(filter(lambda r: r.success, results)):
            return True
        return False

    def _has_four_same_color(self, offsets_to_check: [int]):
        results: [CardCheckResult] = []
        for color in self._colors:
            results.append(self._get_result(self._hand, color, offsets_to_check))
        if any(filter(lambda r: r.success, results)):
            return True
        return False

    def _three_and_one_other(self, primary_offsets: [int], secondary_offsets: [int]) -> bool:
        results: [CardCheckResult] = []
        for color in self._colors:
            results.append(self._get_result(self._hand, color, primary_offsets))

        colors_with_match = list(filter(lambda r: r.success, results))
        if len(colors_with_match) == 1:
            results: [CardCheckResult] = []
            other_colors = list(filter(lambda c: c != colors_with_match[0].color, self._colors))
            for color in other_colors:
                results.append(self._get_result(self._hand, color, secondary_offsets))
            if any(filter(lambda r: r.success, results)):
                return True
        elif len(colors_with_match) == 2:
            return True
        return False

    def _two_and_two_other(self, primary_offsets: [int], secondary_offsets: [int]) -> bool:
        results: [CardCheckResult] = []
        for color in self._colors:
            results.append(self._get_result(self._hand, color, primary_offsets))

        colors_with_match = list(filter(lambda r: r.success, results))
        if len(colors_with_match) == 1:
            results: [CardCheckResult] = []
            other_colors = list(filter(lambda c: c != colors_with_match[0].color, self._colors))
            for color in other_colors:
                results.append(self._get_result(self._hand, color, secondary_offsets))
            if len(list(filter(lambda r: r.success, results))) >= 2:
                return True
        elif len(colors_with_match) > 1:
            return True
        return False

    def _get_result(self, hand: [int], color: int, cards_to_check: [int]) -> CardCheckResult:
        results: [bool] = []
        for card_offset in cards_to_check:
            results.append(self._has_card(hand, color * 9 + card_offset))

        if all(results):
            return CardCheckResult(color, True)
        return CardCheckResult(color, False)

    @staticmethod
    def _has_card(hand: [int], card: int) -> bool:
        return hand[card] == 1
