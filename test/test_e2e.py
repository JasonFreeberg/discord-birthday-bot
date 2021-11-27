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
TEST_DATA_FILE = join(os.getcwd(),'temp','test-data.json')

def test_e2e():

    # Can pull out the test data like this, add another person, add 1 or 2 more reminders, then run it at frozen times in method below.
    # Then beyond checking the messages sent to discord, I can add "days_until_next_message" or something in the summary info dict, and 
    # also use that to check

    with freeze_time(FROZEN_TIME):
        
        DAYS_UNTIL_BIRTHDAY1 = 14
        DAYS_UNTIL_BIRTHDAY2 = 2
        
        BIRTHDAY1 = date.today() + timedelta(days=DAYS_UNTIL_BIRTHDAY1)
        BIRTHDATE1 = date(1995, BIRTHDAY1.month, BIRTHDAY1.day)

        BIRTHDAY2 = date.today() + timedelta(days=DAYS_UNTIL_BIRTHDAY2)
        BIRTHDATE2 = date(1992, BIRTHDAY2.month, BIRTHDAY2.day)
        
        EXPECTED_MESSAGE1 = 'Joe Integration Testerson is turning 25 in two weeks on July 15. Maybe we should get him a new keyboard?'
        EXPECTED_MESSAGE2 = 'Jordan Quality Assuranceburg is turning 29 in two days on July 03. Maybe we should get him some festive socks?'

        test_data = {
            "date_format": "%Y-%m-%d",
            "reminders_in_days": [
                str(DAYS_UNTIL_BIRTHDAY1),
                str(DAYS_UNTIL_BIRTHDAY2)
            ],
            "friends": [
                {
                    "name": "Joe Integration Testerson",
                    "birthdate": BIRTHDATE1.strftime("%Y-%m-%d"),
                    "gift_ideas": [
                        "a new keyboard"
                    ]
                },
                {
                    "name": "Jordan Quality Assuranceburg",
                    "birthdate": BIRTHDATE2.strftime("%Y-%m-%d"),
                    "gift_ideas": [
                        "some festive socks"
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

        summary = main.main(friends_file_path=TEST_DATA_FILE)

        assert summary['successful_send_count'] == 2
        assert summary['total_send_count'] == 2
        assert summary['failed_send_count'] == 0

        # Call discord API to check if the new message is there
        response = requests.get(BASE_URL+'/channels/'+CHANNEL_ID+'/messages',
            headers={
                'Authorization': BOT_TOKEN,
                'Content-Type': 'application/json'
            })
        
        print("Last 5 message objects: \n"+json.dumps(response.json()[:5], indent=4, sort_keys=True))
        assert response.json()[0]['content'] == EXPECTED_MESSAGE2
        assert response.json()[1]['content'] == EXPECTED_MESSAGE1
