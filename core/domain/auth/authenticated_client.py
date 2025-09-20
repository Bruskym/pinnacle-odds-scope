from core.domain.exceptions.auth_exception import AuthenticationError
from core.domain.auth.iauth_provider import IAuthProvider

class AuthenticatedClient:

    def __init__(self, auth: IAuthProvider, max_retries: int = 3):
        self.auth = auth
        self.max_retries = max_retries

    def request(self, resquest_func, *args, **kwargs):
        for attempt in range(self.max_retries):
            try:
                token = self.auth.get_token()
                return resquest_func(token, *args, **kwargs)
            except Exception as e:
                if is_auth_error(e):
                    if attempt == self.max_retries - 1:
                        raise AuthenticationError(
                            f"Falha de autenticação após {self.max_retries} tentativas: {e}"
                        )
                    self.auth.invalidate_token()
                    continue
                raise

def is_auth_error(exception) -> bool:
    error_str = str(exception).lower()
    return (
        "401" in error_str
        or "unauthorized" in error_str
        or "authentication" in error_str
        or "invalid key" in error_str
        or "api key" in error_str
    )