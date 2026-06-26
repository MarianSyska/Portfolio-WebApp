import re

import pytest
from django.template import Context, Template


class TestAppendFilter:
    def test_joins_with_hyphen(self):
        template = Template("{% load ms_util %}{{ value|append:arg }}")
        result = template.render(Context({"value": "hello", "arg": "world"}))
        assert result == "hello-world"

    def test_handles_non_string_arg(self):
        template = Template("{% load ms_util %}{{ value|append:arg }}")
        result = template.render(Context({"value": "count", "arg": 42}))
        assert result == "count-42"

    def test_empty_value(self):
        template = Template("{% load ms_util %}{{ value|append:arg }}")
        result = template.render(Context({"value": "", "arg": "suffix"}))
        assert result == "-suffix"


class TestUuidTag:
    def test_returns_32_hex_chars(self):
        template = Template("{% load ms_util %}{% uuid %}")
        result = template.render(Context({}))
        assert len(result) == 32
        assert re.match(r"^[0-9a-f]{32}$", result)

    def test_unique_on_each_call(self):
        template = Template("{% load ms_util %}{% uuid %}-{% uuid %}")
        result = template.render(Context({}))
        parts = result.split("-")
        assert len(parts) == 2
        assert parts[0] != parts[1]
