import json
import os
from os.path import join
from datetime import date, datetime, timedelta
from freezegun import freeze_time
from src import main
import responses

CHANNEL_ID = 'AAABBCCDD'
BOT_TOKEN = 'Bot aaabbbcccdddeeefff'
FROZEN_TIME = '2021-07-01'


def test_e2e(monkeypatch):

    DAYS_UNTIL_BIRTHDAY = 14
    EXPECTED_MESSAGE='Joe Integration Testerson is turning 0 in two weeks on September 18. Maybe we should get him A new keyboard ?'
    TEST_DATA_FILE = join(os.getcwd(),'temp','test-data.json')
    BIRTHDAY = date.today() + timedelta(days=DAYS_UNTIL_BIRTHDAY+1)

    test_data = {
        "date_format": "%Y-%m-%d",
        "reminder_in_days": str(DAYS_UNTIL_BIRTHDAY),
        "friends": [
            {
                "name": "Joe Integration Testerson",
                "birthdate": BIRTHDAY.strftime("%Y-%m-%d"),
                "gift_ideas": [
                    "A new keyboard"
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

    """
    ToDo: Call discord API to check if the new message is there
    """
