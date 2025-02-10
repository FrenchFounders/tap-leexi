from __future__ import annotations
import typing as t
from typing import Optional, Any
from importlib import resources
from singer_sdk import typing as th
from tap_leexi.client import LeexiStream
from singer_sdk.pagination import BaseAPIPaginator, BasePageNumberPaginator
from math import ceil
from pathlib import Path
import json

SCHEMAS_DIR = Path(__file__).parent / "schemas"


class LeexiPaginator(BasePageNumberPaginator):

    def has_more(self, response) -> bool:
        data = response.json()
        pagination = data.get("pagination")
        total_items = pagination.get("count")
        items_per_page = pagination.get("items")

        total_pages = ceil(total_items / items_per_page)

        return self._value < total_pages
    

class CallsListStream(LeexiStream):
    name = "calls_list"
    path = "calls"
    primary_keys: t.ClassVar[list[str]] = ["uuid"]
    replication_key = "updated_at"
    records_jsonpath = "$.data[*]"
    schema_filepath = SCHEMAS_DIR / "calls_list.json"
    next_page_token_jsonpath = "$.pagination.page"

    def get_url_params(
        self, 
        context: Optional[dict], 
        next_page_token: Optional[Any]
    ) -> dict[str, Any]:
        params = {
            "items": 100,
            "order": "updated_at asc",
        }
        replication_date = self.get_starting_replication_key_value(context)
        if replication_date:
            params["from"] = replication_date
        
        if next_page_token:
            params["page"] = next_page_token
        return params

    def get_new_paginator(self) -> BaseAPIPaginator:
        return LeexiPaginator(1)

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        call_uuid = record.get("uuid")
        return {"uuid": call_uuid}
    

class CallDetailsStream(LeexiStream):
    name = "call_details"
    path = "calls/{uuid}"
    primary_keys: t.ClassVar[list[str]] = ["uuid"]
    schema_filepath = SCHEMAS_DIR / "call_details.json"
    records_jsonpath = "$.data"
    parent_stream_type = CallsListStream