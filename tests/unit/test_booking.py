import pytest
import booking


@pytest.mark.parametrize(
    "domain",
    [("gmail.com"), ("yahoo.com"), ("hotmail.com"), ("aol.com"), ("icloud.com")],
)
def test_sender_hostname(domain):
    test_email_address = f"jfgphillips@{domain}"
    pass
    # sender = booking.sender()
    # pass
