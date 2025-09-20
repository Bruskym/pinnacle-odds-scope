from abc import ABC, abstractmethod
from typing import Dict, List
from core.domain.models.match import Match

class INotifierStrategy(ABC):
    @abstractmethod
    def check (self, matches: List[Match]) -> None:
        pass