
import datetime 
import random
from num2words import num2words


class Friend():
  name = ''
  birthdate = None
  birthdate = None
  TODAY = None
  date_format = ''
  gift_ideas = []

  def __init__(self, name: str, birthdate: str, gift_ideas: list, date_format='%Y-%m-%d'):
    self.TODAY = datetime.datetime.today()
    self.name = name
    self.birthdate = datetime.datetime.strptime(birthdate, date_format)
    self.birthday = datetime.datetime(self.TODAY.year, self.birthdate.month, self.birthdate.day)
    self.gift_ideas = gift_ideas
  
  @classmethod
  def from_dict(cls, friend: dict):
    return cls(friend['name'], friend['birthdate'], friend['gift_ideas'])

  @property
  def days_until_birthday(self):
    return (self.birthday - self.TODAY).days

  def get_birthday_message(self):
    formatted_birthday = self.birthdate.strftime('%B %d')
    new_age = int((self.TODAY - self.birthdate).days / 365)

    gift = random.choice(self.gift_ideas)

    if self.days_until_birthday % 7 == 0:
      num = num2words(int(self.days_until_birthday/7))
      time_until_birthday = f'{num} weeks'
    else:
      time_until_birthday = str(int(self.days_until_birthday))+' days'

    return f'{self.name} is turning {new_age} in {time_until_birthday} on {formatted_birthday}. Maybe we should get him {gift}?'


def create_message(name: str, birthdate: datetime.datetime):
    formatted_birthday = birthdate.strftime('%B %d')
    new_age = int((datetime.datetime.today() - birthdate).days / 365)

    return f'{name} is turning {new_age} in two weeks on {formatted_birthday}.'