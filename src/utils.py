
import datetime 
import random
from num2words import num2words
import requests
import json


class Friend():
  """
  A class representing a friend object from birthdays.json, with associated data and utility methods.
  """
  
  name = ''
  birthdate = None
  birthdate = None
  TODAY = None
  date_format = ''
  gift_ideas = []

  def __init__(self, name: str, birthdate: str, gift_ideas: list, date_format='%Y-%m-%d'):
    self.TODAY = datetime.date.today()
    self.name = name
    self.birthdate = datetime.datetime.strptime(birthdate, date_format).date()
    self.birthday = datetime.date(self.TODAY.year, self.birthdate.month, self.birthdate.day)
    self.gift_ideas = gift_ideas
  
  @classmethod
  def from_dict(cls, friend: dict):
    """
    Alternative constructor to instantiate the class from a dictionary. 
    """
    return cls(friend['name'], friend['birthdate'], friend['gift_ideas'])

  @property
  def days_until_birthday(self):
    """
    The number of days between now and the friend's birthday. Does not take time (hours/minutes) into account, only the dates.
    """
    return (self.birthday - self.TODAY).days

  def get_birthday_message(self):
    """
    Returns the formatted reminder message for posting on Discord channel. 
    """
    formatted_birthday = self.birthdate.strftime('%B %d')
    new_age = int((self.TODAY - self.birthdate).days / 365)

    gift = random.choice(self.gift_ideas)

    if self.days_until_birthday % 7 == 0:
      num = num2words(int(self.days_until_birthday/7))
      time_until_birthday = f'{num} weeks'
    else:
      num = num2words(int(self.days_until_birthday))
      time_until_birthday = f'{num} days'

    return f'{self.name} is turning {new_age} in {time_until_birthday} on {formatted_birthday}. Maybe we should get him {gift}?'


def read_json_file(file_path: str) -> list:
  """
  Reads friends JSON file from URL or file path.
  """
  if file_path[0:4] == 'http':
    response = requests.get(file_path)
    birthday_data = response.json()
  else:
    with open(file_path) as json_file:
      birthday_data = json.load(json_file)

  return birthday_data
