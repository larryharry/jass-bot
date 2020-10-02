import logging
from jass.agents.agent import Agent
from jass.game.const import color_masks
from jass.game.game_observation import GameObservation
from jass.game.game_state import GameState
from jass.game.rule_schieber import RuleSchieber

from minimax.minimax_card_selector import MinimaxCardSelector


class AgentMinimaxSchieber(Agent):

    def __init__(self, game_state: GameState):
        # log actions
        self._logger = logging.getLogger(__name__)
        # Use rule object to determine valid actions
        self._rule = RuleSchieber()
        self._game_state = game_state

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
        return MinimaxCardSelector(self._game_state, 2).calculateBestCardForCurrentPlayer()
