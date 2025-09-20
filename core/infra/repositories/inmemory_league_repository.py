import threading
from typing import Dict, Optional
from core.domain.models.league import League
from core.domain.repositories.league_repository import LeagueRepository


class InMemoryLeagueRepository(LeagueRepository):
    def __init__(self):
        self._leagues: Dict[str, League] = {}
        self._lock = threading.Lock()

    def save_league(self, league: League) -> None:
        with self._lock:
            self._leagues[league.id] = league

    def get_league(self, league_id: str) -> Optional[League]:
        with self._lock:
            return self._leagues.get(league_id)

    def get_all_leagues(self) -> Dict[str, League]:
        with self._lock:
            return dict(self._leagues)

    def list_leagues(self) -> list[League]:
        with self._lock:
            return list(self._leagues.values())

    def delete_league(self, league_id: str) -> None:
        with self._lock:
            if league_id in self._leagues:
                del self._leagues[league_id]
