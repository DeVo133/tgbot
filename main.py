import os
import random
import sqlite3
import emoji
import telebot
from telebot import types

bot = telebot.TeleBot('6122993473:AAGVccBcreIvIKSyJbPypo8TwMv7Gin81ZY')
name = None


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('/start', '/Анкета')
    user_markup.row('Фотки', 'Видео с выступлений')
    user_markup.row('/Контакты')
    bot.send_message(message.chat.id, 'Привет, это мой Фокусбот-помошник\n Тут ты можешь посмотреть мои фотки с '
                                      'выступлений \n , видео с выступлений,\n а так же оставить заявку, '
                                      'на мое выступление)))', reply_markup=user_markup)


@bot.message_handler(commands=['Анкета'])
def anketka(message):
    conn = sqlite3.connect('anketa.db')
    cur = conn.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS malyawi(id INTEGER PRIMARY KEY, name TEXT, num INTEGER, commentars TEXT); ")
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Введите имя:')
    bot.register_next_step_handler(message, user_name)


def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите ваш номер :')
    bot.register_next_step_handler(message, user_numb)


def user_numb(message):
    global numb
    numb = message.text.strip()
    bot.send_message(message.chat.id, 'Опишите подробнее ваше мероприятие:')
    bot.register_next_step_handler(message, user_comments)

def user_comments(message):
    comnt = message.text.strip()

    conn = sqlite3.connect('anketa.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO malyawi(name, num, commentars) VALUES (?, ?, ?)", (name, numb, comnt))
    conn.commit()
    cur.close()
    conn.close()
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Список заявок', callback_data='anketki'))
    bot.send_message(message.chat.id, 'Заявка создана', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('anketa.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM malyawi')
    all_users = cur.fetchall()
    spisok = ''
    for i in all_users:
        spisok += f'Имя:{i[1]}\n , номер:{i[2]}\n , комментарий:{i[3]}\n'
    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, spisok)

@bot.message_handler(commands=['Контакты'])
def cont(message):
    buttons = types.InlineKeyboardMarkup(row_width=2)
    urlbut_1 = types.InlineKeyboardButton(text=emoji.emojize(":camera: Instagram"),
                                          url='https://www.instagram.com/andreimrkv/')
    urlbut_2 = types.InlineKeyboardButton(text=emoji.emojize(":left_speech_bubble:VK"), url='https://vk.com/prokot97')
    urlbut_3 = types.InlineKeyboardButton(text=emoji.emojize("Брякнуть мне :call_me_hand_light_skin_tone:"),
                                          callback_data='urlbut_3')
    buttons.add(urlbut_1, urlbut_2, urlbut_3)
    bot.send_message(message.chat.id, "Cвязь со мной", reply_markup=buttons)


@bot.callback_query_handler(func=lambda callback: callback.data)
def cb_check(callback):
    if callback.data == 'urlbut_3':
        bot.send_contact(callback.message.chat.id, phone_number='80298461260', first_name='Andrei', last_name='Mrkv')


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'Фотки':
        direct = 'C:/Users/vavad/PycharmProjects/tgbot/portf'
        all_photo = os.listdir(direct)
        random_photo = random.choice(all_photo)
        img = open(direct + '/' + random_photo, 'rb')
        bot.send_chat_action(message.from_user.id, 'upload_photo')
        bot.send_photo(message.from_user.id, img)
        img.close()
    elif message.text == 'Видео с выступлений':
        video = 'C:/Users/vavad/PycharmProjects/tgbot/vido'
        all_vid = os.listdir(video)
        random_vid = random.choice(all_vid)
        vid = open(video + '/' + random_vid, 'rb')
        bot.send_chat_action(message.from_user.id, 'upload_video')
        bot.send_video(message.from_user.id, vid)
        vid.close()


bot.polling(none_stop=True)
