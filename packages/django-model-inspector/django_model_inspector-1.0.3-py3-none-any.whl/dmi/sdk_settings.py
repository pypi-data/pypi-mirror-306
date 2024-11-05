from django.conf import settings

# Default settings for the SDK
DEFAULT_SETTINGS = {
    'INCLUDE_PRIVATE_FIELDS': False,
    'INCLUDE_METHODS': False,
    'EXCLUDE_FIELDS': [],
    'APP_LABELS': None,
    'USER_DEFINED_ONLY': False,  # New setting to include only user-defined models
}

# Load settings from Django's settings.py if defined, otherwise use defaults
SDK_SETTINGS = {
    key: getattr(settings, f'DMI_{key}', default)
    for key, default in DEFAULT_SETTINGS.items()
}
