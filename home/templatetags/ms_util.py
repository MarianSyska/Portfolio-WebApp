import uuid
from typing import Any

from django import template

register = template.Library()

@register.filter(name="append")
def append_string(value: str, arg: Any) -> str:
    return "-".join([value, str(arg)])

@register.simple_tag(name="uuid")
def generate_uuid() -> str:
    return uuid.uuid4().hex
