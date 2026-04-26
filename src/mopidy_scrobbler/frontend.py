from __future__ import annotations

import datetime as dt
import logging
from typing import TYPE_CHECKING, cast, override

import pykka
import pylast
from mopidy.core import CoreListener
from mopidy.httpclient import format_proxy

from mopidy_scrobbler.types import NetworkConfig

if TYPE_CHECKING:
    from mopidy.config import Config
    from mopidy.core import CoreProxy
    from mopidy.models import TlTrack
    from mopidy.types import DurationMs

    from mopidy_scrobbler.types import ScrobblerConfig

logger = logging.getLogger(__name__)

NETWORK_CONFIG = {
    "lastfm": NetworkConfig(
        name="Last.fm",
        network_class=pylast.LastFMNetwork,
        api_key="2236babefa8ebb3d93ea467560d00d04",
        api_secret="94d9a09c0cd5be955c4afaeaffcaefcd",  # noqa: S106
    ),
    "librefm": NetworkConfig(
        name="Libre.fm",
        network_class=pylast.LibreFMNetwork,
        #
        # Libre.fm API key may expire 2031-04-25
        api_key="339f358f9ba0dc49e00a400c8cdd773e",
        api_secret="4c3d7cf6f6379cb86e4c08231a347cda",  # noqa: S106
    ),
}

# Limits from https://www.last.fm/api/scrobbling
MIN_DURATION = dt.timedelta(seconds=30)
MIN_PLAYED_TIME = dt.timedelta(minutes=4)
MIN_PLAYED_PERCENT = 50


class ScrobblerFrontend(pykka.ThreadingActor, CoreListener):
    network: pylast.LastFMNetwork | pylast.LibreFMNetwork
    last_start_time: dt.datetime | None

    @override
    def __init__(
        self,
        *,
        config: Config,
        core: CoreProxy,
    ) -> None:
        super().__init__()
        self.config = config
        self.last_start_time = None

    @override
    def on_start(self) -> None:
        scrobbler_config = cast("ScrobblerConfig", self.config["scrobbler"])
        network_config = NETWORK_CONFIG[scrobbler_config["network"]]
        try:
            self.network = network_config.network_class(
                api_key=network_config.api_key,
                api_secret=network_config.api_secret,
                username=scrobbler_config["username"],
                password_hash=pylast.md5(scrobbler_config["password"]),
                proxy=format_proxy(self.config["proxy"]),
            )
            logger.info(f"Scrobbler connected to {network_config.name}")
        except pylast.PyLastError as exc:
            logger.error(f"Error during {network_config.name} setup: {exc}")  # noqa: TRY400
            self.stop()

    @override
    def track_playback_started(self, tl_track: TlTrack) -> None:
        track = tl_track.track
        artists = ", ".join(sorted([a.name for a in track.artists if a.name]))
        duration = (track.length and track.length // 1000) or 0
        self.last_start_time = dt.datetime.now(tz=dt.UTC)
        logger.debug(f"Now playing track: {artists} - {track.name}")
        try:
            self.network.update_now_playing(
                artists,
                (track.name or ""),
                album=((track.album and track.album.name) or ""),
                duration=str(duration),
                track_number=str(track.track_no or 0),
                mbid=(str(track.musicbrainz_id) if track.musicbrainz_id else ""),
            )
        except pylast.PyLastError as exc:
            logger.warning(f"Error submitting playing track to Last.fm: {exc}")

    @override
    def track_playback_ended(
        self,
        tl_track: TlTrack,
        time_position: DurationMs,
    ) -> None:
        track = tl_track.track
        duration = dt.timedelta(milliseconds=track.length) if track.length else None
        position = dt.timedelta(milliseconds=time_position)

        if duration is None or duration < MIN_DURATION:
            logger.debug(
                f"Track too short to scrobble (<{MIN_DURATION.total_seconds()}s)"
            )
            return
        if (
            position < (duration * MIN_PLAYED_PERCENT / 100)
            and position < MIN_PLAYED_TIME
        ):
            logger.debug(
                "Track not played long enough to scrobble: "
                f"{MIN_PLAYED_PERCENT}% or {MIN_PLAYED_TIME.total_seconds()}s"
            )
            return

        if self.last_start_time is None:
            self.last_start_time = dt.datetime.now(tz=dt.UTC) - duration

        artists = ", ".join(sorted([a.name for a in track.artists if a.name]))
        logger.debug(f"Scrobbling track: {artists} - {track.name}")
        try:
            self.network.scrobble(
                artists,
                (track.name or ""),
                round(self.last_start_time.timestamp()),
                album=((track.album and track.album.name) or ""),
                track_number=track.track_no,
                duration=round(duration.total_seconds()),
                mbid=(str(track.musicbrainz_id) if track.musicbrainz_id else ""),
            )
        except pylast.PyLastError as exc:
            logger.warning(f"Error submitting played track to Last.fm: {exc}")
