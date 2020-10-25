from __future__ import annotations
from __future__ import annotations

from jass.game.game_observation import GameObservation

from ismcts.information_set.information_set import InformationSet
from ismcts.information_set.information_set_observation_factory import InformationSetObservationFactory


class InformationSetFactory:

    def __init__(self, game_obs: GameObservation):
        self._inf_set_obs = InformationSetObservationFactory(game_obs).create()

    def create(self) -> InformationSet:
        return InformationSet(self._inf_set_obs)
