import logging
from collections import OrderedDict
from typing import Any, ClassVar, List, Mapping, MutableMapping, Optional, Sequence, Tuple, Union

import httpx
from attrs import asdict, define, field
from httpx import QueryParams

from bbsky.cache import Cache, DiskCache
from bbsky.config import SkyConfig
from bbsky.constants import API_BASE_URL
from bbsky.data_cls import URL
from bbsky.digest import Digest
from bbsky.paths import BBSKY_CACHE_DIR
from bbsky.tokens import OAuth2Token

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

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


@define(frozen=True, slots=True, kw_only=True)
class SearchConstituentsParams:
    """
    Search for constituents in the Blackbaud Sky API.

    See docs:
    https://developer.sky.blackbaud.com/api#api=crm-conmg&operation=SearchConstituents
    """

    id_: Optional[str] = field(default=None, alias="id")
    lookup_id: Optional[str] = field(default=None)
    sort_constituent_name: Optional[str] = field(default=None)
    address: Optional[str] = field(default=None)
    city: Optional[str] = field(default=None)
    state: Optional[str] = field(default=None)
    post_code: Optional[str] = field(default=None)
    country_id: Optional[str] = field(default=None)
    gives_anonymously: Optional[bool] = field(default=None)
    classof: Optional[int] = field(default=None)
    organization: Optional[bool] = field(default=None)
    name: Optional[str] = field(default=None)
    email_address: Optional[str] = field(default=None)
    group: Optional[bool] = field(default=None)
    household: Optional[bool] = field(default=None)
    middle_name: Optional[str] = field(default=None)
    suffixcodeid: Optional[str] = field(default=None)
    phone: Optional[str] = field(default=None)
    prospectmanager: Optional[str] = field(default=None)

    def to_dict(self) -> MutableMapping[str, str]:
        return OrderedDict({k: v for k, v in asdict(self).items() if v is not None})


def create_authorized_headers(config: SkyConfig, token: OAuth2Token) -> dict[str, str]:
    return {
        "Bb-Api-Subscription-Key": config.subscription_key,
        "Authorization": f"Bearer {token.access_token}",
    }


def create_digest_from_request(request: httpx.Request) -> Digest:
    string = ""
    string += f"{request.method} {request.url}\n"
    for k, v in request.headers.items():
        string += f"{k}: {v}\n"
    return Digest.from_data(data=string.encode(encoding="utf-8"), algorithm="sha256")


def create_cache_key_from_request(request: httpx.Request) -> str:
    digest = create_digest_from_request(request)
    return digest.sri


@define
class HTTPSyncClient:
    token: OAuth2Token
    config: SkyConfig
    base_url: ClassVar[URL] = API_BASE_URL
    # cache: Cache[str, Any] = field(factory=InMemoryCache[str, Any])
    cache: Cache[str, Any] = field(factory=lambda: DiskCache[str, Any](cache_dir=BBSKY_CACHE_DIR))
    _client: httpx.Client = field(init=False, default=None, repr=False)

    @property
    def client(self) -> httpx.Client:
        if not self._client or self._client.is_closed:
            self._client = httpx.Client(
                base_url=str(self.base_url),
                headers=create_authorized_headers(self.config, self.token),
            )
        return self._client

    @property
    def headers(self) -> httpx.Headers:
        return httpx.Headers(
            {
                "Bb-Api-Subscription-Key": self.config.subscription_key,
                "Authorization": f"Bearer {self.token.access_token}",
            }
        )

    def build_request(
        self, method: str, endpoint: str, params: QueryParamTypes | None = None, data: RequestData | None = None
    ) -> httpx.Request:
        url = str(self.base_url / endpoint)
        with self.client as client:
            return client.build_request(method=method, url=url, params=params, json=data, headers=self.headers)

    def send_request(self, request: httpx.Request) -> dict[str, Any]:
        cache_key = create_cache_key_from_request(request)
        cached_json_data = self.cache.get(cache_key)
        if cached_json_data:
            print(f"Returning cached response for {request.url}")
            return cached_json_data
        else:
            print(f"Sending request to {request.url}")
            with self.client as client:
                response = client.send(request)
            json_data = response.json()
            self.cache.set(cache_key, json_data)
            print(f"Set cache entry for key: {cache_key}")
            return json_data

    def close(self):
        if self._client:
            self._client.close()


@define
class SkyAPIClient:
    client: HTTPSyncClient

    def search_constituents(self, params: SearchConstituentsParams) -> dict[str, Any]:
        request = self.client.build_request("GET", "crm-conmg/constituents/search", params=params.to_dict())
        return self.client.send_request(request)


# sky_client = SkyAPIClient(client=HTTPSyncClient(token=OAuth2Token.from_cache(), config=SkyConfig.load()))
#
# query = SearchConstituentsParams(classof=1901, name="John Doe")
# data = sky_client.search_constituents(query)
# # print(response)
# # print(response.json())
#
#
# output_path = "output.json"
# _ = Path(output_path).write_text(json.dumps(data, indent=2))
#
#
# data2 = sky_client.search_constituents(query)
# # print(response)
# # print(response.json())
#
#
# output_path = "output2.json"
# _ = Path(output_path).write_text(json.dumps(data, indent=2))
# print(data == data2)


# search = SearchConstituentsParams(classof=1901, name="John Doe")
# print(search)
#
# headers = {
#     "Bb-Api-Subscription-Key": settings.BLACKBAUD_SUBSCRIPTION_KEY,
#     "Authorization": f"Bearer {token_data['access_token']}"
# }
# print(headers)
# # resp = requests.get("https://api.sky.blackbaud.com/constituent/v1/constituents?limit=5", headers=headers)
# resp = requests.get(
# "https://api.sky.blackbaud.com/crm-conmg/constituents/search?constituent_quick_find=smith&limit=5",
# headers=headers
# )
# print(resp)
# print(resp.text)
