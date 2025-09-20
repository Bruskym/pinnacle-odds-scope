import time
from typing import Dict, List, Optional
from core.domain.bookmaker.ibookmaker_adapter import IBookmakerAdapter
from core.domain.bookmaker.ibookmaker_client import IBookmakerClient
from core.domain.exceptions.bookmaker_exception import LeaguesNotFound
from core.domain.models.league import League
from core.domain.repositories.league_repository import LeagueRepository

class LeagueService:
    def __init__(
        self,
        client: IBookmakerClient,
        adapter: IBookmakerAdapter,
        league_repository: LeagueRepository,
        refresh_interval = 120
    ):
        self.client = client
        self.adapter = adapter
        self.league_repository = league_repository
        self.refresh_interval = refresh_interval
        self.last_update: Optional[float] = None
        self._leagues_cache: Dict[str, League] = {}

    def should_refresh(self) -> bool:
        if self.last_update is None:
            return True
        return (time.time() - self.last_update) >= self.refresh_interval
    
    def fetch_and_store_leagues(self) -> None:
        raw_leagues = self.client.get_leagues()

        if not raw_leagues:
            raise LeaguesNotFound("O servidor não retornou nenhuma liga")
        
        leagues = self.adapter.leagues_from_api(raw_leagues)
        
        for league in leagues:
            self.league_repository.save_league(league)

        self._leagues_cache.clear()
        self.last_update = time.time()
    
    
    def get_league(self, league_id: str) -> Optional[League]:
        if league_id in self._leagues_cache:
            return self._leagues_cache[league_id]
        
        league = self.league_repository.get_league(league_id)
        if league:
            self._leagues_cache[league_id] = league
        
        return league

    def _get_all_leagues(self) -> List[League]:
        if not self._leagues_cache:
            leagues = self.league_repository.get_all_leagues()
            self._leagues_cache = {**leagues}

        leagues_dict = self._leagues_cache.copy()

        return list(leagues_dict.values())
    
    def refresh_leagues(self) -> List[League]:
        if self.should_refresh():
            self.fetch_and_store_leagues()

        return self._get_all_leagues()
    

