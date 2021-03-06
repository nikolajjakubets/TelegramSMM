import telebot # импорт api бота
from telebot.types import Message
from telebot import types
from telebot.types import InputMediaPhoto
import api2ch # апи двача
import html2text #чтобы красово выглядили посты с двача без меток <br> им прочей лабуды
import wget #скачивать и отправлять картинки
# импорт виртуального окружения для получения токена
import os
from dotenv import load_dotenv
load_dotenv()
telegram_bot_token = os.getenv("telegram_bot_token")
print(telegram_bot_token)
#####################
bot = telebot.TeleBot(telegram_bot_token) # включение бота
#-------------------------------------------------------

# Парсинг ссылки
def link_parse(message):
    try:
        link = message.text
        link = link.split('/')
        if "2ch.hk" in link: #если это точно двач
            desk = link[3] # инфа о доске
            thread_num = link[5].split(".")[0] # номер треда
            bot.send_message(message.chat.id, "Парсинг треда")
            get_info_for_thread(message, desk, thread_num)
            return True
        else:
            pass
    except:
        pass
#--------------------------

def get_pic(message, desk, thread_num):
    api = api2ch.DvachApi(desk)
    thread = api.get_thread(thread_num)
    pic_in_thread = []
    for post in thread:
        for file in post.files:
            pic_in_thread.append(api2ch.CHAN_URL + file.path)
    bot.send_message(message.chat.id, pic_in_thread[0])

def get_info_for_thread(message, desk, thread_num):
    # переменные треда
    api = api2ch.DvachApi(desk)
    thread = api.get_thread(thread_num)
    text_of_OP = html2text.html2text(thread[0].comment)
    len_thread = "Всего " + str(len(thread)) + " постов"
    #--------------------
    # генерация текста о треде
    response_text = "\n" + \
        thread[0].subject + \
        "\n\n" + \
        len_thread + \
        "\n\n" + \
        text_of_OP[:900]
 
    pic = []
    file_url = "https://2ch.hk" + str(thread[0].files[0].path)
    pic.append(file_url)

    media = [InputMediaPhoto(pic[0], caption=response_text)]

    for i in range(1, len(thread[0].files)):
        file_url = "https://2ch.hk" + str(thread[0].files[i].path)
        pic.append(file_url)
        media.append(InputMediaPhoto(pic[i]))

    bot.send_media_group(message.chat.id, media)
    

    keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes'); #кнопка «Да»
    keyboard.add(key_yes); #добавляем кнопку в клавиатуру
    key_no= types.InlineKeyboardButton(text='Нет', callback_data='no');
    keyboard.add(key_no);
    
    bot.send_message(message.chat.id, "Что делать будем?", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes": #call.data это callback_data, которую мы указали при объявлении кнопки
        bot.send_message(call.message.chat.id, 'Запомню : )');
    elif call.data == "no":
        pass
    


@bot.message_handler(content_types=['text'])
def start(message):
    link_parse(message) #если это ссылка на тред, то ответ информацией о нем
    if message.text == "test":
        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes'); #кнопка «Да»
        keyboard.add(key_yes); #добавляем кнопку в клавиатуру
        key_no= types.InlineKeyboardButton(text='Нет', callback_data='no');
        keyboard.add(key_no);
        question = 'Тебе  лет, тебя зовут'
        bot.send_message(message.chat.id, text=question, reply_markup=keyboard)


bot.polling(none_stop=True, interval=0)