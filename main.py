import os
from utils import create_message
import requests
import json
import datetime

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

        for friend in birthday_data['friends']:
            birthdate = datetime.datetime.strptime(friend['birthday'], birthday_data['date_format'])
            birthday = datetime.datetime(TODAY.year, birthdate.month, birthdate.day)
            
            days_until_birthday = (birthday - TODAY)

            if days_until_birthday.days == int(birthday_data['reminder_in_days']):

                response = requests.post(
                    BASE_URL+'/channels/'+CHANNEL_ID+'/messages',
                    headers={
                        'Authorization': BOT_TOKEN,
                        'Content-Type': 'application/json'
                    },
                    data = json.dumps({
                        "content": create_message(friend['name'], birthdate)
                    })
                )

                if response.status_code >= 400:
                    print('There was a problem sending the birthday message to '+friend['name'])
                    print(response.content)
                else:
                    print('Birthday reminder sent for '+friend['name'])


