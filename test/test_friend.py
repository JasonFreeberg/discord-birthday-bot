
from src.utils import Friend
from freezegun import freeze_time


def test_constructor():

  with freeze_time("2021-07-01"):
    friend = Friend('John Smith', '1995-07-01', [])

    assert friend.days_until_birthday == 0