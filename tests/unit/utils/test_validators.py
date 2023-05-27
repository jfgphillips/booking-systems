import pytest
from utils import parsers


@pytest.mark.parametrize("user_input", [("string"), ("11"), (None)])
def test_string_input_parser(user_input, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: user_input)
    result = parsers.string_input_parser("test prompt")
    assert result == user_input


@pytest.mark.parametrize("user_input, expected_result", [("10", 10), ("010", 10), ("-1", -1)])
def test_integer_input_parser(user_input, expected_result, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: user_input)
    result = parsers.integer_input_parser("test prompt")
    assert result == expected_result
