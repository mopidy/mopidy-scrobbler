import unittest

from mopidy_scrobbler import Extension, frontend as frontend_lib


class ExtensionTest(unittest.TestCase):

    def test_get_default_config(self):
        ext = Extension()

        config = ext.get_default_config()

        self.assertIn('[scrobbler]', config)
        self.assertIn('enabled = true', config)
        self.assertIn('username =', config)
        self.assertIn('password =', config)

    def test_get_config_schema(self):
        ext = Extension()

        schema = ext.get_config_schema()

        self.assertIn('username', schema)
        self.assertIn('password', schema)

    def test_get_frontend_classes(self):
        ext = Extension()

        classes = ext.get_frontend_classes()

        self.assertIn(frontend_lib.ScrobblerFrontend, classes)
