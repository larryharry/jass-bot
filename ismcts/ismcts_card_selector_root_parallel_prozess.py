import logging
import time
from concurrent import futures
from multiprocessing.managers import SharedMemoryManager
from typing import List

from jass.game.const import card_strings
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

    def run_algorithm_until_timeout(self, t_end: int) -> List[int]:
        ismcts_algorithm = ISMCTSAlgorithm(self._obs, self._root_node, TreePolicyUCB1(), DefaultPolicyRandom())
        while True:
            ismcts_algorithm.perform()
            if t_end < time.time():
                break
        nbr_of_nodes_were_played = [0] * len(self._root_node.get_child_nodes())
        for i, subtree_root_node in enumerate(self._root_node.get_child_nodes()):
            nbr_of_nodes_were_played[i] += subtree_root_node.nbr_of_node_was_played
        return nbr_of_nodes_were_played

    def execute_parallel(self, t_end: float) -> List[int]:
        paras = [t_end, t_end, t_end, t_end]
        with futures.ProcessPoolExecutor(max_workers=4) as pool:
            res = pool.map(self.run_algorithm_until_timeout, paras, chunksize=1)
            result_total = []
            for result in res:
                if len(result_total) == 0:
                    result_total.extend(result)
                else:
                    result_total = [sum(x) for x in zip(result_total, result)]
        return result_total

    def calculateBestCardForCurrentPlayer(self, search_time_in_sec: int) -> int:
        t_end = time.time() + search_time_in_sec
        self._logger.debug("calculate best card for player {}".format(self._obs.player))
        nbr_of_nodes_were_played = self.execute_parallel(t_end)

        best_card = self._root_node.get_child_nodes()[0].last_played_card
        highest_nbr_of_played_games = 0
        for i, subtree_root_node in enumerate(self._root_node.get_child_nodes()):
            if nbr_of_nodes_were_played[i] > highest_nbr_of_played_games:
                highest_nbr_of_played_games = nbr_of_nodes_were_played[i]
                best_card = subtree_root_node.last_played_card
        print(sum(nbr_of_nodes_were_played))
        self._logger.debug("best card for player {} is {}".format(self._obs.player, card_strings[best_card]))
        return best_card
