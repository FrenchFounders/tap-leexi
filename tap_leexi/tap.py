"""Leexi tap class."""

from singer_sdk import Tap
from singer_sdk import typing as th

from tap_leexi import streams

class TapLeexi(Tap):
    """Leexi tap class."""

    name = "tap-leexi"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "key_id",
            th.StringType,
            required=True,
            secret=True,
            title="API Key ID",
            description="The Leexi API Key ID for authentication",
        ),
        th.Property(
            "key_secret",
            th.StringType,
            required=True,
            secret=True,
            title="API Key Secret",
            description="The Leexi API Key Secret for authentication",
        )
    ).to_dict()

    def discover_streams(self) -> list[streams.LeexiStream]:
        """Return a list of discovered streams."""
        return [
            streams.CallsListStream(self),
            streams.CallDetailsStream(self),
        ]