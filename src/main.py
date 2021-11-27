import os
import requests
import json
import datetime
from utils import Friend, read_json_file
from sys import argv


def main(friends_file_path: str):
    """
    Main entrypoint for the bot. Expects a file path to the location of the JSON file with the friends
    information
    """

    print('Starting bot...')
    
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    CHANNEL_ID = os.environ.get('CHANNEL_ID')

    if BOT_TOKEN is None:
        raise ValueError('No env var found for BOT_TOKEN')
    if CHANNEL_ID is None:
        raise ValueError('No env var found for CHANNEL_ID')

    BOT_TOKEN = 'Bot '+BOT_TOKEN
    BASE_URL = 'https://discord.com/api/v9'
    
    birthday_data = read_json_file(friends_file_path)

    if len(birthday_data['friends']) < 1: 
        raise ValueError('No friend objects found in the list of friends. There was likely a problem reading the file.')
    
    print(f"Data found for {len(birthday_data['friends'])} friends.")
    print(f"Sending {', '.join(birthday_data['reminders_in_days'])} day reminders ")

    successful_send_count = 0
    failed_send_count = 0
    for friend_entry in birthday_data['friends']:
        friend = Friend.from_dict(friend_entry)
        print(f"{friend.name}'s birthday is in {friend.days_until_birthday} days.")
        
        for reminder in birthday_data['reminders_in_days']:
            if friend.days_until_birthday == int(reminder):

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
                    print(f'\tThere was a problem sending the birthday reminder for {friend.name}.')
                    print(response.content)
                    failed_send_count += 1
                else:
                    print(f'\tBirthday reminder sent for {friend.name}.')
                    successful_send_count += 1

    print('Bot run completed. Summary:')
    print(f'\tTotal reminders sent: {successful_send_count+failed_send_count}')
    print(f'\tReminders successfully sent: {successful_send_count}')
    print(f'\tReminders which failed to send: {failed_send_count}')

    return dict(
        successful_send_count = successful_send_count,
        failed_send_count = failed_send_count,
        total_send_count = successful_send_count+failed_send_count
    )

if __name__ == '__main__':
  if len(argv) <= 1:
    raise ValueError("You must specify the location of the JSON file with your friends' data.")
  friends_file_path = argv[1]

  main(friends_file_path)
