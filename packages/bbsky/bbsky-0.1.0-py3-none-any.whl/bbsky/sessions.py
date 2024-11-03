from collections import OrderedDict
from typing import Any, List, Mapping, Optional, Sequence, Tuple, Union

import httpx
from attrs import define, field
from httpx import QueryParams

from bbsky.config import SkyConfig
from bbsky.constants import API_BASE_URL
from bbsky.tokens import OAuth2Token

# From httpx/_types.py
PrimitiveData = Optional[Union[str, int, float, bool]]
QueryParamTypes = Union[
    "QueryParams",
    Mapping[str, Union[PrimitiveData, Sequence[PrimitiveData]]],
    List[Tuple[str, PrimitiveData]],
    Tuple[Tuple[str, PrimitiveData], ...],
    str,
    bytes,
]
RequestData = Mapping[str, Any]


@define
class User:
    user_id: str
    token: OAuth2Token


def create_authorized_headers(config: SkyConfig, token: OAuth2Token) -> dict[str, str]:
    return {
        "Bb-Api-Subscription-Key": config.subscription_key,
        "Authorization": f"Bearer {token.access_token}",
    }


@define
class SyncUserSession:
    user: User
    config: SkyConfig
    client: httpx.Client = field(init=False, default=None)

    def get_client(self) -> httpx.Client:
        if not self.client or self.client.is_closed:
            self.client = httpx.Client(
                base_url=str(API_BASE_URL),
                headers=create_authorized_headers(self.config, self.user.token),
            )
        return self.client

    def get(self, endpoint: str, params: QueryParamTypes | None = None) -> httpx.Response:
        with self.get_client() as client:
            return client.get(endpoint, params=params)

    def post(
        self, endpoint: str, params: QueryParamTypes | None = None, data: RequestData | None = None
    ) -> httpx.Response:
        with self.get_client() as client:
            return client.post(endpoint, params=params, json=data)


class SyncSessionManager:
    """
    Manages multiple user sessions for the Blackbaud Sky API.

    Sessions are stored in a dict, with the user ID as the key.
    If the number of sessions exceeds the max_sessions, the oldest session is removed.
    This is to prevent the dictionary from growing indefinitely.

    """

    def __init__(self, config: SkyConfig, max_sessions: int = 10):
        self.config = config
        self.sessions: OrderedDict[str, SyncUserSession] = OrderedDict()
        self.max_sessions = max_sessions

    def __repr__(self):
        return f"SyncSessionManager(num_sessions={self.num_sessions}, max_sessions={self.max_sessions})"

    @property
    def num_sessions(self) -> int:
        return len(self.sessions)

    def add_session(self, user: User):
        self.sessions[user.user_id] = SyncUserSession(user=user, config=self.config)

        if len(self.sessions) > self.max_sessions:
            self.sessions.popitem(last=False)

    def find_session(self, user_id: str) -> Optional[SyncUserSession]:
        return self.sessions.get(user_id, None)

    def get_session(self, user_id: str) -> SyncUserSession:
        session = self.find_session(user_id)
        if session is None:
            raise ValueError(f"No session found for user ID: {user_id}")
        return session

    def has_session(self, user_id: str) -> bool:
        return user_id in self.sessions

    def remove_session(self, user_id: str):
        self.sessions.pop(user_id)

    def clear_sessions(self):
        self.sessions.clear()
