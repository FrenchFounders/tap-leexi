"""REST client handling, including LeexiStream base class."""

from __future__ import annotations

import typing as t
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream
from requests.auth import HTTPBasicAuth

if t.TYPE_CHECKING:
    from singer_sdk.helpers.types import Context

    
class LeexiStream(RESTStream):
    """Leexi stream class."""

    @property
    def url_base(self) -> str:
        return "https://public-api.leexi.ai/v1/"

    @property
    def authenticator(self) -> HTTPBasicAuth:
        return HTTPBasicAuth(
            username=self.config.get("key_id"),
            password=self.config.get("key_secret"),
        )

    @property
    def http_headers(self) -> dict:
        return {"Accept": "application/json"}