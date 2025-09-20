from abc import ABC, abstractmethod

class IAuthProvider(ABC):
    
    @abstractmethod
    def get_token(self, force_refresh: bool = False) -> str:
        pass

    @abstractmethod
    def invalidate_token(self) -> None:
        pass