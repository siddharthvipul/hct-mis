"""
Settings for Steficon namespaced in the STEFICON setting.
For example your project's `settings.py` file might look like this:
STEFICON = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
}
This module provides the `api_setting` object, that is used to access
REST framework settings, checking for user settings first, then falling
back to the defaults.
"""
from django.conf import settings
from django.core.signals import setting_changed

DEFAULTS = {
    "USE_BLACK": False,
    "BUILTIN_MODULES": ["random", "datetime", "dateutil"],
}


class Config:
    def __init__(self, user_settings=None, defaults=None):
        if user_settings:
            self._user_settings = user_settings
        self.defaults = defaults or DEFAULTS
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, "_user_settings"):
            self._user_settings = getattr(settings, "STEFICON", {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid STEFICON setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Cache the result
        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if hasattr(self, "_user_settings"):
            delattr(self, "_user_settings")


config = Config(None, DEFAULTS)


def reload_config(*args, **kwargs):
    setting = kwargs["setting"]
    if setting == "STEFICON":
        config.reload()


setting_changed.connect(reload_config)