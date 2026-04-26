from __future__ import annotations

from typing import TYPE_CHECKING
from unittest import mock
from uuid import UUID

import pylast
import pytest
from mopidy import models
from mopidy.types import DurationMs, TracklistId, Uri

from mopidy_scrobbler.frontend import API_KEY, API_SECRET, ScrobblerFrontend

if TYPE_CHECKING:
    from collections.abc import Generator


@pytest.fixture
def pylast_mock() -> Generator[mock.MagicMock]:
    with mock.patch("mopidy_scrobbler.frontend.pylast", spec=pylast) as m:
        m.PyLastError = pylast.PyLastError
        yield m


@pytest.fixture
def frontend() -> ScrobblerFrontend:
    config = {
        "scrobbler": {"username": "alice", "password": "secret"},
        "proxy": {
            "scheme": None,
            "hostname": None,
            "port": None,
            "username": None,
            "password": None,
        },
    }
    core = mock.sentinel.core
    return ScrobblerFrontend(
        config=config,  # pyright: ignore[reportArgumentType]
        core=core,
    )


def test_on_start_creates_lastfm_network(
    pylast_mock: mock.MagicMock,
    frontend: ScrobblerFrontend,
) -> None:
    pylast_mock.md5.return_value = mock.sentinel.password_hash

    frontend.on_start()

    pylast_mock.LastFMNetwork.assert_called_with(
        api_key=API_KEY,
        api_secret=API_SECRET,
        username="alice",
        password_hash=mock.sentinel.password_hash,
        proxy=None,
    )


def test_on_start_passes_configured_proxy(
    pylast_mock: mock.MagicMock,
    frontend: ScrobblerFrontend,
) -> None:
    pylast_mock.md5.return_value = mock.sentinel.password_hash
    frontend.config["proxy"] = {  # pyright: ignore[reportIndexIssue]
        "scheme": "https",
        "hostname": "proxy.example.com",
        "port": 8080,
        "username": "bob",
        "password": "hunter2",
    }

    frontend.on_start()

    pylast_mock.LastFMNetwork.assert_called_with(
        api_key=API_KEY,
        api_secret=API_SECRET,
        username="alice",
        password_hash=mock.sentinel.password_hash,
        proxy="https://bob:hunter2@proxy.example.com:8080",
    )


def test_on_start_stops_actor_on_error(
    pylast_mock: mock.MagicMock,
    frontend: ScrobblerFrontend,
) -> None:
    pylast_mock.NetworkError = pylast.NetworkError
    pylast_mock.LastFMNetwork.side_effect = pylast.NetworkError(None, "foo")
    frontend.stop = mock.Mock()

    frontend.on_start()

    frontend.stop.assert_called_with()


def test_track_playback_started_updates_now_playing(
    pylast_mock: mock.MagicMock,
    frontend: ScrobblerFrontend,
) -> None:
    frontend.lastfm = mock.Mock(spec=pylast.LastFMNetwork)
    artists = frozenset([models.Artist(name="ABC"), models.Artist(name="XYZ")])
    album = models.Album(name="The Collection")
    track = models.Track(
        uri=Uri("test:123"),
        name="One Two Three",
        artists=artists,
        album=album,
        track_no=3,
        length=DurationMs(180432),
        musicbrainz_id=UUID("59e2b08a-f428-4db6-85aa-a757f026aa2a"),
    )
    tl_track = models.TlTrack(track=track, tlid=TracklistId(17))

    frontend.track_playback_started(tl_track)

    frontend.lastfm.update_now_playing.assert_called_with(
        "ABC, XYZ",
        "One Two Three",
        duration="180",
        album="The Collection",
        track_number="3",
        mbid="59e2b08a-f428-4db6-85aa-a757f026aa2a",
    )


def test_track_playback_started_has_default_values(
    pylast_mock: mock.MagicMock,
    frontend: ScrobblerFrontend,
) -> None:
    frontend.lastfm = mock.Mock(spec=pylast.LastFMNetwork)
    track = models.Track(uri=Uri("test:foo"))
    tl_track = models.TlTrack(track=track, tlid=TracklistId(17))

    frontend.track_playback_started(tl_track)

    frontend.lastfm.update_now_playing.assert_called_with(
        "", "", duration="0", album="", track_number="0", mbid=""
    )


