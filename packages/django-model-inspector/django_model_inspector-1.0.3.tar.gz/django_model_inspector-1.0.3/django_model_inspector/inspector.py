import django
from django.apps import apps
from django.db import models
from django.db.migrations.executor import MigrationExecutor
from django.db import connection
from .sdk_settings import SDK_SETTINGS

DJANGO_BUILTIN_APPS = {'auth', 'admin', 'sessions', 'contenttypes', 'staticfiles', 'messages'}

class DjangoSchemaInspector:
    def __init__(self):
        """
        Initialize the SDK with configured settings from Django settings.
        """
        django.setup()

    def collect_schema(self):
        """
        Collects schema information of all models in the installed Django apps.
        :return: A dictionary containing schema information of each app and its models.
        """
        schema = {}

        for app_config in apps.get_app_configs():
            # Skip built-in Django apps if USER_DEFINED_ONLY is set to True
            if SDK_SETTINGS['USER_DEFINED_ONLY'] and app_config.label in DJANGO_BUILTIN_APPS:
                continue
            
            if SDK_SETTINGS['APP_LABELS'] and app_config.label not in SDK_SETTINGS['APP_LABELS']:
                continue  # Skip apps not in the APP_LABELS setting

            app_name = app_config.label
            schema[app_name] = self._collect_app_models(app_config)

        return schema

    def _collect_app_models(self, app_config):
        """
        Collects schema information for models in a given app.
        :param app_config: Django AppConfig object for an app.
        :return: A dictionary containing schema information of each model in the app.
        """
        models_schema = {}

        for model in app_config.get_models():
            models_schema[model.__name__] = self._collect_model_fields(model)

        return models_schema

    def _collect_model_fields(self, model):
        """
        Collects key metadata for each field in a given model, focusing on model name, reference type, and other attributes.
        :param model: Django model class.
        :return: A dictionary with field names and simplified metadata.
        """
        fields_info = {}

        for field in model._meta.get_fields():
            # Set callable defaults to None for JSON compatibility
            default_value = getattr(field, 'default', None)
            if callable(default_value):
                default_value = None  # Replace callable defaults with None

            field_info = {
                'type': type(field).__name__,
                'null': getattr(field, 'null', None),
                'blank': getattr(field, 'blank', None),
                'max_length': getattr(field, 'max_length', None),
                'default': default_value,
            }

            # Include relationship type and split related model into app and model attributes
            if isinstance(field, models.ForeignKey):
                field_info['relationship'] = 'ForeignKey'
                field_info['related_model'] = {
                    'app': field.related_model._meta.app_label,
                    'model': field.related_model.__name__
                }
                field_info['on_delete'] = field.remote_field.on_delete.__name__
            elif isinstance(field, models.OneToOneField):
                field_info['relationship'] = 'OneToOneField'
                field_info['related_model'] = {
                    'app': field.related_model._meta.app_label,
                    'model': field.related_model.__name__
                }
                field_info['on_delete'] = field.remote_field.on_delete.__name__
            elif isinstance(field, models.ManyToManyField):
                field_info['relationship'] = 'ManyToManyField'
                field_info['related_model'] = {
                    'app': field.related_model._meta.app_label,
                    'model': field.related_model.__name__
                }

            fields_info[field.name] = field_info

        return fields_info

    def _get_unapplied_migrations(self):
        """
        Returns a list of unapplied migrations if INCLUDE_UNAPPLIED_MIGRATIONS is enabled.
        :return: List of unapplied migrations or an empty list if no migrations exist.
        """
        try:
            executor = MigrationExecutor(connection)
            targets = executor.loader.graph.leaf_nodes()
            unapplied_migrations = executor.migration_plan(targets)
            return [{'app': migration[0], 'name': migration[1].name} for migration in unapplied_migrations]
        except (AttributeError, KeyError):
            # Return an empty list if there are no migrations or an error occurs
            return []
