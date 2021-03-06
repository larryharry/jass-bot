import logging

from jass.agents.agent import Agent
from jass.game.const import color_masks
from jass.game.game_observation import GameObservation
from jass.game.rule_schieber import RuleSchieber

from ismcts.ismcts_card_selector_root_parallel_prozess import ISMCTSCardSelector


class AgentISMCTSSchieber(Agent):

    def __init__(self, max_calculation_time: int = 3):
        # log actions
        self._logger = logging.getLogger(__name__)
        # Use rule object to determine valid actions
        self._rule = RuleSchieber()
        self._max_calculation_time = max_calculation_time

    def action_trump(self, obs: GameObservation) -> int:
        trump = 0
        max_number_in_color = 0
        for c in range(4):
            number_in_color = (obs.hand * color_masks[c]).sum()
            if number_in_color > max_number_in_color:
                max_number_in_color = number_in_color
                trump = c
        return trump

    def action_play_card(self, obs: GameObservation) -> int:
        return ISMCTSCardSelector(obs).calculateBestCardForCurrentPlayer(self._max_calculation_time)
