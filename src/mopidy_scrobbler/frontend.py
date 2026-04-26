from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING, cast, override

import pykka
import pylast
from mopidy.core import CoreListener

if TYPE_CHECKING:
    from mopidy.config import Config
    from mopidy.core import CoreProxy
    from mopidy.models import TlTrack
    from mopidy.types import DurationMs

    from mopidy_scrobbler.types import ScrobblerConfig

logger = logging.getLogger(__name__)

API_KEY = "2236babefa8ebb3d93ea467560d00d04"
API_SECRET = "94d9a09c0cd5be955c4afaeaffcaefcd"  # noqa: S105


class ScrobblerFrontend(pykka.ThreadingActor, CoreListener):
    lastfm: pylast.LastFMNetwork
    last_start_time: int | None

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
        try:
            self.lastfm = pylast.LastFMNetwork(
                api_key=API_KEY,
                api_secret=API_SECRET,
                username=scrobbler_config["username"],
                password_hash=pylast.md5(scrobbler_config["password"]),
            )
            logger.info("Scrobbler connected to Last.fm")
        except pylast.PyLastError as exc:
            logger.error(f"Error during Last.fm setup: {exc}")  # noqa: TRY400
            self.stop()

    @override
    def track_playback_started(self, tl_track: TlTrack) -> None:
        track = tl_track.track
        artists = ", ".join(sorted([a.name for a in track.artists if a.name]))
        duration = (track.length and track.length // 1000) or 0
        self.last_start_time = int(time.time())
        logger.debug(f"Now playing track: {artists} - {track.name}")
        try:
            self.lastfm.update_now_playing(
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
        artists = ", ".join(sorted([a.name for a in track.artists if a.name]))
        duration_sec = track.length // 1000 if track.length else None
        time_position_sec = time_position // 1000
        if duration_sec is None or duration_sec < 30:
            logger.debug("Track too short to scrobble. (30s)")
            return
        if time_position_sec < duration_sec // 2 and time_position_sec < 240:
            logger.debug("Track not played long enough to scrobble. (50% or 240s)")
            return
        if self.last_start_time is None:
            self.last_start_time = int(time.time()) - duration_sec
        logger.debug(f"Scrobbling track: {artists} - {track.name}")
        try:
            self.lastfm.scrobble(
                artists,
                (track.name or ""),
                self.last_start_time,
                album=((track.album and track.album.name) or ""),
                track_number=track.track_no,
                duration=duration_sec,
                mbid=(str(track.musicbrainz_id) if track.musicbrainz_id else ""),
            )
        except pylast.PyLastError as exc:
            logger.warning(f"Error submitting played track to Last.fm: {exc}")
