
# Django Schema Inspector

**Django Schema Inspector** is a utility designed to inspect and expose metadata about Django models in a structured format. It provides a simple, configurable way to retrieve schema information for models across Django applications, with optional filtering by user-defined settings.

## Features

- **Schema Collection**: Gathers metadata for all Django models, including field types, relationships, and defaults.
- **Configurable Filtering**: Optionally exclude built-in Django apps, private fields, or specific fields.
- **JSON Output**: Exposes schema data via a Django view for easy JSON retrieval.

## Installation

Install Django Schema Inspector via pip:

```bash
pip install django-schema-collector
```

## Configuration

In your Django `settings.py`, add optional settings prefixed with `DMI_` to customize the behavior of the schema collector. Available settings:

- **`DMI_INCLUDE_PRIVATE_FIELDS`**: Set to `True` to include private fields in the schema output. Default is `False`.
- **`DMI_INCLUDE_METHODS`**: Set to `True` to include model methods in the schema output. Default is `False`.
- **`DMI_EXCLUDE_FIELDS`**: A list of field names to exclude from the output. Default is an empty list (`[]`).
- **`DMI_APP_LABELS`**: A list of specific app labels to include in the schema output. Default is `None`, which includes all apps.
- **`DMI_USER_DEFINED_ONLY`**: Set to `True` to exclude built-in Django apps from the output. Default is `False`.

Example configuration:

```python
# settings.py
DMI_INCLUDE_PRIVATE_FIELDS = False
DMI_INCLUDE_METHODS = False
DMI_EXCLUDE_FIELDS = ['password', 'email']
DMI_APP_LABELS = ['myapp', 'another_app']
DMI_USER_DEFINED_ONLY = True
```

## Usage

### 1. Schema Collection

The main component of this SDK is the `DjangoSchemaInspector` class, which provides methods to collect schema metadata.

```python
from dmi.inspector import DjangoSchemaInspector

# Initialize the collector
collector = DjangoSchemaInspector()

# Collect schema information
schema = collector.collect_schema()
print(schema)
```

### 2. Exposing Schema as JSON

If you want to expose your schema in a endpoint, create a url path in urls.py and map the view. Or, you can import a pre-defined `SchemaView` and map to a specific path

```python
# urls.py
from django.urls import path
from dmi.views import SchemaView

urlpatterns = [
    path('api/schema/', SchemaView.as_view(), name='schema-view'),
]
```

Accessing `/api/schema/` will return a JSON representation of the schema.

## Example Response

A sample JSON response from `/api/schema/` endpoint might look like:

```json
{
  "myapp": {
    "MyModel": {
      "id": {"type": "AutoField", "null": false, "blank": false, "max_length": null, "default": null},
      "name": {"type": "CharField", "null": false, "blank": false, "max_length": 255, "default": ""},
      "created_at": {"type": "DateTimeField", "null": true, "blank": true, "max_length": null, "default": null},
      "related_model": {
        "type": "ForeignKey",
        "relationship": "ForeignKey",
        "related_model": {"app": "related_app", "model": "RelatedModel"},
        "on_delete": "CASCADE"
      }
    }
  }
}
```

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for suggestions or feature requests.

## Contact

For any issues, please open an issue on [GitHub](https://github.com/mowzlisre/django-schema-collector) or contact [speak2mowzli@gmail.com](mailto:speak2mowzli@gmail.com).

---

Happy coding!
