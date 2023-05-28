from utils import utils


def test_gen_otp():
    result = utils.gen_otp()
    assert isinstance(result, str)
    assert len(result) == 6
