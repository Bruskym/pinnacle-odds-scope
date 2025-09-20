import requests

from typing import Optional
from config.pinnacle_config import APP_CONFIG_URL, HEADERS
from core.domain.auth.iauth_provider import IAuthProvider

class PinnacleKeyManager(IAuthProvider):

    def __init__(self):
        self._api_key: Optional[str] = None
    
    def get_token(self, force_refresh: bool = False) -> str:
        if force_refresh or self._api_key is None:
            self._api_key = self._fetch_apikey()
        
        if self._api_key == None:
            raise Exception("API key not found")
    
        return self._api_key
    
    def _fetch_apikey(self) -> str:
        resp = requests.get(APP_CONFIG_URL, headers=HEADERS)
        resp.raise_for_status()

        return resp.json()["api"]["haywire"]["apiKey"]

    def invalidate_token(self) -> None:
        self._api_key = None