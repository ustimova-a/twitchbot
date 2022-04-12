from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from log import log
from parser import get_chat_dataframe
import socket
import logging
from emoji import demojize
import pandas as pd
from datetime import datetime
import re
from parser import get_chat_dataframe


def start(update, context):
    update.message.reply_text('Started logging')
    server = 'irc.chat.twitch.tv'
    port = 6667
    nickname = 'anna_ust'
    token = 'oauth:xm9h2totjjh9rzwu26td8gvo4lcfnt'
    channel = '#burkeblack'

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s — %(message)s',
                        datefmt='%Y-%m-%d_%H:%M:%S',
                        handlers=[logging.FileHandler('chat.log', encoding='utf-8')])

    sock = socket.socket()
    sock.connect((server, port))
    sock.send(f"PASS {token}\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\n".encode('utf-8'))
    sock.send(f"JOIN {channel}\n".encode('utf-8'))

    while update.message.text != 'stop':
        resp = sock.recv(2048).decode('utf-8')

        if resp.startswith('PING'):
            sock.send("PONG\n".encode('utf-8'))

        elif len(resp) > 0:
            logging.info(demojize(resp))


def get_file(update, context):
    update.message.reply_text('Generating file')
    get_chat_dataframe('chat.log')


def error(update, context):
    update.message.reply_text('an error occured')


def text(update, context):
    text_received = update.message.text
    update.message.reply_text(f'did you said "{text_received}" ?')


def main():
    token = '5176515362:AAGrqG4Pqd6FKJQ8M-EprT5vFc4AYN_uz0M'
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("get_file", get_file))

    dispatcher.add_handler(MessageHandler(Filters.text, text))

    dispatcher.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
