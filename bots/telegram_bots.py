import logging

from telegram import ParseMode, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater

from config import TelegramConfig

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

PERIOD = 'period'
CATEGORY = 'category'


def start(bot, update):

    update.message.reply_text(
        '*Moneyfier bot helps people track they money spending*\n'
        '/{} — get statistics by type period\n'
        '/{} — get statistic by category\n'.format(PERIOD, CATEGORY),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardMarkup([['/' + PERIOD, '/' + CATEGORY]], one_time_keyboard=True),
    )


def period(bot, update):
    pass


def category(bot, update):
    pass


def on_error():
    pass


def message(msg):
    pass


def main():
    tc = TelegramConfig()
    updater = Updater(tc.bot_token)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler(PERIOD, period))
    dp.add_handler(CommandHandler(CATEGORY, category))

    dp.add_error_handler(on_error)

    updater.start_polling()

    updater.idle()
