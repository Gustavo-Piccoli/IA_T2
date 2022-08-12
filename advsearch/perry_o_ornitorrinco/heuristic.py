
from abc import ABC, abstractmethod
from advsearch.perry_o_ornitorrinco.node import Node

class Heuristic(ABC):
    @abstractmethod
    def get_state_value(self,node:Node):
        pass