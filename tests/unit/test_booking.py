import pytest
import booking


@pytest.mark.parametrize("domain", [("gmail.com"), ("yahoo.com"), ("hotmail.com"), ("aol.com"), ("icloud.com")])
def test_sender_hostnm(domain):
    test_email_address = f"jfgphillips@{domain}"
    sender = booking.sender()
    pass
