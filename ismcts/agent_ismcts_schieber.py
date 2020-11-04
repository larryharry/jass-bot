import logging

from jass.agents.agent import Agent
from jass.game.game_observation import GameObservation
from jass.game.rule_schieber import RuleSchieber

from heuristic.trump_prediction.heuristic_trump_builder import HeuristicTrumpBuilder
from ismcts.ismcts_card_selector import ISMCTSCardSelector


class AgentISMCTSSchieber(Agent):

    def __init__(self, max_calculation_time: int = 3):
        # log actions
        self._logger = logging.getLogger(__name__)
        # Use rule object to determine valid actions
        self._rule = RuleSchieber()
        self._max_calculation_time = max_calculation_time
        self._heuristic_trump = HeuristicTrumpBuilder()

    def action_trump(self, obs: GameObservation) -> int:
        trump = self._heuristic_trump.get_trump(obs.forehand == -1, obs.hand)
        self._logger.debug("player {} selected trump: {}".format(obs.player, trump))

        return trump

    def action_play_card(self, obs: GameObservation) -> int:
        return ISMCTSCardSelector(obs).calculateBestCardForCurrentPlayer(self._max_calculation_time)
