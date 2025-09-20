from typing import Dict, List

from core.domain.models.odd import Odd
from core.domain.models.match import Match

class MatchAggregatorService:
    @staticmethod
    def consolidate(matches: List[Match], odds: List[Odd]) -> List[Match]:
        odds_dict: Dict[str, Odd] = {odd.match_id: odd for odd in odds}
        
        for match in matches:
            odd = odds_dict.get(match.match_id)
            if odd:
                match.odds = odd

        return matches
