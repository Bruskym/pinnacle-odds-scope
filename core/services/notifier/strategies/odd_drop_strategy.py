import logging
from typing import Dict, List, cast
from core.domain.models.match import Match
from core.services.notifier.strategies.inotify_strategy import INotifierStrategy

logger = logging.getLogger(__name__)

class OddDropStrategy(INotifierStrategy):
    def __init__(
            self, 
            drop_threshold: float = 0.10
    ):
        self.drop_threshold = drop_threshold
        self.previous_odd: Dict[str, Dict[str, float]] = {}

    def check(self, matches: List[Match]) -> None:
        for match in matches: 
            if match.odds is None:
                continue

            if match.home_team == "Unknown" or match.away_team == "Unknown":
                continue

            match_id = match.match_id

            new_odds: Dict[str, float] = {
                "home": cast(float, match.odds.home_odds),
                "away": cast(float, match.odds.away_odds),
                "draw": cast(float, match.odds.draw_odds)
            }

            old_odds = self.previous_odd.get(match_id)

            if old_odds:
                self._compare_and_log(match, old_odds, new_odds)

            self.previous_odd[match_id] = new_odds
            
    def _compare_and_log(self, match: Match, old_odds: Dict[str, float], new_odds: Dict[str, float]):
        drop_detected = False
        for key in ["home", "away", "draw"]:
            old_val = old_odds.get(key)
            new_val = new_odds.get(key)

            if old_val and new_val and new_val < old_val:
                drop_percent = (old_val - new_val) / old_val
                if drop_percent >= self.drop_threshold:
                    drop_detected = True

        if drop_detected:
            logger.info(
                "[ALERTA] %s vs %s | HOME: %.2f (%.2f) | DRAW: %.2f (%.2f) | AWAY: %.2f (%.2f)",
                match.home_team,
                match.away_team,
                (new_odds["home"]), (old_odds.get("home", float("nan"))),
                (new_odds["draw"]), (old_odds.get("draw", float("nan"))),
                (new_odds["away"]), (old_odds.get("away", float("nan"))),
            )