import logging
import time

import numpy as np
from jass.game.game_state import GameState

from montecarlo.default_policy_random import DefaultPolicyRandom
from montecarlo.jass_carpet import JassCarpet
from montecarlo.monte_carlo_node import MonteCarloNode
from montecarlo.tree_policy_random import TreePolicyRandom
from montecarlo.valid_card_holder import ValidCardHolder


def expand(node_to_expand: MonteCarloNode, default_policy: DefaultPolicyRandom):
    if node_to_expand.has_unexplored_child_nodes():
        explored_node = default_policy.selection_with_remove(node_to_expand.get_unexplored_child_nodes())
        node_to_expand.update(simulate(explored_node, default_policy))
    else:
        # node to expand without unexplored child's is a leaf node
        node_to_expand.update(node_to_expand.get_payoff())


def simulate(node_to_explore: MonteCarloNode, default_policy: DefaultPolicyRandom) -> np.ndarray:
    subtree_root_node = MonteCarloNode(node_to_explore.initial_player, node_to_explore.jass_carpet,
                                       node_to_explore.valid_card_holder)
    child_node = subtree_root_node
    while child_node.has_child_nodes():
        child_node = default_policy.selection(child_node.get_child_nodes())
    return child_node.get_payoff()


class MonteCarloCardSelector:

    def __init__(self, game_state: GameState, nbr_of_tricks_to_look_ahead: int) -> None:
        # log actions
        self._logger = logging.getLogger(__name__)
        self._game_state = game_state
        self._nbr_of_cards_to_look_ahead = nbr_of_tricks_to_look_ahead * 4
        self._total_n = 0
        self._default_policy = DefaultPolicyRandom()
        self._tree_policy = TreePolicyRandom(5)

    def calculateBestCardForCurrentPlayer(self, search_time_in_sec: int) -> int:
        t_end = time.time() + search_time_in_sec
        self._logger.debug("calculate best card for player " + str(self._game_state.player))
        root_node = MonteCarloNode(self._game_state.player, JassCarpet.from_game_state(self._game_state).copy(),
                                   ValidCardHolder.from_game_state(self._game_state).copy())
        while True:
            subtree_root_node = self._tree_policy.selection(self._total_n, root_node.get_child_nodes())
            node_to_expand = self._determine_node_to_expand(subtree_root_node)
            expand(node_to_expand,  self._default_policy)
            self._total_n += 1
            if t_end < time.time():
                break

        best_card = root_node.get_child_nodes()[0].played_card
        highest_nbr_of_played_games = 0
        for subtree_root_node in root_node.get_child_nodes():
            if subtree_root_node.n > highest_nbr_of_played_games:
                highest_nbr_of_played_games = subtree_root_node.n
                best_card = subtree_root_node.played_card
        return best_card

    def _determine_node_to_expand(self, root_node: MonteCarloNode) -> MonteCarloNode:
        node_to_expand = root_node
        while not node_to_expand.has_unexplored_child_nodes() and node_to_expand.has_child_nodes():
            node_to_expand = self._default_policy.selection(node_to_expand.get_child_nodes())
        return node_to_expand
