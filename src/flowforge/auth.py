"""Authentication providers."""
from abc import ABC, abstractmethod
import httpx

class AuthProvider(ABC):
    @abstractmethod
    def get_token(self) -> str: ...

class ApiKeyAuth(AuthProvider):
    def __init__(self, api_key: str): self._key = api_key
    def get_token(self) -> str: return self._key

class OAuth2Auth(AuthProvider):
    def __init__(self, client_id: str, client_secret: str, token_url: str):
        self._client_id = client_id
        self._client_secret = client_secret
        self._token_url = token_url
        self._token: str | None = None

    def get_token(self) -> str:
        if not self._token:
            r = httpx.post(self._token_url, data={"grant_type": "client_credentials", "client_id": self._client_id, "client_secret": self._client_secret})
            r.raise_for_status()
            self._token = r.json()["access_token"]
        return self._token
