from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal, TypedDict

if TYPE_CHECKING:
    import pylast


class ScrobblerConfig(TypedDict):
    enabled: bool
    network: Literal["lastfm", "librefm"]
    username: str
    password: str


@dataclass
class NetworkConfig:
    name: str
    network_class: type[pylast.LastFMNetwork | pylast.LibreFMNetwork]
    api_key: str
    api_secret: str
