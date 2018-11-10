from __future__ import unicode_literals

import os

from mopidy import config, ext


__version__ = '1.2.0'


class Extension(ext.Extension):

    dist_name = 'Mopidy-Scrobbler'
    ext_name = 'scrobbler'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['username'] = config.String()
        schema['password'] = config.Secret()
        schema['scrobble_filter'] = config.List(optional=True)
        return schema

    def setup(self, registry):
        from .frontend import ScrobblerFrontend
        registry.add('frontend', ScrobblerFrontend)
