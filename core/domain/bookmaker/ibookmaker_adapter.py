from abc import ABC, abstractmethod
from typing import List

from core.domain.models.league import League
from core.domain.models.match import Match
from core.domain.models.odd import Odd


class IBookmakerAdapter(ABC):
    @abstractmethod
    def leagues_from_api(self, api_data: list) -> List[League]:
        pass

    @abstractmethod
    def matches_from_api(self, api_data: list) -> List[Match]:
        pass

    @abstractmethod
    def odds_from_api(self, api_data: list) -> List[Odd]:
        pass
