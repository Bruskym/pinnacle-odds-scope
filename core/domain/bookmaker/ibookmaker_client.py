from abc import ABC, abstractmethod
from typing import List

class IBookmakerClient(ABC):
    @abstractmethod
    def get_leagues(self) -> List[dict]:
        pass

    @abstractmethod
    def get_matches(self, league_id: str) -> List[dict]:
        pass

    @abstractmethod
    def get_odds(self, league_id: str) -> List[dict]:
        pass
