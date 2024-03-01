import telebot
import config
import random
from telebot import types
import datetime

import requests
from bs4 import BeautifulSoup
import re


session = requests.Session()

response = session.post(config.url, data=config.data, headers=config.header).text


journal_response = session.get(config.journal, headers=config.header).text

cookies_dict = [
    {"domain": key.domain, "name": key.name, "path": key.path, "value": key.value}
    for key in session.cookies
]

session2 = requests.Session()

for cookies in cookies_dict:
    session2.cookies.set(**cookies)

dirt_resp = session2.get(config.journal, headers=config.header).text

soup = BeautifulSoup(dirt_resp, 'lxml')
block = soup.find('div', class_='layout-inner__content')
all_hw = str(block.findAll('div', class_='dnevnik-lesson'))

next_week_dirt = session2.get(config.journal_next, headers=config.header).text
soup2 = BeautifulSoup(next_week_dirt, 'lxml')
block = soup2.find('div', class_='layout-inner__content')
hw_next = str(block.findAll('div', class_='dnevnik-lesson'))

soup3 = BeautifulSoup(''.join(map(str, all_hw)), 'html.parser')
hw_text = soup3.get_text()
hw_text = ' '.join(hw_text.split())
hw_text = hw_text.replace('[', '').replace(']', '')

soup4 = BeautifulSoup(''.join(map(str, hw_next)), 'html.parser')
hw_next = soup4.get_text()
hw_next = ' '.join(hw_next.split())
hw_next = hw_next.replace('[', '').replace(']', '')



start_index = hw_text.find('1. 08:00–08:40')
end_index = hw_text.find('1. 08:00–08:40', start_index + 1)


if start_index != -1 and end_index != -1:
    hw_monday = hw_text[:end_index]



second_occurrence = hw_text.find(', 1. 08:00–08:40')
third_occurrence = hw_text.find(', 1. 08:00–08:40', second_occurrence + 1)


if second_occurrence != -1 and third_occurrence != -1:
    hw_tuesday = hw_text[second_occurrence + len(', 1. 08:00–08:40'):third_occurrence]


pattern = re.compile(r'(?:.*?08:00–08:40.*?){3}(.*?08:00–08:40)')


matches = re.findall(pattern, hw_text)


hw_wednesday = matches[0] if matches else ''



pattern = re.compile(r'(?:.*?08:00–08:40.*?){4}(.*?08:00–08:40)')


matches = re.findall(pattern, hw_text)


hw_thursday = matches[0] if matches else ''


pattern = re.compile(r'(?:.*?08:00–08:40.*?){5}(.*)')


matches = re.findall(pattern, hw_text)


hw_friday = matches[0] if matches else ''








pattern = re.compile(r'\d\. 08:00–08:40(.*?)\d\. 08:00–08:40', re.DOTALL)
matches = re.findall(pattern, hw_next)


hw_monday_next = matches[0] if len(matches) > 0 else ''

second_occurrence = hw_next.find(', 1. 08:00–08:40')
third_occurrence = hw_next.find(', 1. 08:00–08:40', second_occurrence + 1)

if second_occurrence != -1 and third_occurrence != -1:
    hw_next_tuesday = hw_next[second_occurrence + len(', 1. 08:00–08:40'):third_occurrence]




today_date = datetime.date.today()


day_of_week = today_date.weekday()


days_of_week_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

current_day_of_week = days_of_week_list[day_of_week]


bot = telebot.TeleBot(config.TOKEN)
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton("🎲 Разное")
item2 = types.KeyboardButton("📚 Получить ДЗ")
item3 = types.KeyboardButton("🤓 След. неделя")
markup.add(item1, item2, item3)

print('БОТ ЗАПУЩЕН')


@bot.message_handler(commands=['start'])
def privet(message):
    user_id_telegram = message.from_user.id
    if user_id_telegram in config.whitelist:
        sti = open('static/welcome.webp', 'rb')
        bot.send_sticker(message.chat.id, sti)
        bot.send_message(message.chat.id, "Привет, {0.first_name}!\nЯ - <b>бот</b>, которого разрабатывает\n<b><a href='https://github.com/Evgenchick4434'>🍀Evgenchick4434🍀</a></b>\n \n✅ <i>Вы есть в белом списке, доступ разрешён.</i>".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "❌ Вас нету в белом списке этого бота, он не для вас...")


