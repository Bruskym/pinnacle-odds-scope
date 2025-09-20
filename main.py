import logging
from core.infra.pinnacle.pinnacle_adapter import PinnacleAdapter
from core.infra.pinnacle.pinnacle_auth import PinnacleKeyManager
from core.infra.pinnacle.pinnacle_client import PinnacleClient
from core.infra.repositories.inmemory_league_repository import InMemoryLeagueRepository
from core.infra.repositories.inmemory_match_repository import InMemoryMatchRepository
from core.infra.scheduler.scheduler import CoordinatorScheduler
from core.services.bookmaker_coordinator import BookmakerCoordinator

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    
    pinnacle_auth_provider = PinnacleKeyManager()
    client = PinnacleClient(pinnacle_auth_provider)
    adapter = PinnacleAdapter()
    matches_repository = InMemoryMatchRepository()
    leagues_repository = InMemoryLeagueRepository()

    coordinator = BookmakerCoordinator(
        client=client,
        adapter=adapter,
        league_repository=leagues_repository,
        match_repository=matches_repository
    )

    coordinator_scheduler = CoordinatorScheduler(coordinator)
    coordinator_scheduler.start()

    coordinator.refresh_leagues()
    
    try:
        while True:
            pass
    except KeyboardInterrupt:
        coordinator_scheduler.stop()