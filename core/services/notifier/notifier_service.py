from typing import List
from core.domain.models.match import Match
from core.services.notifier.strategies.inotify_strategy import INotifierStrategy

class NotifierService():
    def __init__(self, strategy: INotifierStrategy):
        self.strategy = strategy

    def run(self, matches: List[Match]) -> None:        
        self.strategy.check(matches)