import logging
from concurrent import futures
from multiprocessing.context import Process

from jass.game.const import card_strings
from jass.game.game_observation import GameObservation
import logging
from ismcts.information_set.information_set_factory import InformationSetFactory
from ismcts.ismcts_tree.default_policy import DefaultPolicy
from ismcts.ismcts_tree.default_policy_random import DefaultPolicyRandom
from ismcts.ismcts_tree.icmcts_algorithm import ISMCTSAlgorithm
from ismcts.ismcts_tree.ismcts_node import ISMCTSNode
from ismcts.ismcts_tree.ismcts_node_state import ISMCTSNodeState
from ismcts.ismcts_tree.tree_policy import TreePolicy
from ismcts.ismcts_tree.tree_policy_ucb1 import TreePolicyUCB1
from ismcts.jass_stuff.jass_carpet import JassCarpet
from multiprocessing.managers import BaseManager
import time


class AlgorithmManager(BaseManager):
    def ISMCTSAlgorithm(self, obs: GameObservation, root_node: ISMCTSNode, tree_policy: TreePolicy,
                        default_policy: DefaultPolicy) -> ISMCTSAlgorithm:
        pass

    def perform(self):
        pass


def run_algorithm_until_timeout(params):
    AlgorithmManager.register('perform')
    m = AlgorithmManager(address=('127.0.0.1', 50000))
    m.connect()

    while True:
        m.perform()
        filename = 'example.log' + str(params[0])
        logging.basicConfig(filename=filename)
        logging.info('Performed')
        if params[1] < time.time():
            break

class ISMCTSCardSelector:


    def __init__(self, obs: GameObservation) -> None:
        self._logger = logging.getLogger(__name__)
        self._obs = obs
        info_set = InformationSetFactory(self._obs).create()
        jass_carpet = JassCarpet.from_obs(self._obs)
        self._root_node = ISMCTSNode(ISMCTSNodeState(info_set, jass_carpet))
        #manager.start()
        #self.ismcts_algorithm = manager.ISMCTSAlgorithm(self._obs, self._root_node, TreePolicyUCB1(),
         #                                               DefaultPolicyRandom())
        self._ismcts_algorithm = ISMCTSAlgorithm(self._obs, self._root_node, TreePolicyUCB1(), DefaultPolicyRandom())
        AlgorithmManager.register('perform', callable=self._ismcts_algorithm.perform)

    def execute_parallel(self, t_end: float):
        paras = [[1, t_end], [2, t_end], [3, t_end],
                 [4, t_end]]
        with futures.ProcessPoolExecutor(max_workers=4) as pool:
            pool.map(run_algorithm_until_timeout, paras, chunksize=1)

    def calculateBestCardForCurrentPlayer(self, search_time_in_sec: int) -> int:
        t_end = time.time() + search_time_in_sec
        self._logger.debug("calculate best card for player {}".format(self._obs.player))
        while True:
            self._ismcts_algorithm.perform()
            if t_end < time.time():
                break

        total_played = 0
        best_card = self._root_node.get_child_nodes()[0].last_played_card
        highest_nbr_of_played_games = 0
        for subtree_root_node in self._root_node.get_child_nodes():
            total_played += subtree_root_node.nbr_of_node_was_played
            if subtree_root_node.nbr_of_node_was_played > highest_nbr_of_played_games:
                highest_nbr_of_played_games = subtree_root_node.nbr_of_node_was_played
                best_card = subtree_root_node.last_played_card
        print(total_played)
        self._logger.debug("best card for player {} is {}".format(self._obs.player, card_strings[best_card]))
        return best_card
