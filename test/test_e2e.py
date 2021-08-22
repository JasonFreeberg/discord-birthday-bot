from freezegun import freeze_time
from src import main
import responses

CHANNEL_ID = 'AAABBCCDD'
BOT_TOKEN = 'Bot aaabbbcccdddeeefff'
FROZEN_TIME = '2021-07-01'


@responses.activate
def test_e2e(monkeypatch):

    responses.add(responses.POST, f'https://discord.com/api/v9/channels/{CHANNEL_ID}/messages', json={
                  'error': 'not found'}, status=404)
    monkeypatch.setenv('CHANNEL_ID', CHANNEL_ID)
    monkeypatch.setenv('BOT_TOKEN', BOT_TOKEN)

    with freeze_time(FROZEN_TIME):
        main.main('test/test_data.json')

        assert len(responses.calls) == 2
        assert responses.calls[0].body.content == ''
