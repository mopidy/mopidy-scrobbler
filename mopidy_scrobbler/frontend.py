from __future__ import unicode_literals

import logging
import time

from mopidy.core import CoreListener

import pykka

import pylast


logger = logging.getLogger(__name__)

API_KEY = '2236babefa8ebb3d93ea467560d00d04'
API_SECRET = '94d9a09c0cd5be955c4afaeaffcaefcd'

PYLAST_ERRORS = tuple(
    getattr(pylast, exc_name)
    for exc_name in (
        'ScrobblingError', 'NetworkError', 'MalformedResponseError', 'WSError')
    if hasattr(pylast, exc_name)
)


class ScrobblerFrontend(pykka.ThreadingActor, CoreListener):
    def __init__(self, config, core):
        super(ScrobblerFrontend, self).__init__()
        self.config = config
        self.lastfm = None
        self.last_start_time = None

    def check_uri_scheme(self, uri):
        uri_scheme = uri.split(':')[0]
        if uri_scheme in self.config['scrobbler']['scrobble_filter']:
            logger.info('Not scrobbling track from %s', uri_scheme)
            return True
        else:
            return False

    def concatenate_artist_names(self, objects):
        names = sorted([a.name for a in objects]);
        if len(names) == 0:
            return ''
        elif len(names) < 3:
            return ' & '.join(names)
        else:
            first_lot = names[:len(names)-1]
            return ', '.join(first_lot) + ' & ' + names[len(names)-1]

    def on_start(self):
        try:
            self.lastfm = pylast.LastFMNetwork(
                api_key=API_KEY, api_secret=API_SECRET,
                username=self.config['scrobbler']['username'],
                password_hash=pylast.md5(self.config['scrobbler']['password']))
            logger.info('Scrobbler connected to Last.fm')
        except PYLAST_ERRORS as e:
            logger.error('Error during Last.fm setup: %s', e)
            self.stop()

    def track_playback_started(self, tl_track):
        track = tl_track.track
        if self.check_uri_scheme(track.uri):
            return
        artists = self.concatenate_artist_names(track.artists)
        albumartists = self.concatenate_artist_names(track.album.artists)
        logger.info("Scrobbler : Album Artists are %s", albumartists)
        duration = track.length and track.length // 1000 or 0
        self.last_start_time = int(time.time())
        logger.debug('Now playing track: %s - %s', artists, track.name)
        try:
            self.lastfm.update_now_playing(
                artists,
                (track.name or ''),
                album=(track.album and track.album.name or ''),
                album_artist=albumartists,
                duration=str(duration),
                track_number=str(track.track_no or 0),
                mbid=(track.musicbrainz_id or ''))
        except PYLAST_ERRORS as e:
            logger.warning('Error submitting playing track to Last.fm: %s', e)

    def track_playback_ended(self, tl_track, time_position):
        track = tl_track.track
        if self.check_uri_scheme(track.uri):
            return
        artists = self.concatenate_artist_names(track.artists)
        albumartists = self.concatenate_artist_names(track.album.artists)
        duration = track.length and track.length // 1000 or 0
        time_position = time_position // 1000
        if duration < 30:
            logger.debug('Track too short to scrobble. (30s)')
            return
        if time_position < duration // 2 and time_position < 240:
            logger.debug(
                'Track not played long enough to scrobble. (50% or 240s)')
            return
        if self.last_start_time is None:
            self.last_start_time = int(time.time()) - duration
        logger.debug('Scrobbling track: %s - %s', artists, track.name)
        try:
            self.lastfm.scrobble(
                artists,
                (track.name or ''),
                str(self.last_start_time),
                album=(track.album and track.album.name or ''),
                album_artist=albumartists,
                track_number=str(track.track_no or 0),
                duration=str(duration),
                mbid=(track.musicbrainz_id or ''))
        except PYLAST_ERRORS as e:
            logger.warning('Error submitting played track to Last.fm: %s', e)
