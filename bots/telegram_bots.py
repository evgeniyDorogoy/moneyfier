from telegram import ParseMode
from telegram.ext import CommandHandler, Updater

from config import TelegramConfig


def start(bot, update):
    update.message.reply_text(
        '*First of all, add this bot to your group chat*\n'
        '/stat — get statistics in group\n'
        '/me — get your own statistics\n',
        parse_mode=ParseMode.MARKDOWN,
    )


def on_error():
    pass


def message(msg):
    pass


def main():
    tc = TelegramConfig()
    updater = Updater(tc.bot_token)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_error_handler(on_error)

    updater.start_polling()

    updater.idle()
