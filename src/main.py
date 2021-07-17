import os
from utils import create_message
import requests
import json
import datetime
from .utils import Friend

'''
- How to break this up so it's more testable
- Can I use more declarative, map-style programming here over the list of friends?

'''

if __name__ == '__main__':
    print('Runing application.')
    
    BOT_TOKEN = 'Bot '+os.environ.get('BOT_TOKEN')
    CHANNEL_ID = os.environ.get('SERVER_ID')
    BASE_URL = 'https://discord.com/api/v9'
    TODAY = datetime.datetime.today()

    with open('birthdays.json') as json_file:
        birthday_data = json.load(json_file)

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
                    print('There was a problem sending the birthday message to '+friend['name'])
                    print(response.content)
                else:
                    print('Birthday reminder sent for '+friend['name'])