def test_track_playback_started_catches_pylast_error(
    pylast_mock: mock.MagicMock,
    frontend: ScrobblerFrontend,
) -> None:
    frontend.lastfm = mock.Mock(spec=pylast.LastFMNetwork)
    pylast_mock.NetworkError = pylast.NetworkError
    frontend.lastfm.update_now_playing.side_effect = pylast.NetworkError(None, "foo")
    track = models.Track(uri=Uri("test:foo"))
    tl_track = models.TlTrack(track=track, tlid=TracklistId(17))

    frontend.track_playback_started(tl_track)


def test_track_playback_ended_scrobbles_played_track(
    pylast_mock: mock.MagicMock,
    frontend: ScrobblerFrontend,
) -> None:
    frontend.last_start_time = 123
    frontend.lastfm = mock.Mock(spec=pylast.LastFMNetwork)
    artists = frozenset([models.Artist(name="ABC"), models.Artist(name="XYZ")])
    album = models.Album(name="The Collection")
    track = models.Track(
        uri=Uri("test:123"),
        name="One Two Three",
        artists=artists,
        album=album,
        track_no=3,
        length=DurationMs(180432),
        musicbrainz_id=UUID("59e2b08a-f428-4db6-85aa-a757f026aa2a"),
    )
    tl_track = models.TlTrack(track=track, tlid=TracklistId(17))

    frontend.track_playback_ended(tl_track, DurationMs(150000))

    frontend.lastfm.scrobble.assert_called_with(
        "ABC, XYZ",
        "One Two Three",
        123,
        duration=180,
        album="The Collection",
        track_number=3,
        mbid="59e2b08a-f428-4db6-85aa-a757f026aa2a",
    )


def test_track_playback_ended_has_default_values(
    pylast_mock: mock.MagicMock,
    frontend: ScrobblerFrontend,
) -> None:
    frontend.last_start_time = 123
    frontend.lastfm = mock.Mock(spec=pylast.LastFMNetwork)
    track = models.Track(uri=Uri("test:foo"), length=DurationMs(180432))
    tl_track = models.TlTrack(track=track, tlid=TracklistId(17))

    frontend.track_playback_ended(tl_track, DurationMs(150000))

    frontend.lastfm.scrobble.assert_called_with(
        "",
        "",
        123,
        duration=180,
        album="",
        track_number=None,
        mbid="",
    )


def test_does_not_scrobble_tracks_shorter_than_30_sec(
    pylast_mock: mock.MagicMock,
    frontend: ScrobblerFrontend,
) -> None:
    frontend.lastfm = mock.Mock(spec=pylast.LastFMNetwork)
    track = models.Track(uri=Uri("test:foo"), length=DurationMs(20432))
    tl_track = models.TlTrack(track=track, tlid=TracklistId(17))

    frontend.track_playback_ended(tl_track, DurationMs(20432))

    assert frontend.lastfm.scrobble.call_count == 0


def test_does_not_scrobble_if_played_less_than_half(
    pylast_mock: mock.MagicMock,
    frontend: ScrobblerFrontend,
) -> None:
    frontend.lastfm = mock.Mock(spec=pylast.LastFMNetwork)
    track = models.Track(uri=Uri("test:foo"), length=DurationMs(180432))
    tl_track = models.TlTrack(track=track, tlid=TracklistId(17))

    frontend.track_playback_ended(tl_track, DurationMs(60432))

    assert frontend.lastfm.scrobble.call_count == 0


def test_does_scrobble_if_played_not_half_but_240_sec(
    pylast_mock: mock.MagicMock,
    frontend: ScrobblerFrontend,
) -> None:
    frontend.lastfm = mock.Mock(spec=pylast.LastFMNetwork)
    track = models.Track(uri=Uri("test:foo"), length=DurationMs(180432))
    tl_track = models.TlTrack(track=track, tlid=TracklistId(17))

    frontend.track_playback_ended(tl_track, DurationMs(241432))

    assert frontend.lastfm.scrobble.call_count == 1


def test_track_playback_ended_catches_pylast_error(
    pylast_mock: mock.MagicMock,
    frontend: ScrobblerFrontend,
) -> None:
    frontend.lastfm = mock.Mock(spec=pylast.LastFMNetwork)
    pylast_mock.NetworkError = pylast.NetworkError
    frontend.lastfm.scrobble.side_effect = pylast.NetworkError(None, "foo")
    track = models.Track(uri=Uri("test:foo"), length=DurationMs(180432))
    tl_track = models.TlTrack(track=track, tlid=TracklistId(17))

    frontend.track_playback_ended(tl_track, DurationMs(150000))
