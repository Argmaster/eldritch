from pluggy import PluginManager

from ._mixins import SingletonMixin


class EldritchPluginManager(SingletonMixin):
    def load_plugins() -> None:
        plugin_manager = PluginManager("eldritch")
