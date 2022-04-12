import socket
import logging
from emoji import demojize
import pandas as pd
from datetime import datetime
import re
from parser import get_chat_dataframe


def log():
    server = 'irc.chat.twitch.tv'
    port = 6667
    nickname = 'anna_ust'
    token = 'oauth:xm9h2totjjh9rzwu26td8gvo4lcfnt'
    channel = '#bolt_roleplay'

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s — %(message)s',
                        datefmt='%Y-%m-%d_%H:%M:%S',
                        handlers=[logging.FileHandler('chat.log', encoding='utf-8')])

    sock = socket.socket()
    sock.connect((server, port))
    sock.send(f"PASS {token}\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\n".encode('utf-8'))
    sock.send(f"JOIN {channel}\n".encode('utf-8'))

    while True:
        resp = sock.recv(2048).decode('utf-8')

        if resp.startswith('PING'):
            sock.send("PONG\n".encode('utf-8'))

        elif len(resp) > 0:
            logging.info(demojize(resp))


log()
