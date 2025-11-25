import pathlib
from importlib.metadata import version

from mopidy import config, ext

__version__ = version("mopidy-scrobbler")


class Extension(ext.Extension):
    dist_name = "mopidy-scrobbler"
    ext_name = "scrobbler"
    version = __version__

    def get_default_config(self):
        return config.read(pathlib.Path(__file__).parent / "ext.conf")

    def get_config_schema(self):
        schema = super().get_config_schema()
        schema["username"] = config.String()
        schema["password"] = config.Secret()
        return schema

    def setup(self, registry) -> None:
        from .frontend import ScrobblerFrontend  # noqa: PLC0415

        registry.add("frontend", ScrobblerFrontend)
