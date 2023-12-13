import json

from django.http import HttpRequest


def parse_json_request(request: HttpRequest):
    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        return None
