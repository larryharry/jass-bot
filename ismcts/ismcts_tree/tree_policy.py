from __future__ import annotations

from abc import abstractmethod, ABC
from typing import List

from ismcts.ismcts_tree.ismcts_node import ISMCTSNode


class TreePolicy(ABC):

    @abstractmethod
    def selection(self, nodes: List[ISMCTSNode]) -> ISMCTSNode:
        pass
