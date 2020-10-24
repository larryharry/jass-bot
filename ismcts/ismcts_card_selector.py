import logging
import time

from jass.game.game_observation import GameObservation

from ismcts.information_set.information_set_factory import InformationSetFactory
from ismcts.ismcts_tree.default_policy_random import DefaultPolicyRandom
from ismcts.ismcts_tree.icmcts_algorithm import ISMCTSAlgorithm
from ismcts.ismcts_tree.ismcts_node import ISMCTSNode
from ismcts.ismcts_tree.ismcts_node_state import ISMCTSNodeState
from ismcts.ismcts_tree.tree_policy_ucb1 import TreePolicyUCB1
from ismcts.jass_stuff.jass_carpet import JassCarpet


class ISMCTSCardSelector:

    def __init__(self, obs: GameObservation) -> None:
        self._logger = logging.getLogger(__name__)
        self._obs = obs
        info_set = InformationSetFactory(self._obs).create()
        jass_carpet = JassCarpet.from_obs(self._obs)
        self._root_node = ISMCTSNode(ISMCTSNodeState(info_set, jass_carpet))
        self._ismcts_algorithm = ISMCTSAlgorithm(obs, self._root_node, TreePolicyUCB1(), DefaultPolicyRandom())

    def calculateBestCardForCurrentPlayer(self, search_time_in_sec: int) -> int:
        t_end = time.time() + search_time_in_sec
        self._logger.debug("calculate best card for player " + str(self._obs.player))
        while True:
            self._ismcts_algorithm.perform()
            if t_end < time.time():
                break

        best_card = self._root_node.get_possible_child_nodes()[0].last_played_card
        highest_nbr_of_played_games = 0
        for subtree_root_node in self._root_node.get_possible_child_nodes():
            if subtree_root_node.nbr_of_node_was_played > highest_nbr_of_played_games:
                highest_nbr_of_played_games = subtree_root_node.nbr_of_node_was_played
                best_card = subtree_root_node.last_played_card
        return best_card
