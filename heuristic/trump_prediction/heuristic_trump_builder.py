from heuristic.trump_prediction.heuristic_trump_predictor import HeuristicTrumpPredictor
from jass.game.const import *


class HeuristicTrumpBuilder:

    def __init__(self):
        self._rng = np.random.default_rng()

    def get_trump(self, is_forehand: bool, hand: [int]) -> int:
        schellen_result = HeuristicTrumpPredictor(hand, DIAMONDS)
        rosen_result = HeuristicTrumpPredictor(hand, HEARTS)
        schilten_result = HeuristicTrumpPredictor(hand, SPADES)
        eichel_result = HeuristicTrumpPredictor(hand, CLUBS)
        obe_abe_result = HeuristicTrumpPredictor(hand, OBE_ABE)
        une_ufe_result = HeuristicTrumpPredictor(hand, UNE_UFE)

        trump_results = [schellen_result, rosen_result, schilten_result, eichel_result, obe_abe_result, une_ufe_result]
        possible_trumps = list(filter(lambda r: r.could_be_trump, trump_results))

        if len(possible_trumps) == 0:
            if is_forehand:
                return PUSH
            else:
                max_card_count = max(map(lambda x: x.card_count, trump_results))
                result_most_cards = list(filter(lambda r: r.card_count == max_card_count, trump_results))
                if len(result_most_cards) == 1:
                    return result_most_cards[0].color
                elif len(result_most_cards) > 1:
                    return self._rng.integers(low=0, high=len(result_most_cards) - 1, endpoint=True)
                else:
                    return int(self._rng.integers(low=0, high=MAX_TRUMP, endpoint=True))

        if len(possible_trumps) == 1:
            return possible_trumps[0].color

        if len(possible_trumps) > 1:
            max_save_ticks_count = max(map(lambda x: x.save_ticks, possible_trumps))
            best_trumps_by_save_ticks = list(filter(lambda r: r.save_ticks == max_save_ticks_count, possible_trumps))

            if len(best_trumps_by_save_ticks) == 1:
                return best_trumps_by_save_ticks[0].color
            else:
                max_count = max(map(lambda x: x.card_count, possible_trumps))
                best_trumps_by_card_count = list(filter(lambda r: r.card_count == max_count, possible_trumps))

                if len(best_trumps_by_card_count) == 1:
                    return best_trumps_by_card_count[0].color
                else:
                    random_selection = self._rng.integers(low=0, high=len(best_trumps_by_card_count))
                    return best_trumps_by_card_count[random_selection].color
