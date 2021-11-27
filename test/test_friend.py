
from src.utils import Friend
from freezegun import freeze_time

name = 'John Smith'
birthday = '1995-07-15'
gift_ideas = ['an Xbox', 'something nice']

FROZEN_TIME = '2021-07-01'

def test_constructor():

  with freeze_time('2021-07-01'):
    friend = Friend(name, birthday, gift_ideas)

    assert friend.name == name
    assert friend.birthday.year == 2021
    assert friend.birthdate.year == 1995
    assert friend.birthday.month == 7
    assert friend.birthday.day == 15
    assert friend.gift_ideas == gift_ideas


def test_get_birthday_message(): 
  
  with freeze_time(FROZEN_TIME):
    friend = Friend(name, birthday, gift_ideas)

    # The gift ideas are randomly selected, so we create a list of all the possible expected messages
    expected_messages = [] 
    for gift in gift_ideas:
      expected_messages.append(f'{name} is turning 25 in two weeks on July 15. Maybe we should get him {gift}?')

    assert friend.get_birthday_message() in expected_messages

def test_days_until_birthday():

  with freeze_time(FROZEN_TIME):
    friend = Friend(name, birthday, gift_ideas)

    assert friend.days_until_birthday == 14
  
  # Test half day
  with freeze_time(FROZEN_TIME+' 12:30:30'):
    friend = Friend(name, birthday, gift_ideas)

    assert friend.days_until_birthday == 14  