@bot.message_handler(content_types=['text'])
def otvet(message):
    if message.chat.id in config.whitelist:
        if message.chat.type == 'private':
            if message.text == '🎲 Разное':
                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("😱 Оценка по истории", callback_data='history')
                item2 = types.InlineKeyboardButton("📒 Учебник", callback_data='studbook')

                markup.add(item1, item2)

                bot.send_message(message.chat.id, "Выберите нужный пункт:", reply_markup=markup)
            elif message.text == "📚 Получить ДЗ":

                markup = types.InlineKeyboardMarkup(row_width=2)
                item0 = types.InlineKeyboardButton("📖 НА ЗАВТРА", callback_data='tomorrow')
                item1 = types.InlineKeyboardButton("😡 Понедельник", callback_data='monday')
                item2 = types.InlineKeyboardButton("😠 Вторник", callback_data='tuesday')
                item3 = types.InlineKeyboardButton("🙄 Среда", callback_data='wednesday')
                item4 = types.InlineKeyboardButton("😏 Четверг", callback_data='thursday')
                item5 = types.InlineKeyboardButton("😍 Пятница", callback_data='friday')

                markup.add(item0, item1, item2, item3, item4, item5)

                bot.send_message(message.chat.id, "<b>Выберите день недели:</b>".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)
            elif message.text == "🤓 След. неделя":

                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("😡 Понедельник", callback_data='monday_next')
                item2 = types.InlineKeyboardButton("😠 Вторник", callback_data='tuesday_next')

                markup.add(item1, item2)

                bot.send_message(message.chat.id, "<b>Выберите день cледующей недели:</b>\n<i>Други дни недели будут позже, связано с непонятным багом.</i>".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)
            elif message.text == "/about":
                bot.send_message(message.chat.id, "<i>🐍 <u>Разработчики</u>:\n<b>Evgenchick4434</b> - Разработчик, дизайнер.</i>\n<i><b>ChatGPT</b> - Правка кода, тыкание разраба носом в ошибки.</i>\n \n<b><a href='https://github.com/Evgenchick4434'>📁 Мой Github с другими проектами</a></b>\n<b>🪲 Нашли баг? Сообщите мне на почту</b> <i>evgenchickart@mail.ru</i>\n<b><a href='https://www.donationalerts.com/r/evgenchick4434/'>☕ Купить мне кофе</a></b>\n\n<i>Этот бот был написан <b>с нуля</b> на языке программирования <b>Python</b> используя библиотеку <b>pyTelegramBotAPI</b>. Исходный код будет позже на GitHub, но без моих авторизационных данных. Сбор информации с ЭлЖура работает через авторизацию на моём аккаунте. Не пытайтесь вытащить логин или пароль, через телеграм это просто невозможно.</i>".format(message.from_user, bot.get_me()), parse_mode='html')
            elif message.text == "/help":
                no_neg_video = open('static/guys.mp4', 'rb')
                bot.send_video(message.chat.id, no_neg_video)
                bot.send_message(message.chat.id, "Вообще, <b>спасение утопающих - дело рук самих утопающих</b>.\nНо так уж и быть - дам вам подсказку - напишите мне в лс.\n\n<b>ЕСЛИ ПРОПАЛА КЛАВИАТУРА</b> - /start".format(message.from_user, bot.get_me()), parse_mode='html')
            elif message.text == "/admin":
                trash = open('static/trash.mp4', 'rb')
                bot.send_video(message.chat.id, trash)
                bot.send_message(message.chat.id, "😱😱😱 Всё, ты взломал этого бота, конец света.")
            elif message.text == "/whitelist_add":
                if message.chat.id in config.admin_list:
                    def whitelist_adding(message):
                        chat_id = message.chat.id
                        new_whitelist_member = message.text
                        try:
                            config.whitelist_add(new_whitelist_member)
                            bot.send_message(chat_id, f'✅ Успешно добавил {new_whitelist_member} во временный белый список!')
                        except:
                            bot.send_message(chat_id, f"❌ Произошла ошибка")
                    bot.send_message(message.chat.id, "Введи ID пользователя для добавления его в белый список:")
                    bot.register_next_step_handler(message, whitelist_adding)
                else:
                    bot.send_message(message.chat.id, "🚫 Эта команда не для вас")
