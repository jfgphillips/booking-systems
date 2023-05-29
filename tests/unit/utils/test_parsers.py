import builtins
from unittest import mock

import pytest

from utils.customer import Customer
from utils import parsers


@pytest.mark.parametrize("user_input", [("string"), ("11"), (None)])
def test_string_input_parser(
    user_input,
):
    with mock.patch.object(builtins, "input", return_value=user_input):
        result = parsers.string_input_parser("test prompt")
        assert result == user_input


@pytest.mark.parametrize("user_input, expected_result", [("10", 10), ("010", 10), ("-1", -1)])
def test_integer_input_parser(user_input, expected_result, monkeypatch):
    with mock.patch.object(builtins, "input", return_value=user_input):
        result = parsers.integer_input_parser("test prompt")
        assert result == expected_result


def test_input_parser_with_validator():
    user_input = "1234@gmail.com"
    with mock.patch.object(builtins, "input", return_value=user_input):
        result = parsers.string_input_parser(user_input, Customer.validate_customer_email)
        assert result == user_input


def test_input_parser_with_validator_failed():
    valid_input = "1234@gmail.com"
    with mock.patch.object(builtins, "input", side_effect=["invlaid_email", valid_input]) as mocked_input:
        result = parsers.string_input_parser("input email", Customer.validate_customer_email)
        assert result == valid_input
        assert mocked_input.call_count == 2


@pytest.mark.parametrize(
    "parser, input_response, expected_response",
    [(parsers.string_input_parser, "string", "string"), (parsers.integer_input_parser, "1", 1)],
)
def test_input_parser_handles_value_error(parser, input_response, expected_response):
    with mock.patch.object(builtins, "input", side_effect=[ValueError, input_response]):
        actual_response = parser("enter choice: ")
        assert actual_response == expected_response


@pytest.mark.parametrize("parser", [parsers.string_input_parser, parsers.integer_input_parser])
def test_input_keyboard_interrupt(parser):
    """test that keyboard interrupt followed by q exits the program"""
    with mock.patch.object(builtins, "input", side_effect=[KeyboardInterrupt, "q"]):
        with pytest.raises(SystemExit):
            parser("enter choice: ")


@pytest.mark.parametrize(
    "parser, input_response, expected_response",
    [(parsers.string_input_parser, "string", "string"), (parsers.integer_input_parser, "1", 1)],
)
def test_input_keyboard_interrupt_continue(parser, input_response, expected_response):
    """test that keyboard interrupt followed by c allows user to continue as normal"""
    with mock.patch.object(builtins, "input", side_effect=[KeyboardInterrupt, "c", input_response]):
        actual_response = parser("enter choice: ")
        assert actual_response == expected_response
