import logging
from core.services.bookmaker_coordinator import BookmakerCoordinator
from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger(__name__)

class CoordinatorScheduler:
    def __init__(self, coordinator: BookmakerCoordinator):
        self.coordinator = coordinator
        self.scheduler = BackgroundScheduler()

    def start(self):
        self.scheduler.add_job(
            self.coordinator.refresh_leagues,
            trigger="interval",
            seconds=120,
            id="refresh_leagues"
        )

        self.scheduler.add_job(
            self.coordinator.refresh_matches,
            trigger="interval",
            seconds=15,
            id="refresh_leagues_matches",
            max_instances=1,
            coalesce=True
        )

        self.scheduler.start()
        logger.info("Bot iniciado!")

    def stop(self):
        self.scheduler.shutdown()
        logger.info("Bot finalizado!")