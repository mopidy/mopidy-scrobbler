#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

import logging
import os
import time

from mopidy.core import CoreListener

import pykka

import pylast

logger = logging.getLogger(__name__)

LASTFM_API_KEY = '2236babefa8ebb3d93ea467560d00d04'
LASTFM_API_SECRET = '94d9a09c0cd5be955c4afaeaffcaefcd'
LIBREFM_SESSION_KEY_FILE = os.path.join(os.path.expanduser('~'),
                                        '.librefm_session_key')


class ScrobblerFrontend(pykka.ThreadingActor, CoreListener):
    def __init__(self, config, core):
        super(ScrobblerFrontend, self).__init__()
        self.config = config
        self.lastfm = None
        self.librefm = None
        self.networks = {}
        self.last_start_time = None

    def on_start(self):
        if not (self.connect_to_lastfm() and self.connect_to_librefm()):
            logger.warning("Couldn't connect to any scrobbling services. "
                           "Mopidy Scrobbler will stop.")
            self.stop()

    def connect_to_lastfm(self):
        ''' Connect to Last.fm and return True on success. '''
        lastfm_username = self.config['scrobbler']['lastfm_username']
        lastfm_password = self.config['scrobbler']['lastfm_password']

        try:
            if lastfm_username and lastfm_password:
                self.lastfm = pylast.LastFMNetwork(
                    api_key=LASTFM_API_KEY,
                    api_secret=LASTFM_API_SECRET,
                    username=lastfm_username,
                    password_hash=pylast.md5(lastfm_password))
                logger.info('Scrobbler connected to Last.fm')
                self.networks['Last.fm'] = self.lastfm
                return True
        except (pylast.NetworkError, pylast.MalformedResponseError,
                pylast.WSError) as e:
            logger.error('Error while connecting to Last.fm: %s', e)

        return False

    def connect_to_librefm(self):
        ''' Connect to Libre.fm and return True on success. '''
        librefm_username = self.config['scrobbler']['librefm_username']
        librefm_password = self.config['scrobbler']['librefm_password']

        try:
            if librefm_username and librefm_password:
                self.librefm = pylast.LibreFMNetwork(
                    username=librefm_username,
                    password_hash=pylast.md5(librefm_password))

                if self.retrieve_librefm_session():
                    self.networks['Libre.fm'] = self.librefm
                    logger.info('Scrobbler connected to Libre.fm')
                    return True
                else:
                    return False
        except (pylast.NetworkError, pylast.MalformedResponseError,
                pylast.WSError) as e:
            logger.error('Error while connecting to Libre.fm: %s', e)

        return False

    def retrieve_librefm_session(self):
        ''' Opens a Web browser to create a session key file if none
        exists yet. Else, it is loaded from disk. Returns True on
        success. '''
        if not os.path.exists(LIBREFM_SESSION_KEY_FILE):
            import webbrowser
            logger.warning('The Libre.fm session key does not exist. A Web '
                           'browser will open an authentication URL. Confirm '
                           'access using your username and password. This '
                           'has to be done only once.')

            session_keygen = pylast.SessionKeyGenerator(self.librefm)
            auth_url = session_keygen.get_web_auth_url()
            webbrowser.open(auth_url)
            logger.info('A Web browser may not be opened if you run Mopidy '
                        'as a different user. In this case, you will have '
                        'to manually open the link "{url}".'
                        .format(url=auth_url))

            remainingTime = 30  # approximately 30 seconds before timeout
            while remainingTime:
                try:
                    session_key = session_keygen \
                                    .get_web_auth_session_key(auth_url)
                    # if the file was created in the meantime, it will
                    # be blindly overwritten:
                    with open(LIBREFM_SESSION_KEY_FILE, 'w') as f:
                        f.write(session_key)
                    logger.debug('Libre.fm session key retrieved and written '
                                 'to disk.')
                    break
                except pylast.WSError:
                    remainingTime -= 1
                    time.sleep(1)
                except IOError:
                    logger.error('Cannot write to session key file "{path}"'
                                 .format(path=LIBREFM_SESSION_KEY_FILE))
                    return False
            if not remainingTime:
                logger.error('Authenticating to Libre.fm timed out. Did you '
                             'allow access in your Web browser?')
                return False
        else:
            session_key = open(LIBREFM_SESSION_KEY_FILE).read()

        self.librefm.session_key = session_key
        return True

    def get_duration(self, track):
        return track.length and track.length // 1000 or 0

    def get_artists(self, track):
        ''' Return a tuple consisting of the first artist and a merged
        string of artists. The first artist is considered to be the
        primary artist of the track. The artists are joined by using
        slashes as recommended in ID3v2.3. Prefer the album artist if
        any is given. '''
        if not len(track.artists):
            logger.error('The track does not have any artists.')
            raise ValueError
        artists = [a.name for a in track.artists]
        if track.album and track.album.artists:
            artists = [a.name for a in track.album.artists]

            metaArtists = ['compilation', 'split', 'various artists']
            if artists[0].lower() in metaArtists:
                artists = [a.name for a in track.artists]
        primaryArtist = artists[0]
        artists = '/'.join(artists)
        return (primaryArtist, artists)

    def track_playback_started(self, tl_track):
        track = tl_track.track
        (artist, artists) = self.get_artists(track)
        duration = self.get_duration(track)
        self.last_start_time = int(time.time())
        logger.debug('Now playing track: %s - %s', artists, track.name)

        for network in self.networks.items():
            try:
                network[1].update_now_playing(
                    artist=artist,
                    title=(track.name or ''),
                    album=(track.album and track.album.name or ''),
                    duration=str(duration),
                    track_number=str(track.track_no or 0),
                    mbid=(track.musicbrainz_id or ''))
            except (pylast.ScrobblingError, pylast.NetworkError,
                    pylast.MalformedResponseError, pylast.WSError) as e:
                logger.warning('Error submitting playing track to {network}: '
                               '{error}'.format(network=network[0], error=e))

    def track_playback_ended(self, tl_track, time_position):
        ''' Scrobble the current track but only submit the primary
        artist instead of a combined string which could wrongfully
        create new Last.FM artist pages. '''
        track = tl_track.track
        (artist, artists) = self.get_artists(track)
        duration = self.get_duration(track)
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
        for network in self.networks.items():
            try:
                network[1].scrobble(
                    artist=artist,
                    title=(track.name or ''),
                    timestamp=str(self.last_start_time),
                    album=(track.album and track.album.name or ''),
                    track_number=str(track.track_no or 0),
                    duration=str(duration),
                    mbid=(track.musicbrainz_id or ''))
            except (pylast.ScrobblingError, pylast.NetworkError,
                    pylast.MalformedResponseError, pylast.WSError) as e:
                logger.warning('Error submitting played track to {network}: '
                               '{error}'.format(network=network[0], error=e))
