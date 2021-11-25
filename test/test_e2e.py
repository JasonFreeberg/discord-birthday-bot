import json
import os
from os.path import join
from datetime import date, datetime, timedelta
from freezegun import freeze_time
from src import main
import requests

FROZEN_TIME = '2021-07-01'
BASE_URL = 'https://discord.com/api/v9'
BOT_TOKEN = 'Bot '+os.environ.get('BOT_TOKEN')
CHANNEL_ID = os.environ.get('CHANNEL_ID')

def test_e2e():
    with freeze_time(FROZEN_TIME):

        DAYS_UNTIL_BIRTHDAY = 14
        EXPECTED_MESSAGE='Joe Integration Testerson is turning 25 in two weeks on July 15. Maybe we should get him a new keyboard?'
        TEST_DATA_FILE = join(os.getcwd(),'temp','test-data.json')
        BIRTHDAY = date.today() + timedelta(days=DAYS_UNTIL_BIRTHDAY)
        BIRTHDATE = date(1995, BIRTHDAY.month, BIRTHDAY.day)

        test_data = {
            "date_format": "%Y-%m-%d",
            "reminder_in_days": str(DAYS_UNTIL_BIRTHDAY),
            "friends": [
                {
                    "name": "Joe Integration Testerson",
                    "birthdate": BIRTHDATE.strftime("%Y-%m-%d"),
                    "gift_ideas": [
                        "a new keyboard"
                    ]
                }
            ]
        }

        # Create directory for test data (https://stackoverflow.com/questions/12517451/automatically-creating-directories-with-file-output)
        if not os.path.exists(os.path.dirname(TEST_DATA_FILE)):
            try:
                os.makedirs(os.path.dirname(TEST_DATA_FILE))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        # Write test file and run script
        with open(TEST_DATA_FILE, 'w') as file:
            json.dump(test_data, file, indent=4)

        main.main(friends_file_path=TEST_DATA_FILE)

        # Call discord API to check if the new message is there
        response = requests.get(BASE_URL+'/channels/'+CHANNEL_ID+'/messages',
            headers={
                'Authorization': BOT_TOKEN,
                'Content-Type': 'application/json'
            })
        
        print("Last 5 message objects: \n"+json.dumps(response.json()[:5], indent=4, sort_keys=True))
        assert response.json()[0]['content'] == EXPECTED_MESSAGE
