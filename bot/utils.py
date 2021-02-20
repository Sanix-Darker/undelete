from telegram.ext import Updater, CommandHandler, MessageHandler

from bot.settings import TOKEN
from app.utils import *
from app.model import UnDelete, WatchMe

Ud = UnDelete.UnDelete
Wm = WatchMe.WatchMe


def presentation():
    print("[+] Ud-bot started on tg !")


def start_callback(bot, update):
    print("[+] start-callback")

    bot.send_message(
        chat_id=update.message.chat_id,
        text="Hello there, \nSend me a tweet link you want me to watch for you !"
    )


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
