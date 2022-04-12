import pandas as pd
from datetime import datetime
import re
import csv


def get_chat_dataframe(file):
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n\n\n')

        with open('comments.csv', 'w') as csvfile:

            for line in lines:
                try:
                    time_logged = line.split('—')[0].strip()
                    time_logged = datetime.strptime(
                        time_logged, '%Y-%m-%d_%H:%M:%S')

                    username_message = line.split('—')[1:]
                    username_message = '—'.join(username_message).strip()

                    search_result = re.search(
                        ':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', username_message
                    )

                    if search_result:
                        username, channel, message = search_result.groups()

                        d = {
                            'dt': time_logged,
                            'channel': channel,
                            'username': username,
                            'message': message
                        }

                        writer = csv.DictWriter(csvfile, fieldnames=[
                                                'dt', 'channel', 'username', 'message'])
                        writer.writerow(d)

                except Exception:
                    pass

    return csvfile


get_chat_dataframe('chat.log')


if __name__ == "__main__":
    get_chat_dataframe('chat.log')
