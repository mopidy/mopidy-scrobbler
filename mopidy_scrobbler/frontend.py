from __future__ import unicode_literals

import logging
import time

import pykka
import pylast

from mopidy.core import CoreListener


logger = logging.getLogger(__name__)

API_KEY = '2236babefa8ebb3d93ea467560d00d04'
API_SECRET = '94d9a09c0cd5be955c4afaeaffcaefcd'


class ScrobblerFrontend(pykka.ThreadingActor, CoreListener):
    def __init__(self, config, core):
        super(ScrobblerFrontend, self).__init__()
        self.config = config
        self.lastfm = None
        self.last_start_time = None

    def on_start(self):
        try:
            self.lastfm = pylast.LastFMNetwork(
                api_key=API_KEY, api_secret=API_SECRET,
                username=self.config['scrobbler']['username'],
                password_hash=pylast.md5(self.config['scrobbler']['password']))
            logger.info('Scrobbler connected to Last.fm')
        except (pylast.NetworkError, pylast.MalformedResponseError,
                pylast.WSError) as e:
            logger.error('Error during Last.fm setup: %s', e)
            self.stop()

    def getDuration(self, track):
        return track.length and track.length // 1000 or 0

    def getArtists(self, track):
        ''' Return a tuple consisting of the first artist and a merged string of
        artists. The first artist is considered to be the primary artist of the
        track. The artists are joined by using slashes as recommended in
        ID3v2.3. '''
        if not len(track.artists):
            logger.error('The track does not have any artists.')
            raise ValueError
        artist = track.artists[0]
        artists =  '/'.join(sorted([a.name for a in track.artists]))
        return (artist, artists)

    def track_playback_started(self, tl_track):
        track = tl_track.track
        assert len(track.artists), logger.error('The track does not have any artists.')
        (artist, artists) = self.getArtists(track)
        duration = self.getDuration(track)
        self.last_start_time = int(time.time())
        logger.debug('Now playing track: %s - %s', artists, track.name)
        try:
            self.lastfm.update_now_playing(
                artist,
                (track.name or ''),
                album=(track.album and track.album.name or ''),
                duration=str(duration),
                track_number=str(track.track_no or 0),
                mbid=(track.musicbrainz_id or ''))
        except (pylast.ScrobblingError, pylast.NetworkError,
                pylast.MalformedResponseError, pylast.WSError) as e:
            logger.warning('Error submitting playing track to Last.fm: %s', e)

    def track_playback_ended(self, tl_track, time_position):
        ''' Scrobble the current track but only submit the primary artist
        instead of a combined string which could wrongfully create new
        Last.FM artist pages. '''
        track = tl_track.track
        (artist, artists) = self.getArtists(track)
        duration = self.getDuration(track)
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
                artist,
                (track.name or ''),
                str(self.last_start_time),
                album=(track.album and track.album.name or ''),
                track_number=str(track.track_no or 0),
                duration=str(duration),
                mbid=(track.musicbrainz_id or ''))
        except (pylast.ScrobblingError, pylast.NetworkError,
                pylast.MalformedResponseError, pylast.WSError) as e:
            logger.warning('Error submitting played track to Last.fm: %s', e)
