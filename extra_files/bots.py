import json
import logging
import os
import requests
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')


def start(update, context):
    """ Функция с описанием бота """
    reply_keyboard = [['/start', '/help'],
                      ['/horoscope', '/info']]
    markup = ReplyKeyboardMarkup(reply_keyboard,
                                 one_time_keyboard=False)
    update.message.reply_text("Привет! Я подмастерье. Вот список команд: \n"
                              "/help - Контакты \n"
                              "/horoscope - Гороскоп & Котики \n"
                              "/info - Гадатели и цены", reply_markup=markup)


def helps(update, context):
    update.message.reply_text('Почта: witcheshut@mail.ru \n'
                              'Телеграм: @changethispls')


def info(update, context):
    context.bot.send_photo(
        update.message.chat_id, photo=open('../static/img/specialists/all_witches.png', 'rb'),
        caption="Наши специалисты приведены выше. \nСвязаться с нами напрямую: witcheshut@mail.ru"
    )


def horoscope(update, context):
    with open('../static/json/horoscope.json', encoding='utf-8') as file:
        data = json.load(file)
    if update.message.text == '/horoscope':
        reply_keyboard = [['Овен', 'Телец', 'Близнецы'],
                          ['Рак', 'Лев', 'Дева'],
                          ['Весы', 'Скорпион', 'Стрелец'],
                          ['Козерог', 'Водолей', 'Рыбы']]
        markup = ReplyKeyboardMarkup(reply_keyboard)
        update.message.reply_text("Напиши свой знак зодиака:", reply_markup=markup)
    else:
        text = f'Гороскоп на сегодня для знака зодиака {update.message.text}: \n'
        text += data['znak']['today']
        response = requests.get('https://aws.random.cat/meow')
        data = response.json()
        context.bot.send_photo(
            update.message.chat_id, photo=data['file'],
            caption=text
        )


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', helps))
    dp.add_handler(CommandHandler('info', info))
    text_handler = MessageHandler(Filters.text, horoscope)
    dp.add_handler(text_handler)
    dp.add_handler(CommandHandler('horoscope', horoscope))
    updater.start_polling()
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()