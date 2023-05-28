import pytest

from utils.customer import Customer


@pytest.mark.parametrize("email", [("john@gmail.com"), ("john@hotmail.co.uk"), ("john@outlook.com")])
def test_customer(email):
    name = "John"
    address = "70 Bristol Ln"
    actual_customer = Customer(email=email, name=name, address=address)
    assert actual_customer.email == email
    assert actual_customer.name == name
    assert actual_customer.address == address
    assert len(actual_customer.items) == 0


@pytest.mark.parametrize("email", [("john.gmail.com"), ("john@hotmail"), ("@outlook.com")])
def test_customer_raises_invalid_email(email):
    name = "John"
    address = "70 Bristol Ln"
    with pytest.raises(ValueError):
        Customer(email=email, name=name, address=address)
