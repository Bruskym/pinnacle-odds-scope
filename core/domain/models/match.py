from core.domain.models.odd import Odd
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Match:
    match_id: str
    home_team: str
    away_team: str
    start_time: datetime
    league_id: str
    odds: Optional[Odd] = None