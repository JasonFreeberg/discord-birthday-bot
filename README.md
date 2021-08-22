# Discord Birthday Bot

A simple Discord Bot to show how to interact with REST APIs. Uses a JSON file to hold your friends' names and birthdays. The bot runs once per day with GitHub Actions, reads the file, and send a message to the main chat on the Discord server letting everyone know that someone's birthday is coming up!

TODO: Screenshot here

## Usage

1. Fork this repository
1. Create GitHub Actions Secrets for the bot token and channel ID.
    - `BOT_TOKEN`: Your Discord Bot token
    - `CHANNEL_ID`: The ID of the channel that you want the Bot to post in
1. Add your list of friends in the friends.json file with their names, birthdays, and gift ideas. You can make your fork private to keep the information private, or put the JSON file in a secret gist and put the URL to the JSON file where the main script is called in the workflow file.
1. Save your secrets and push your changes to the JSON file. The bot will run once per day.

## Local dev

1. Clone your fork of the repo
1. Create a venv and install the requirements
1. Run the script from the project root

    `python src/main.py birthdays.json`

1. Run tests by running `pytest` from the project root.

To contribute, make a PR and tag JasonFreeberg as a reviewer.
