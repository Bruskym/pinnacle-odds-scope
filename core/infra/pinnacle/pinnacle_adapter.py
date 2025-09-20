from datetime import datetime
from typing import List

from core.domain.bookmaker.ibookmaker_adapter import IBookmakerAdapter
from core.domain.models.league import League
from core.domain.models.match import Match
from core.domain.models.odd import Odd
from core.utils.odds_converter import american_to_decimal

class PinnacleAdapter(IBookmakerAdapter):

    def leagues_from_api(self, api_data: list) -> List[League]:
        leagues: List[League] = []

        for item in api_data:
            leagues.append(
                League(
                    id=str(item.get("id")),
                    name=item.get("name", "Unknown League"),
                    country=item.get("group", "Unknown"),
                    matchup_count=item.get("matchupCount", 0)
                )
            )

        return leagues
    
    def matches_from_api(self, api_data: list) -> List[Match]:
        matches: List[Match] = []

        for item in api_data:
            match_id = str(item.get("id") or item.get("parentId"))
            participants = item.get("participants", [])
            home_team = next((p["name"] for p in participants if p.get("alignment")=="home"), "Unknown")
            away_team = next((p["name"] for p in participants if p.get("alignment")=="away"), "Unknown")

            start_time_str = item.get("startTime")
            start_time = datetime.fromisoformat(start_time_str.replace("Z", "+00:00"))

            matches.append(
                Match(
                    match_id=match_id,
                    home_team=home_team,
                    away_team=away_team,
                    start_time=start_time,
                    league_id=str(item.get("league", {}).get("id")),
                )
            )
    
        return matches

    def odds_from_api(self, api_data: list) -> List[Odd]:
        odds: List[Odd] = []

        for market in api_data:
            if market.get("type") == "moneyline" and market.get("period") == 0:
                prices = market.get("prices", [])
                home_odds = american_to_decimal(prices[0].get("price")) if len(prices) > 0 else None
                away_odds = american_to_decimal(prices[1].get("price")) if len(prices) > 1 else None
                draw_odds = american_to_decimal(prices[2].get("price")) if len(prices) > 2 else None

                odds.append(Odd(
                    match_id=str(market.get("matchupId")),
                    home_odds=home_odds,
                    away_odds=away_odds,
                    draw_odds=draw_odds
                ))
                
        return odds