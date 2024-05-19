import pytest
from booking import BookingSystem


@pytest.mark.parametrize(
    "menucard",
    [
        ([{"Items": "Fish and Chips", "Price": 10}, {"Items": "Potato", "Price": 8}, {"Items": "Bhaji", "Price": 5}]),
        (
            [
                {"Items": "Fish and Chips", "Price": 10},
                {"Items": "Potato", "Price": 8},
            ]
        ),
    ],
)
def test_booking_system_show_menucard(menucard):
    booking_system = BookingSystem(menu=menucard)
    print(booking_system.showMenucard())
