import threading
from typing import Dict, Optional

from core.domain.models.match import Match
from core.domain.repositories.match_repository import MatchRepository

class InMemoryMatchRepository(MatchRepository):
    def __init__(self):
        self._matches: Dict[str, Match] = {}
        self._lock = threading.Lock()

    def save_match(self, match: Match) -> None:
        with self._lock:
            self._matches[match.match_id] = match
        
    def get_match(self, match_id: str) -> Optional[Match]:
        with self._lock:
            return self._matches.get(match_id)

    def list_matches(self, league_id: str | None = None) -> Dict[str, Match]:
        with self._lock:
            if league_id is None:
                return dict(self._matches)
            return {mid: m for mid, m in self._matches.items() if m.league_id == league_id}

    def delete_match(self, match_id: str) -> None:
        with self._lock:
            self._matches.pop(match_id, None)