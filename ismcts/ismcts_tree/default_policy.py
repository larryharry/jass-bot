from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from ismcts.ismcts_tree.ismcts_node import ISMCTSNode


class DefaultPolicy(ABC):

    @abstractmethod
    def selection(self, nodes: List[ISMCTSNode]) -> ISMCTSNode:
        pass
