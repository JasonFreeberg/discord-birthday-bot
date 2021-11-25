import os
import requests
import json
import datetime
from utils import Friend
from sys import argv


def main(friends_file_path: str):
    """
    Main entrypoint for the bot. Expects a file path to the location of the JSON file with the friends
    information
    """

    print('Runing application...')
    
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    CHANNEL_ID = os.environ.get('CHANNEL_ID')

    if BOT_TOKEN is None:
        raise ValueError('No env var found for BOT_TOKEN')
    if CHANNEL_ID is None:
        raise ValueError('No env var found for CHANNEL_ID')

    BOT_TOKEN = 'Bot '+BOT_TOKEN
    BASE_URL = 'https://discord.com/api/v9'
    TODAY = datetime.datetime.today()

    with open(friends_file_path) as json_file:
        birthday_data = json.load(json_file)

        if len(birthday_data['friends']) < 1: 
            raise ValueError('No friend objects found in the list of friends. There was likely a problem reading the file.')

        for friend_entry in birthday_data['friends']:
            friend = Friend.from_dict(friend_entry)

            if friend.days_until_birthday == int(birthday_data['reminder_in_days']):

                response = requests.post(
                    BASE_URL+'/channels/'+CHANNEL_ID+'/messages',
                    headers={
                        'Authorization': BOT_TOKEN,
                        'Content-Type': 'application/json'
                    },
                    data = json.dumps({
                        "content": friend.get_birthday_message()
                    })
                )

                if response.status_code >= 400:
                    print('There was a problem sending the birthday message to '+friend.name)
                    print(response.content)
                else:
                    print('Birthday reminder sent for '+friend.name)


if __name__ == '__main__':
  if len(argv) <= 1:
    raise ValueError("You must specify the location of the JSON file with your friends' data.")
  friends_file_path = argv[1]

  main(friends_file_path)
