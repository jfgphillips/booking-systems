from unittest import mock

import pytest

from utils.customer import Customer
from utils import parsers


@pytest.mark.parametrize("user_input", [("string"), ("11"), (None)])
def test_string_input_parser(user_input, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: user_input)
    result = parsers.string_input_parser("test prompt")
    assert result == user_input


@pytest.mark.parametrize("user_input, expected_result", [("10", 10), ("010", 10), ("-1", -1)])
def test_integer_input_parser(user_input, expected_result, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: user_input)
    result = parsers.integer_input_parser("test prompt")
    assert result == expected_result


def test_string_input_parser_with_validator(monkeypatch):
    user_input = "1234@gmail.com"
    monkeypatch.setattr("builtins.input", lambda _: user_input)
    result = parsers.string_input_parser(user_input, Customer.validate_customer_email)
    assert result == user_input


def test_string_input_parser_with_validator_failed():
    valid_input = "1234@gmail.com"
    with mock.patch("builtins.input", side_effect=["invlaid_email", valid_input]) as mocked_input:
        result = parsers.string_input_parser("input email", Customer.validate_customer_email)
        assert result == valid_input
        assert mocked_input.call_count == 2
