import unittest

import mock

from mopidy_scrobbler import Extension, frontend as frontend_lib


class ExtensionTest(unittest.TestCase):

    def test_get_default_config(self):
        ext = Extension()

        config = ext.get_default_config()

        self.assertIn('[scrobbler]', config)
        self.assertIn('enabled = true', config)
        self.assertIn('lastfm_username =', config)
        self.assertIn('lastfm_password =', config)
        self.assertIn('librefm_username =', config)
        self.assertIn('librefm_password =', config)

    def test_get_config_schema(self):
        ext = Extension()

        schema = ext.get_config_schema()

        self.assertIn('lastfm_username', schema)
        self.assertIn('lastfm_password', schema)
        self.assertIn('librefm_username', schema)
        self.assertIn('librefm_password', schema)

    def test_setup(self):
        ext = Extension()
        registry = mock.Mock()

        ext.setup(registry)

        registry.add.assert_called_once_with(
            'frontend', frontend_lib.ScrobblerFrontend)

if __name__ == '__main__':
    unittest.main()
