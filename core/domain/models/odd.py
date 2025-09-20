from dataclasses import dataclass
from typing import Optional

@dataclass
class Odd:
    match_id: str
    home_odds: Optional[float]
    draw_odds: Optional[float]
    away_odds: Optional[float]