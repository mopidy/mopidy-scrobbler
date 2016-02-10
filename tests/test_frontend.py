import logging

import unittest

import mock

from mopidy import models

import pylast

from mopidy_scrobbler import frontend as frontend_lib

logging.basicConfig()


@mock.patch('mopidy_scrobbler.frontend.pylast', spec=pylast)
class FrontendTest(unittest.TestCase):

    def setUp(self):
        self.config = {
            'scrobbler': {
                'lastfm_username': 'alice',
                'lastfm_password': 'secret',
                'librefm_username': '',
                'librefm_password': '',
            }
        }
        self.frontend = frontend_lib.ScrobblerFrontend(
            self.config, mock.sentinel.core)
        self.frontend.lastfm = mock.Mock(spec=pylast.LastFMNetwork)
        self.frontend.networks['Last.fm'] = self.frontend.lastfm

        self.artists = [models.Artist(name='ABC'), models.Artist(name='XYZ')]
        self.track = models.Track(
            name='One Two Three',
            artists=self.artists,
            album=models.Album(name='The Collection'),
            track_no=3,
            length=180432,
            musicbrainz_id='123-456')

    def test_on_start_creates_lastfm_network(self, pylast_mock):
        pylast_mock.md5.return_value = mock.sentinel.password_hash

        self.frontend.on_start()

        pylast_mock.LastFMNetwork.assert_called_with(
            api_key=frontend_lib.LASTFM_API_KEY,
            api_secret=frontend_lib.LASTFM_API_SECRET,
            username='alice',
            password_hash=mock.sentinel.password_hash)

    def test_on_start_stops_actor_on_error(self, pylast_mock):
        pylast_mock.NetworkError = pylast.NetworkError
        pylast_mock.LastFMNetwork.side_effect = pylast.NetworkError(
            None, 'foo')
        self.frontend.stop = mock.Mock()

        self.frontend.on_start()

        self.frontend.stop.assert_called_with()

    def test_track_playback_started_updates_now_playing(self, pylast_mock):
        tl_track = models.TlTrack(track=self.track, tlid=17)

        self.frontend.track_playback_started(tl_track)

        # get_artists() returns the primary artist and thus, we expect 'ABC'
        # instead of 'ABC, XYZ'
        self.frontend.lastfm.update_now_playing.assert_called_with(
            artist='ABC',
            title='One Two Three',
            duration='180',
            album='The Collection',
            track_number='3',
            mbid='123-456')

    def test_track_playback_started_fails_on_missing_artists(self,
                                                             pylast_mock):
        track = models.Track()
        tl_track = models.TlTrack(track=track, tlid=17)

        self.assertRaises(ValueError,
                          self.frontend.track_playback_started,
                          tl_track)

    def test_track_playback_started_catches_pylast_error(self, pylast_mock):
        pylast_mock.ScrobblingError = pylast.ScrobblingError
        self.frontend.lastfm.update_now_playing.side_effect = (
            pylast.ScrobblingError('foo'))
        tl_track = models.TlTrack(track=self.track, tlid=17)

        self.frontend.track_playback_started(tl_track)

    def test_track_playback_ended_scrobbles_played_track(self, pylast_mock):
        self.frontend.last_start_time = 123
        tl_track = models.TlTrack(track=self.track, tlid=17)

        self.frontend.track_playback_ended(tl_track, 150000)

        self.frontend.lastfm.scrobble.assert_called_with(
            artist='ABC',
            title='One Two Three',
            timestamp='123',
            duration='180',
            album='The Collection',
            track_number='3',
            mbid='123-456')

    def test_track_playback_ended_has_default_values(self, pylast_mock):
        self.frontend.last_start_time = 123
        track = models.Track(length=180432, artists=self.artists)
        tl_track = models.TlTrack(track=track, tlid=17)

        self.frontend.track_playback_ended(tl_track, 150000)

        self.frontend.lastfm.scrobble.assert_called_with(
            artist='ABC',
            title='',
            timestamp='123',
            duration='180',
            album='',
            track_number='0',
            mbid='')

    def test_does_not_scrobble_tracks_shorter_than_30_sec(self, pylast_mock):
        track = models.Track(length=20432, artists=self.artists)
        tl_track = models.TlTrack(track=track, tlid=17)

        self.frontend.track_playback_ended(tl_track, 20432)

        self.assertEqual(self.frontend.lastfm.scrobble.call_count, 0)

    def test_does_not_scrobble_if_played_less_than_half(self, pylast_mock):
        track = models.Track(length=180432, artists=self.artists)
        tl_track = models.TlTrack(track=track, tlid=17)

        self.frontend.track_playback_ended(tl_track, 60432)

        self.assertEqual(self.frontend.lastfm.scrobble.call_count, 0)

    def test_does_scrobble_if_played_not_half_but_240_sec(self, pylast_mock):
        track = models.Track(length=880432, artists=self.artists)
        tl_track = models.TlTrack(track=track, tlid=17)

        self.frontend.track_playback_ended(tl_track, 241432)

        self.assertEqual(self.frontend.lastfm.scrobble.call_count, 1)

    def test_track_playback_ended_catches_pylast_error(self, pylast_mock):
        pylast_mock.ScrobblingError = pylast.ScrobblingError
        self.frontend.lastfm.scrobble.side_effect = (
            pylast.ScrobblingError('foo'))
        track = models.Track(length=180432, artists=self.artists)
        tl_track = models.TlTrack(track=track, tlid=17)

        self.frontend.track_playback_ended(tl_track, 150000)

if __name__ == '__main__':
    unittest.main()
