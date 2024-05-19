import pytest
from booking import BookingSystem
from utils.customer import Customer


@pytest.fixture(scope="function")
def booking_system_fixture(mocked_customer):
    menucard = [
        {"Items": "Fish and Chips", "Price": 10},
        {"Items": "Potato", "Price": 8},
        {"Items": "Bhaji", "Price": 5},
    ]
    booking_system = BookingSystem(menu=menucard, customer=mocked_customer)
    return booking_system


@pytest.fixture(scope="function")
def mocked_customer():
    return Customer(name="John", email="1234@gmail.com", address="70 Rd Drive")
