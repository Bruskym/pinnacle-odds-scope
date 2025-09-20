import logging
import threading
from typing import Dict
from core.domain.exceptions.bookmaker_exception import LeaguesNotFound, MatchesNotFound, OddsNotFound
from core.services.league_service import LeagueService
from core.services.match_service import MatchService
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.domain.bookmaker.ibookmaker_adapter import IBookmakerAdapter
from core.domain.bookmaker.ibookmaker_client import IBookmakerClient
from core.domain.repositories.league_repository import LeagueRepository
from core.domain.repositories.match_repository import MatchRepository
from core.services.notifier.notifier_service import NotifierService
from core.services.notifier.strategies.odd_drop_strategy import OddDropStrategy

logger = logging.getLogger(__name__)

class BookmakerCoordinator:
    def __init__(
            self,
            client: IBookmakerClient,
            adapter: IBookmakerAdapter,
            league_repository: LeagueRepository,
            match_repository: MatchRepository,
    ):
        self.league_service = LeagueService(
            client=client,
            adapter=adapter,
            league_repository=league_repository,
            refresh_interval=120
        )

        self.client = client
        self.adapter = adapter
        self._match_services: Dict[str, MatchService] = {}
        self.match_repository = match_repository
        self.notify_service = NotifierService(OddDropStrategy(drop_threshold=0.10))
        self._services_lock = threading.RLock()
        self._max_workers = 10

    def refresh_leagues(self):
        with self._services_lock:
            leagues = self.league_service.refresh_leagues()

            for league in leagues:
                if not league.id in self._match_services:
                    self._match_services[league.id] = MatchService(
                        client=self.client,
                        adapter=self.adapter,
                        match_repository=self.match_repository,
                        league_id=league.id,
                        refresh_interval=15
                    )

    def refresh_matches(self):
        with self._services_lock:
            services_snapshot = list(self._match_services.items())

        if not services_snapshot:
            return
        
        workers = min(len(services_snapshot), self._max_workers)
        with ThreadPoolExecutor(max_workers=workers) as executor:
            future_to_leagues = {
                executor.submit(service.refresh_matches): league_id for league_id, service in services_snapshot
            }

            for future in as_completed(future_to_leagues):
                league_id = future_to_leagues[future]
                
                try:
                    matches = future.result()
                    if matches:
                        self.notify_service.run(matches)
                except MatchesNotFound:
                    league = self.league_service.get_league(league_id)

                    if league:
                        name = league.name
                        logger.warning(f"A liga de nome {name} não retornou partida")
                        continue
                    logger.warning(f"A liga de id {league_id} não retornou partida")

                except OddsNotFound:
                    logger.warning(f"A liga de id {league_id} não retornou nenhuma odd")
                    
                except Exception as e:
                    logger.exception("Erro ao atualizar liga %s: %s", league_id, e)
                    continue
