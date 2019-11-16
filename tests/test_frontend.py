from unittest import mock

import pylast
import pytest

from mopidy import models
from mopidy_scrobbler import frontend as frontend_lib


@pytest.fixture
def pylast_mock():
    with mock.patch("mopidy_scrobbler.frontend.pylast", spec=pylast) as m:
        yield m


@pytest.fixture
def frontend():
    config = {"scrobbler": {"username": "alice", "password": "secret"}}
    core = mock.sentinel.core
    return frontend_lib.ScrobblerFrontend(config, core)


def test_on_start_creates_lastfm_network(pylast_mock, frontend):
    pylast_mock.md5.return_value = mock.sentinel.password_hash

    frontend.on_start()

    pylast_mock.LastFMNetwork.assert_called_with(
        api_key=frontend_lib.API_KEY,
        api_secret=frontend_lib.API_SECRET,
        username="alice",
        password_hash=mock.sentinel.password_hash,
    )


def test_on_start_stops_actor_on_error(pylast_mock, frontend):
    pylast_mock.NetworkError = pylast.NetworkError
    pylast_mock.LastFMNetwork.side_effect = pylast.NetworkError(None, "foo")
    frontend.stop = mock.Mock()

    frontend.on_start()

    frontend.stop.assert_called_with()


def test_track_playback_started_updates_now_playing(pylast_mock, frontend):
    frontend.lastfm = mock.Mock(spec=pylast.LastFMNetwork)
    artists = [models.Artist(name="ABC"), models.Artist(name="XYZ")]
    album = models.Album(name="The Collection")
    track = models.Track(
        name="One Two Three",
        artists=artists,
        album=album,
        track_no=3,
        length=180432,
        musicbrainz_id="123-456",
    )
    tl_track = models.TlTrack(track=track, tlid=17)

    frontend.track_playback_started(tl_track)

    frontend.lastfm.update_now_playing.assert_called_with(
        "ABC, XYZ",
        "One Two Three",
        duration="180",
        album="The Collection",
        track_number="3",
        mbid="123-456",
    )


def test_track_playback_started_has_default_values(pylast_mock, frontend):
    frontend.lastfm = mock.Mock(spec=pylast.LastFMNetwork)
    track = models.Track()
    tl_track = models.TlTrack(track=track, tlid=17)

    frontend.track_playback_started(tl_track)

    frontend.lastfm.update_now_playing.assert_called_with(
        "", "", duration="0", album="", track_number="0", mbid=""
    )


def test_track_playback_started_catches_pylast_error(pylast_mock, frontend):
    frontend.lastfm = mock.Mock(spec=pylast.LastFMNetwork)
    pylast_mock.NetworkError = pylast.NetworkError
    frontend.lastfm.update_now_playing.side_effect = pylast.NetworkError(
        None, "foo"
    )
    track = models.Track()
    tl_track = models.TlTrack(track=track, tlid=17)

    frontend.track_playback_started(tl_track)


def test_track_playback_ended_scrobbles_played_track(pylast_mock, frontend):
    frontend.last_start_time = 123
    frontend.lastfm = mock.Mock(spec=pylast.LastFMNetwork)
    artists = [models.Artist(name="ABC"), models.Artist(name="XYZ")]
    album = models.Album(name="The Collection")
    track = models.Track(
        name="One Two Three",
        artists=artists,
        album=album,
        track_no=3,
        length=180432,
        musicbrainz_id="123-456",
    )
    tl_track = models.TlTrack(track=track, tlid=17)

    frontend.track_playback_ended(tl_track, 150000)

    frontend.lastfm.scrobble.assert_called_with(
        "ABC, XYZ",
        "One Two Three",
        "123",
        duration="180",
        album="The Collection",
        track_number="3",
        mbid="123-456",
    )


def test_track_playback_ended_has_default_values(pylast_mock, frontend):
    frontend.last_start_time = 123
    frontend.lastfm = mock.Mock(spec=pylast.LastFMNetwork)
    track = models.Track(length=180432)
    tl_track = models.TlTrack(track=track, tlid=17)

    frontend.track_playback_ended(tl_track, 150000)

    frontend.lastfm.scrobble.assert_called_with(
        "", "", "123", duration="180", album="", track_number="0", mbid=""
    )


def test_does_not_scrobble_tracks_shorter_than_30_sec(pylast_mock, frontend):
    frontend.lastfm = mock.Mock(spec=pylast.LastFMNetwork)
    track = models.Track(length=20432)
    tl_track = models.TlTrack(track=track, tlid=17)

    frontend.track_playback_ended(tl_track, 20432)

    assert frontend.lastfm.scrobble.call_count == 0


def test_does_not_scrobble_if_played_less_than_half(pylast_mock, frontend):
    frontend.lastfm = mock.Mock(spec=pylast.LastFMNetwork)
    track = models.Track(length=180432)
    tl_track = models.TlTrack(track=track, tlid=17)

    frontend.track_playback_ended(tl_track, 60432)

    assert frontend.lastfm.scrobble.call_count == 0


def test_does_scrobble_if_played_not_half_but_240_sec(pylast_mock, frontend):
    frontend.lastfm = mock.Mock(spec=pylast.LastFMNetwork)
    track = models.Track(length=880432)
    tl_track = models.TlTrack(track=track, tlid=17)

    frontend.track_playback_ended(tl_track, 241432)

    assert frontend.lastfm.scrobble.call_count == 1


def test_track_playback_ended_catches_pylast_error(pylast_mock, frontend):
    frontend.lastfm = mock.Mock(spec=pylast.LastFMNetwork)
    pylast_mock.NetworkError = pylast.NetworkError
    frontend.lastfm.scrobble.side_effect = pylast.NetworkError(None, "foo")
    track = models.Track(length=180432)
    tl_track = models.TlTrack(track=track, tlid=17)

    frontend.track_playback_ended(tl_track, 150000)
