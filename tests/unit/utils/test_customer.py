from unittest import mock
from unittest.mock import call

import pytest

from utils.customer import Customer


@pytest.mark.parametrize("email", [("john@gmail.com"), ("john@hotmail.co.uk"), ("john@outlook.com")])
def test_customer(email):
    """Test that `Customer` is instantiated with expected attributes for 3 valid emails"""
    name = "John"
    address = "70 Bristol Ln"
    actual_customer = Customer(email=email, name=name, address=address)
    assert actual_customer.email == email
    assert actual_customer.name == name
    assert actual_customer.address == address
    assert len(actual_customer.items) == 0


@pytest.mark.parametrize(
    "email",
    [("john.gmail.com"), ("john@hotmail"), ("@outlook.com")],
    ids=["no domain classifier", "no web address", "no username"],
)
def test_customer_raises_invalid_email(email):
    """test that invalid emails raise `ValueError`"""
    name = "John"
    address = "70 Bristol Ln"
    with pytest.raises(ValueError):
        Customer(email=email, name=name, address=address)


@pytest.mark.parametrize(
    "name, address", [(1, "Valid Address"), ("valid name", 1)], ids=["Invalid name", "Invalid address"]
)
def test_customer_raises_invalid_name_address(name, address):
    email = "john@gmail.com"
    with pytest.raises(ValueError):
        Customer(email=email, name=name, address=address)


def test_customer_from_cli_input():
    name = "John"
    email = "1234@gmail.com"
    address = "70 Long Avenue"
    with mock.patch("builtins.input") as mocked_input:
        mocked_input.side_effect = [email, name, address]
        customer = Customer.from_cli_input()
        assert customer.email == email
        assert customer.name == name
        assert customer.address == address
        assert len(customer.items) == 0


def test_customer_from_cli_input_with_mistake():
    """
    This test checks that when the user passes a wrong email the user is prompted for an email again before proceeding
    Checks:
        a. `Customer` initialised with correct attributes
        b. email validator is called 3 times within the scope of the test (ignoring `expected_customer`)
            1. with invalid "1234.gmail.com"
            2. with valid "1234@gmail.com"
            3. during instantiation of `Customer`
        c. input call args are as expected 2x request for email, 1x request for name and 1x request for address
    """
    name = "John"
    email_mistake = "1234.gmail.com"
    email = "1234@gmail.com"
    address = "70 Long Avenue"
    expected_customer = Customer(name=name, email=email, address=address)
    with mock.patch("builtins.input") as mocked_input:
        with mock.patch.object(
            Customer, "validate_customer_email", wraps=Customer.validate_customer_email
        ) as mocked_customer_validator:
            mocked_input.side_effect = [email_mistake, email, name, address]
            actual_customer = Customer.from_cli_input()
            assert actual_customer == expected_customer
            assert mocked_customer_validator.call_count == 3
            assert mocked_input.call_args_list == [
                call("input email: "),
                call("input email: "),
                call("input name: "),
                call("input address: "),
            ]
