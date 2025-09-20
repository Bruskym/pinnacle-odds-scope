from dataclasses import dataclass

@dataclass
class League:
    id: str
    name: str
    country: str
    matchup_count: int