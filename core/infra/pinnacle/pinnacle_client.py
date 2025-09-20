import requests

from typing import Any, Dict, List
from config.pinnacle_config import HEADERS, LEAGUES_URL
from core.domain.auth.iauth_provider import IAuthProvider
from core.domain.bookmaker.ibookmaker_client import IBookmakerClient

class PinnacleClient(IBookmakerClient):
    
    def __init__(self, auth_provider: IAuthProvider):
        self._auth = auth_provider
    
    def build_headers(self, api_key: str) -> Dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Referer": "https://www.pinnacle.com/",
            "User-Agent": HEADERS["User-Agent"],
            "X-API-Key": api_key,
        }
    
    def _get(self, url: str) -> List[Dict[str, Any]]:
        headers = self.build_headers(self._auth.get_token())
        resp = requests.get(url, headers=headers)

        resp.raise_for_status()

        return resp.json() or []

    def get_leagues(self) -> List[Dict[str, Any]]:
        return self._get(LEAGUES_URL)
    
    def get_matches(self, league_id: str) -> List[Dict[str, Any]]:
        url = f"https://guest.api.arcadia.pinnacle.com/0.1/leagues/{league_id}/matchups?brandId=0"
        return self._get(url)

    def get_odds(self, league_id: str) -> List[Dict[str, Any]]:
        url = f"https://guest.api.arcadia.pinnacle.com/0.1/leagues/{league_id}/markets/straight"
        return self._get(url)