#           elif message.text == "/broadcast":
#               if message.chat.id in config.admin_list:
#                   def broadcast(message):
#                       for user_id in config.whitelist:
#                           bot.send_message(user_id, message)
#                   bot.send_message(message.chat.id, "Введи объявление:")
#                   bot.register_next_step_handler(message, broadcast)
#               else:
#                   bot.send_message(message.chat.id, "🚫 Эта команда не для вас")
            else:
                bot.send_message(message.chat.id, 'Несуществующая команда, пропишите /start')
    else:
        bot.send_message(message.chat.id, "❌ Вас нету в белом списке этого бота, он не для вас...")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'monday':
                if current_day_of_week == 'monday':
                    bot.send_message(call.message.chat.id, hw_monday)
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Успешно")
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Расписание и Д/З на выбранный день:", reply_markup=None)
                else:
                    bot.send_message(call.message.chat.id, "Домашняя работа на прошедшие дни не доступна.")
            elif call.data == 'tuesday':
                if current_day_of_week == 'monday' or current_day_of_week == 'tuesday':
                    bot.send_message(call.message.chat.id, hw_tuesday)
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Успешно")
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="Расписание и Д/З на выбранный день:", reply_markup=None)
                else:
                    bot.send_message(call.message.chat.id, "Домашняя работа на прошедшие дни не доступна.")
            elif call.data == 'wednesday':
                if current_day_of_week == 'monday' or current_day_of_week == 'tuesday' or current_day_of_week == 'wednesday':
                    bot.send_message(call.message.chat.id, hw_wednesday)
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Успешно")
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="Расписание и Д/З на выбранный день:", reply_markup=None)
                else:
                    bot.send_message(call.message.chat.id, "Домашняя работа на прошедшие дни не доступна.")
            elif call.data == 'thursday':
                if current_day_of_week == 'monday' or current_day_of_week == 'tuesday' or current_day_of_week == 'wednesday' or current_day_of_week == 'thursday':
                    bot.send_message(call.message.chat.id, hw_thursday)
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Успешно")
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="Расписание и Д/З на выбранный день:", reply_markup=None)
                else:
                    bot.send_message(call.message.chat.id, "Домашняя работа на прошедшие дни не доступна.")
            elif call.data == 'friday':
                if current_day_of_week == 'monday' or current_day_of_week == 'tuesday' or current_day_of_week == 'wednesday' or current_day_of_week == 'thursday' or current_day_of_week == 'friday':
                    bot.send_message(call.message.chat.id, hw_friday)
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Успешно")
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="Расписание и Д/З на выбранный день:", reply_markup=None)
                else:
                    bot.send_message(call.message.chat.id, "Домашняя работа на прошедшие дни не доступна.")
            elif call.data == 'history':
                history_mark = random.randint(2, 5)
                bot.send_message(call.message.chat.id, f"🔮 Твоя следующая оценка по истории - <b>{history_mark}</b>".format(call.from_user, bot.get_me()), parse_mode='html')
            elif call.data == 'studbook':
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="⌛ Выгружаю файл...")
                studbook_file = open('static/studbook.txt', 'rb')
                bot.send_document(call.message.chat.id, studbook_file)
            elif call.data == 'monday_next':
                bot.send_message(call.message.chat.id, hw_monday_next)
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Успешно")
            elif call.data == 'tuesday_next':
                bot.send_message(call.message.chat.id, hw_next_tuesday)
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Успешно")
            elif call.data == 'wednesday_next':
                bot.send_message(call.message.chat.id, 'В РАЗРАБОТКЕ')
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Успешно")
            elif call.data == 'thursday_next':
                bot.send_message(call.message.chat.id, 'В РАЗРАБОТКЕ')
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Успешно")
            elif call.data == 'friday_next':
                bot.send_message(call.message.chat.id, 'В РАЗРАБОТКЕ')
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Успешно")
            elif call.data == 'tomorrow':
                if current_day_of_week == 'monday':
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Д/З на ВТОРНИК")
                    bot.send_message(call.message.chat.id, hw_tuesday)
                if current_day_of_week == 'tuesday':
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Д/З на CРЕДУ")
                    bot.send_message(call.message.chat.id, hw_wednesday)
                if current_day_of_week == 'wednesday':
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Д/З на ЧЕТВЕРГ")
                    bot.send_message(call.message.chat.id, hw_thursday)
                if current_day_of_week == 'thursday':
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Д/З на ПЯТНИЦУ")
                    bot.send_message(call.message.chat.id, hw_friday)
                if current_day_of_week == 'friday' or current_day_of_week == 'saturday' or current_day_of_week == 'sunday':
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Д/З на ПОНЕДЕЛЬНИК")
                    bot.send_message(call.message.chat.id, hw_monday)


    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)
