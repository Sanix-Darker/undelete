from functools import wraps

from telegram.ext import Updater, CommandHandler, MessageHandler

from app.utils import *
from app.model import UnDelete, WatchMe
import sys, traceback

Ud = UnDelete.UnDelete
Wm = WatchMe.WatchMe


def get_trace():
    print("Exception in code:")
    print("-" * 60)
    traceback.print_exc(file=sys.stdout)
    print("-" * 60)


def presentation():
    print("[+] Ud-bot started on tg !")


# A Decorator for errors
def catch_error(f):
    @wraps(f)
    def wrap(bot, update):
        try:
            return f(bot, update)
        except Exception as e:
            get_trace()
            bot.send_message(chat_id=update.message.chat_id,
                             text="An error occured, please try later ...")

    return wrap


def start_callback(bot, update):
    print("[+] start-callback")

    bot.send_message(
        chat_id=update.message.chat_id,
        text="Hello there, \nSend me a tweet link you want me to watch for you !"
    )


@catch_error
def echo_callback(bot, update):
    print("[+] echo-callback")

    srch = update.message.text
    if dump_tweet_link_validation(srch):
        chat_id = update.message.chat_id

        result = watch_this(Ud, Wm, srch, str(chat_id))

        bot.send_message(
            chat_id=update.message.chat_id,
            text="Ok ok,\n" + result["message"]
        )
    else:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Hmmmmh...\nYour tweet-link seems to be not valid, please check it again.".format(srch)
        )


def help_callback(bot, update):
    print("[+] help-callback")

    bot.send_message(
        chat_id=update.message.chat_id,
        text="Hello there, \nSend me a tweet link you want me to watch for you !"
    )


start_handler = CommandHandler("start", start_callback)
help_handler = CommandHandler("help", help_callback)
echo_handler = MessageHandler(callback=echo_callback, filters=None)

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
