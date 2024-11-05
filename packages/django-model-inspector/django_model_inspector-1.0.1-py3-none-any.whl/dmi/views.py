from django.http import JsonResponse
from django.views import View
from .inspector import DjangoSchemaCollector

class SchemaView(View):
    """
    Django View to expose schema information as JSON without using DRF.
    """

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to return the schema in JSON format.
        """
        collector = DjangoSchemaCollector()
        schema = collector.collect_schema()
        return JsonResponse(schema, safe=False)
