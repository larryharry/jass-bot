import logging
import sys

from jass.game.game_state import GameState

from minimax.const import MISSING_CARD
from minimax.jass_carpet import JassCarpet
from minimax.minimax_node import MinimaxNode
from minimax.valid_card_holder import ValidCardHolder


class MinimaxCardSelector:

    def __init__(self, game_state: GameState, nbr_of_tricks_to_look_ahead: int) -> None:
        # log actions
        self._logger = logging.getLogger(__name__)
        self._game_state = game_state
        self._nbr_of_cards_to_look_ahead = nbr_of_tricks_to_look_ahead * 4
        # initially use biggest and smallest int value
        self._start_alpha = -(sys.maxsize - 1)
        self._start_beta = sys.maxsize

    def calculateBestCardForCurrentPlayer(self) -> int:
        self._logger.debug("calculate best card for player " + str(self._game_state.player))
        root_node = MinimaxNode(JassCarpet.from_game_state(self._game_state).copy(),
                                ValidCardHolder.from_game_state(self._game_state).copy())
        # use smallest int value
        best_heuristic_value: int = -(sys.maxsize - 1)
        best_card: int = MISSING_CARD
        for child_node in root_node.get_child_nodes():
            heuristic_value = self._recursive_min_with_pruning(child_node, self._nbr_of_cards_to_look_ahead - 1,
                                                               self._start_alpha, self._start_beta)
            if heuristic_value > best_heuristic_value:
                best_heuristic_value = heuristic_value
                best_card = child_node.get_card()
        return best_card

    def _recursive_max_with_pruning(self, node: MinimaxNode, depth: int, alpha: int, beta: int) -> int:
        if depth == 0 or node.is_leaf_node():
            heuristic_value = node.calculate_heuristic(self._game_state.player)
            self._logger.debug("max node " + str(node._jass_carpet) + " heuristic: " + str(heuristic_value))
            return heuristic_value

        for child_node in node.get_child_nodes():
            alpha = max(alpha, self._recursive_min_with_pruning(child_node, depth - 1, alpha, beta))
            if beta <= alpha:
                break
        return alpha

    def _recursive_min_with_pruning(self, node: MinimaxNode, depth: int, alpha: int, beta: int) -> int:
        if depth == 0 or node.is_leaf_node():
            heuristic_value = node.calculate_heuristic(self._game_state.player)
            self._logger.debug("min node " + str(node._jass_carpet) + " heuristic: " + str(heuristic_value))
            return heuristic_value

        for child_node in node.get_child_nodes():
            beta = min(beta, self._recursive_max_with_pruning(child_node, depth - 1, alpha, beta))
            if beta <= alpha:
                break
        return beta
