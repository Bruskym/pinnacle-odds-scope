from datetime import datetime, timedelta, timezone
import time
from typing import Dict, List, Optional
from core.domain.bookmaker.ibookmaker_adapter import IBookmakerAdapter
from core.domain.bookmaker.ibookmaker_client import IBookmakerClient
from core.domain.exceptions.bookmaker_exception import MatchesNotFound, OddsNotFound
from core.domain.models.match import Match
from core.domain.repositories.match_repository import MatchRepository
from core.infra.pinnacle.pinnacle_adapter import PinnacleAdapter
from core.services.match_aggregator_service import MatchAggregatorService

class MatchService:
    def __init__(
            self,
            client: IBookmakerClient,
            adapter: IBookmakerAdapter,
            match_repository: MatchRepository,
            league_id: str,
            refresh_interval = 15
    ):
        self.league_id: str = league_id
        self.client = client
        self.adapter = adapter
        self.match_repository = match_repository
        self.refresh_interval = refresh_interval
        self.last_update: Optional[float] = None

    def should_refresh(self) -> bool:
        if self.last_update is None:
            return True
        return (time.time() - self.last_update) >= self.refresh_interval
    
    def fetch_and_store_matches(self) -> None:
        raw_matches = self.client.get_matches(self.league_id)
        if not raw_matches:
            raise MatchesNotFound("A API não retornou nenhuma partida.")
        
        raw_odds = self.client.get_odds(self.league_id)
        if not raw_odds:
            raise OddsNotFound("A API não retornou nenhuma odd.")

        matches = self.adapter.matches_from_api(raw_matches)
        odds = self.adapter.odds_from_api(raw_odds)

        matches_with_odds = MatchAggregatorService.consolidate(matches, odds)

        now = datetime.now(timezone.utc)

        filtered_matches = []
        for match in matches_with_odds:
            if not match.odds:
                continue
            if match.home_team.lower() == "unknown" or match.away_team.lower() == "unknown":
                continue
            if match.start_time - now <= timedelta(minutes=1): 
                continue

            filtered_matches.append(match)

        for match in filtered_matches:
            self.match_repository.save_match(match)
            
        self.last_update = time.time()

    def refresh_matches(self) -> List[Match]:
        if self.should_refresh():
            self.fetch_and_store_matches()

        matches_dict = self.match_repository.list_matches(self.league_id)
        return list(matches_dict.values())
    
    def get_matches_by_league(self):
        return self.match_repository.list_matches(self.league_id)
