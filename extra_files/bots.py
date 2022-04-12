import logging
import os
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')


def start(update, context):
    reply_keyboard = [['/help', '/mcards'],
                      ['/stars', '/info']]
    markup = ReplyKeyboardMarkup(reply_keyboard,
                                 one_time_keyboard=False)
    update.message.reply_text("Привет! Я подмастерье. Вот список команд: \n"
        "/help - Контакты \n"
        "/mcards - Справочник карт \n"
        "/stars - Гороскоп & Котики \n"
        "/info - Контакты и цены", reply_markup=markup)


def helps(update, context):
    update.message.reply_text('Данелян Сергей \n'
                              'Гуляева Юля \n'
                              'Квитка Мария')


def mcard(update, context):
    update.message.reply_text('Вот значения всех карт!')


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('mcards', mcard))
    dp.add_handler(CommandHandler('help', helps))
    updater.start_polling()
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()