from unittest import mock

from mopidy_scrobbler import Extension
from mopidy_scrobbler import frontend as frontend_lib


def test_get_default_config() -> None:
    ext = Extension()

    config = ext.get_default_config()

    assert "[scrobbler]" in config
    assert "enabled = true" in config
    assert "username =" in config
    assert "password =" in config


def test_get_config_schema() -> None:
    ext = Extension()

    schema = ext.get_config_schema()

    assert "username" in schema
    assert "password" in schema


def test_setup() -> None:
    ext = Extension()
    registry = mock.Mock()

    ext.setup(registry)

    registry.add.assert_called_once_with("frontend", frontend_lib.ScrobblerFrontend)
