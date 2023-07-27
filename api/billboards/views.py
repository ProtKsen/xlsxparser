import json

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


@method_decorator(csrf_exempt)
@require_http_methods(["POST"])
def add(request):
    pass
