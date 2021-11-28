from typing import Text
from mysql.connector.utils import validate_normalized_unicode_string
import telebot
import mysql.connector
import config
from telebot import types
from datetime import datetime, time, timedelta
import re
import time

TOKEN = "2048301461:AAERZRoM-7xUTYAgdij-mJkCfDlWOdXk5-o"
bot = telebot.TeleBot(TOKEN)


db = mysql.connector.connect(
  host=config.host,
  user=config.user,
  password=config.password,
  port=config.port,
  database=config.database
)
 
cursor = db.cursor()
today = datetime.today().weekday()
today_date = datetime.now()
date_today_str = today_date.strftime('%Y-%m-%d')

today_plus_seven_days = datetime.now() + timedelta(days=6)
sub_date = today_plus_seven_days.strftime('%Y-%m-%d')


nowTime = int(time.time())


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    sql = "SELECT user_group FROM users WHERE userid={0}".format(message.from_user.id)
    cursor.execute(sql)
    existsUser = cursor.fetchone()

    print(nowTime)

    if (existsUser == None):
        msg = bot.send_message(message.chat.id, "Спасибо за регистрацию. Подарочная подписка на 7 дней уже активирована.\n\nВведите корректное наименование вашей группы. Например, КИС9-121А")
        bot.register_next_step_handler(msg, process_registrationuser_step)
    
    else:
        bot.delete_message(message.chat.id, message.message_id)
        markup = types.InlineKeyboardMarkup(row_width=2)
        item_btn_tablelist = types.InlineKeyboardButton(text = 'Расписание', callback_data='tablelist')
        item_btn_option = types.InlineKeyboardButton(text = '⚙ Опции', callback_data='option')
        item_btn_subs = types.InlineKeyboardButton(text = 'Подписка', callback_data='sub')
        item_btn_about_bot = types.InlineKeyboardButton(text = '🌍 Что это?', callback_data='about_bot')
        markup.add(item_btn_tablelist, item_btn_option, item_btn_subs, item_btn_about_bot)
        bot.send_message(message.chat.id, "С возвращением!\nИспользуй меню для продолжения", reply_markup=markup)

@bot.callback_query_handler(func = lambda call: True)
def answer(call: types.CallbackQuery):
    #Кнопка РАСПИСАНИЕ
    if call.data == 'tablelist':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = types.InlineKeyboardMarkup(row_width=2)
        item_btn_tablelist_top_week = types.InlineKeyboardButton(text='Неделя 1', callback_data='week_one')
        item_btn_tablelist_low_week = types.InlineKeyboardButton(text='Неделя 2', callback_data='week_two')
        item_btn_back = types.InlineKeyboardButton(text='◀ Назад', callback_data='back')
        markup.add(item_btn_tablelist_top_week, item_btn_tablelist_low_week, item_btn_back)
        bot.send_message(call.message.chat.id, 'Выберите неделю', reply_markup=markup)
    
    #Кнопка Опции
    elif call.data == 'option':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = types.InlineKeyboardMarkup(row_width=2)
        item_btn_add_group = types.InlineKeyboardButton(text='Добавить', callback_data='add_group')
        item_btn_send_error = types.InlineKeyboardButton(text='❌Ошибка?', callback_data='error')
        item_btn_group = types.InlineKeyboardButton(text='♦ Группа', callback_data='group')
        item_btn_donat = types.InlineKeyboardButton(text='💰 Donate', callback_data='donat')
        item_btn_back = types.InlineKeyboardButton(text='◀ Назад', callback_data='back')
        markup.add(item_btn_group, item_btn_add_group, item_btn_send_error, item_btn_donat, item_btn_back)
        bot.send_message(call.message.chat.id, 'Для продолжения используй меню', reply_markup=markup)
    
    #Кнопка Что это?
    elif call.data == 'about_bot':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = types.InlineKeyboardMarkup(row_width=2)
        item_btn_tablelist = types.InlineKeyboardButton(text = 'Расписание', callback_data='tablelist')
        item_btn_option = types.InlineKeyboardButton(text = '⚙ Опции', callback_data='option')
        item_btn_subs = types.InlineKeyboardButton(text = 'Подписка', callback_data='sub')
        item_btn_about_bot = types.InlineKeyboardButton(text = '🌍 Что это?', callback_data='about_bot')
        markup.add(item_btn_tablelist, item_btn_option, item_btn_subs, item_btn_about_bot)
        bot.send_message(call.message.chat.id, 'Этот бот показывает твое расписание в Колледже экономики и сервиса.\nОбратите внимание на то, что здесь не учитываются замены!', reply_markup=markup)

    #Кнопка Назад
    elif call.data == 'back':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = types.InlineKeyboardMarkup(row_width=2)
        item_btn_tablelist = types.InlineKeyboardButton(text = 'Расписание', callback_data='tablelist')
        item_btn_option = types.InlineKeyboardButton(text = '⚙ Опции', callback_data='option')
        item_btn_subs = types.InlineKeyboardButton(text = 'Подписка', callback_data='sub')
        item_btn_about_bot = types.InlineKeyboardButton(text = '🌍 Что это?', callback_data='about_bot')
        markup.add(item_btn_tablelist, item_btn_option, item_btn_subs, item_btn_about_bot)
        bot.send_message(call.message.chat.id, 'Для продолжения используй меню', reply_markup=markup)

    #БЛОК Опции
    #Кнопка Группа
    elif call.data == 'group':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = types.InlineKeyboardMarkup(row_width=2)
        item_btn_my_group = types.InlineKeyboardButton(text = '🔥 Моя', callback_data='my_group')
        item_btn_change_group = types.InlineKeyboardButton(text = 'Изменить', callback_data='change_group')
        item_btn_list_group = types.InlineKeyboardButton(text = '📌Список', callback_data='list_group')
        item_btn_back = types.InlineKeyboardButton(text = '◀ Назад', callback_data='back')
        markup.add(item_btn_my_group, item_btn_change_group, item_btn_list_group, item_btn_back)
        bot.send_message(call.message.chat.id, 'Для продолжения используй меню', reply_markup=markup)

    #Кнопка Добавить
    elif call.data == 'add_group':
        markup = types.InlineKeyboardMarkup(row_width=2)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        item_btn_add_group = types.InlineKeyboardButton(text='Добавить', callback_data='add_group')
        item_btn_send_error = types.InlineKeyboardButton(text='❌Ошибка?', callback_data='error')
        item_btn_group = types.InlineKeyboardButton(text='♦ Группа', callback_data='group')
        item_btn_donat = types.InlineKeyboardButton(text='💰 Donate', callback_data='donat')
        item_btn_back = types.InlineKeyboardButton(text='◀ Назад', callback_data='back')
        markup.add(item_btn_group, item_btn_add_group, item_btn_send_error, item_btn_donat, item_btn_back)
        bot.send_message(call.message.chat.id, 'Чтобы оставить заявку на добавление твоей группы, отправь письмо на rgdevelopers.ru@gmail.com с указанием наименования группы и ее расписанием на обе недели. В течении суток мы добавим твою группу', reply_markup=markup)

    #Кнопка Ошибка
    elif call.data == 'error':
        markup = types.InlineKeyboardMarkup(row_width=2)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        item_btn_add_group = types.InlineKeyboardButton(text='Добавить', callback_data='add_group')
        item_btn_send_error = types.InlineKeyboardButton(text='❌Ошибка?', callback_data='error')
        item_btn_group = types.InlineKeyboardButton(text='♦ Группа', callback_data='group')
        item_btn_donat = types.InlineKeyboardButton(text='💰 Donate', callback_data='donat')
        item_btn_back = types.InlineKeyboardButton(text='◀ Назад', callback_data='back')
        markup.add(item_btn_group, item_btn_add_group, item_btn_send_error, item_btn_donat, item_btn_back)
        bot.send_message(call.message.chat.id, 'Нашел ошибку в расписании? Отправь письмо на rgdevelopers.ru@gmail.com с подробным описанием ошибки. В течении суток мы исправим свою оплошность', reply_markup=markup)
    
    #Кнопка Donate
    elif call.data == 'donat':
        markup = types.InlineKeyboardMarkup(row_width=2)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        item_btn_card = types.InlineKeyboardButton(text='❤ QIWI', callback_data='qiwi')
        item_btn_yoomoney = types.InlineKeyboardButton(text='❤ ЮMoney', callback_data='yoomoney')
        item_btn_back = types.InlineKeyboardButton(text='◀ Назад', callback_data='back')
        markup.add(item_btn_card, item_btn_yoomoney, item_btn_back)
        bot.send_message(call.message.chat.id, 'Для продолжения используй меню', reply_markup=markup)

    #Кнопка Моя
    elif call.data == 'my_group':
        markup = types.InlineKeyboardMarkup(row_width=2)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        sql = "SELECT user_group FROM users WHERE userid={0}".format(call.from_user.id)
        cursor.execute(sql)
        user_group = cursor.fetchone()
        item_btn_my_group = types.InlineKeyboardButton(text = '🔥 Моя', callback_data='my_group')
        item_btn_change_group = types.InlineKeyboardButton(text = 'Изменить', callback_data='change_group')
        item_btn_list_group = types.InlineKeyboardButton(text = '📌Список', callback_data='list_group')
        item_btn_back = types.InlineKeyboardButton(text = '◀ Назад', callback_data='back')
        markup.add(item_btn_my_group, item_btn_change_group, item_btn_list_group, item_btn_back)
        bot.send_message(call.message.chat.id, user_group, reply_markup=markup)

    #Кнопка Изменить
    elif call.data == 'change_group':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        msg = bot.send_message(call.message.chat.id, 'Введите наименование новой группы')
        bot.register_next_step_handler(msg, process_changegroup_step)

    #Кнопка Список
    elif call.data == 'list_group':
        markup = types.InlineKeyboardMarkup(row_width=2)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        item_btn_my_group = types.InlineKeyboardButton(text = '🔥 Моя', callback_data='my_group')
        item_btn_change_group = types.InlineKeyboardButton(text = 'Изменить', callback_data='change_group')
        item_btn_list_group = types.InlineKeyboardButton(text = '📌Список', callback_data='list_group')
        item_btn_back = types.InlineKeyboardButton(text = '◀ Назад', callback_data='back')
        markup.add(item_btn_my_group, item_btn_change_group, item_btn_list_group, item_btn_back)
        sql = "SELECT group_name FROM tablelist ORDER BY group_name ASC"
        cursor.execute(sql)
        user_group = cursor.fetchall()
        bot.send_message(call.message.chat.id, "Доступно расписание следующих групп:\n")
        for group in user_group:
            bot.send_message(call.message.chat.id, group[0]+"\n")

        bot.send_message(call.message.chat.id, "\nЕсли в этом списке нет твоей группы ты можешь оставить заявку на добавление. Для этого перейди в ⚙ Опции, нажми кнопку Добавить и следуй указаниям", reply_markup=markup)

    #Кнопка QIWI
    elif call.data == 'qiwi':
        markup = types.InlineKeyboardMarkup(row_width=2)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        item_btn_card = types.InlineKeyboardButton(text='❤ QIWI', callback_data='qiwi')
        item_btn_yoomoney = types.InlineKeyboardButton(text='❤ ЮMoney', callback_data='yoomoney')
        item_btn_back = types.InlineKeyboardButton(text='◀ Назад', callback_data='back')
        markup.add(item_btn_card, item_btn_yoomoney, item_btn_back)
        bot.send_message(call.message.chat.id, 'Хочешь поддержать разработчика и улучшить качество софта? Можешь отправить любую сумму на карту - 4890 4947 2349 4209. Спасибо', reply_markup=markup)

    #Кнопка ЮMoney
    elif call.data == 'yoomoney':
        markup = types.InlineKeyboardMarkup(row_width=2)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        item_btn_card = types.InlineKeyboardButton(text='❤ QIWI', callback_data='qiwi')
        item_btn_yoomoney = types.InlineKeyboardButton(text='❤ ЮMoney', callback_data='yoomoney')
        item_btn_back = types.InlineKeyboardButton(text='◀ Назад', callback_data='back')
        markup.add(item_btn_card, item_btn_yoomoney, item_btn_back)
        bot.send_message(call.message.chat.id, 'Хочешь поддержать разработчика и улучшить качество софта? Можешь отправить любую сумму на кошелек - 4100 1172 2270 4122. Спасибо', reply_markup=markup)


    #БЛОК Расписание
    #Кнопка Неделя 1
    elif call.data == 'week_one':
        markup = types.InlineKeyboardMarkup(row_width=2)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        item_btn_tablelist_dat = types.InlineKeyboardButton(text='💛 Сегодня', callback_data='now')
        item_btn_tablelist_tomorrow = types.InlineKeyboardButton(text='💚 Завтра', callback_data='twomorrow')
        item_btn_tablelist_week = types.InlineKeyboardButton(text='🧡 Неделя', callback_data='first_week')
        item_btn_back = types.InlineKeyboardButton(text='◀ Назад', callback_data='back')
        markup.add(item_btn_tablelist_dat, item_btn_tablelist_tomorrow, item_btn_tablelist_week, item_btn_back)
        bot.send_message(call.message.chat.id, 'Какое расписание показать?', reply_markup=markup)

    #Кнопка Сегодня 1
    elif call.data == 'now':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_btn_tablelist = types.KeyboardButton('OK')
        markup.add(item_btn_tablelist)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        msg = bot.send_message(call.message.chat.id, 'Введите любой символ или нажмите кнопку OK', reply_markup=markup)
        bot.register_next_step_handler(msg, process_tablelistdaytopweek_step)

    #Кнопка Завтра 1
    elif call.data == 'twomorrow':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_btn_tablelist = types.KeyboardButton('OK')
        markup.add(item_btn_tablelist)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        msg = bot.send_message(call.message.chat.id, 'Введите любой символ или нажмите кнопку OK', reply_markup=markup)
        bot.register_next_step_handler(msg, process_tablelisttomorrowtopweek_step)

    #Кнопка Неделя 1
    elif call.data == 'first_week':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_btn_tablelist = types.KeyboardButton('OK')
        markup.add(item_btn_tablelist)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        msg = bot.send_message(call.message.chat.id, 'Введите любой символ или нажмите кнопку еще раз')
        bot.register_next_step_handler(msg, process_tablelisttopweek_step)


    #Кнопка Неделя 2
    elif call.data == 'week_two':
        markup = types.InlineKeyboardMarkup(row_width=2)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        item_btn_tablelist_dat = types.InlineKeyboardButton(text='💙 Сегодня', callback_data='now_two')
        item_btn_tablelist_tomorrow = types.InlineKeyboardButton(text='💜 Завтра', callback_data='twomorrow_two')
        item_btn_tablelist_week = types.InlineKeyboardButton(text='🖤 Неделя', callback_data='second_week')
        item_btn_back = types.InlineKeyboardButton(text='◀ Назад', callback_data='back')
        markup.add(item_btn_tablelist_dat, item_btn_tablelist_tomorrow, item_btn_tablelist_week, item_btn_back)
        bot.send_message(call.message.chat.id, 'Какое расписание показать?', reply_markup=markup)


    #Кнопка Сегодня
    elif call.data == 'now_two':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_btn_tablelist = types.KeyboardButton('OK')
        markup.add(item_btn_tablelist)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        msg = bot.send_message(call.message.chat.id, 'Введите любой символ или нажмите кнопку OK', reply_markup=markup)
        bot.register_next_step_handler(msg, process_tablelistdaylowweek_step)

    #Кнопка Завтра
    elif call.data == 'twomorrow_two':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_btn_tablelist = types.KeyboardButton('OK')
        markup.add(item_btn_tablelist)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        msg = bot.send_message(call.message.chat.id, 'Введите любой символ или нажмите кнопку OK', reply_markup=markup)
        bot.register_next_step_handler(msg, process_tablelisttomorrowlowweek_step)

    #Кнопка Неделя 2 table
    elif call.data == 'second_week':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_btn_tablelist = types.KeyboardButton('OK')
        markup.add(item_btn_tablelist)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        msg = bot.send_message(call.message.chat.id, 'Введите любой символ или нажмите кнопку еще раз')
        bot.register_next_step_handler(msg, process_tablelistlowweek_step)

    #Кнопка Подписка
    elif call.data == 'sub':
        markup = types.InlineKeyboardMarkup(row_width=2)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        item_btn_sub_week = types.InlineKeyboardButton(text='7 дней', callback_data='sub_seven_days')
        item_btn_sum_month = types.InlineKeyboardButton(text='30 дней', callback_data='sub_month')
        item_btn_back = types.InlineKeyboardButton(text='◀ Назад', callback_data='back')
        markup.add(item_btn_sub_week, item_btn_sum_month, item_btn_back)
        bot.send_message(call.message.chat.id, 'Подписка позволяет пользоваться данным ботом. Чтобы оформить подписку, для начала выбери срок действия', reply_markup=markup)

    #Кнопка 7 дней
    elif call.data == 'sub_seven_days':
        markup = types.InlineKeyboardMarkup(row_width=2)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        item_btn_sub_week = types.InlineKeyboardButton(text='7 дней', callback_data='sub_seven_days')
        item_btn_sum_month = types.InlineKeyboardButton(text='30 дней', callback_data='sub_month')
        item_btn_back = types.InlineKeyboardButton(text='◀ Назад', callback_data='back')
        markup.add(item_btn_sub_week, item_btn_sum_month, item_btn_back)
        bot.send_message(call.message.chat.id, 'Подписка на 7 дней.\n\nЧтобы оформить подписку оплати ее переводом на сумму 10 рублей на кошелек ЮMoney - 4890 4947 2349 4209. Это можно сделать в твоем онлайн банке без комиссии. После успешной оплаты отправь чек нашему администратору - @rg_staff', reply_markup=markup)

    #Кнопка 30 дней
    elif call.data == 'sub_month':
        markup = types.InlineKeyboardMarkup(row_width=2)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        item_btn_sub_week = types.InlineKeyboardButton(text='7 дней', callback_data='sub_seven_days')
        item_btn_sum_month = types.InlineKeyboardButton(text='30 дней', callback_data='sub_month')
        item_btn_back = types.InlineKeyboardButton(text='◀ Назад', callback_data='back')
        markup.add(item_btn_sub_week, item_btn_sum_month, item_btn_back)
        bot.send_message(call.message.chat.id, 'Подписка на 30 дней.\n\nЧтобы оформить подписку оплати ее переводом на сумму 30 рублей на кошелек ЮMoney - 4890 4947 2349 4209. Это можно сделать в твоем онлайн банке без комиссии. После успешной оплаты отправь чек нашему администратору - @rg_staff', reply_markup=markup)












#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#Регистрация пользователя в базе данных
def process_registrationuser_step(message):
    try:
        bonusSubTime = nowTime + days_to_seconds(7)
        sql = "INSERT INTO users (userid, user_group, date_registration, sub_end) VALUES (%s, %s, %s, %s)"
        val = (message.from_user.id, message.text, date_today_str, bonusSubTime)
        cursor.execute(sql, val)
        db.commit()

        markup = types.InlineKeyboardMarkup(row_width=2)
        item_btn_tablelist = types.InlineKeyboardButton(text = 'Расписание', callback_data='tablelist')
        item_btn_option = types.InlineKeyboardButton(text = '⚙ Опции', callback_data='option')
        item_btn_subs = types.InlineKeyboardButton(text = 'Подписка', callback_data='sub')
        item_btn_about_bot = types.InlineKeyboardButton(text = '🌍 Что это?', callback_data='about_bot')
        markup.add(item_btn_tablelist, item_btn_option, item_btn_subs, item_btn_about_bot)
        bot.send_message(message.chat.id, "Вы успешно зарегистрированы\nЧтобы узнать свое расписание нажмите на соответствующую кнопку в меню", reply_markup=markup)

    except Exception as e:
        bot.reply_to(message, 'Error: registration false')
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#поиск Расписание на сегодня по 1 неделе
def process_tablelistdaytopweek_step(message):
    try:
        db = mysql.connector.connect(
        host=config.host,
        user=config.user,
        password=config.password,
        port=config.port,
        database=config.database
        )
        cursor = db.cursor()

        #Получение наименования группы пользователя
        sql = "SELECT user_group FROM users WHERE userid=%s"
        val = (message.from_user.id, )
        cursor.execute(sql, val)
        groups = cursor.fetchall()
        for group in groups:
            userGroup = group[0]

        #*********************************************************
        sql = "SELECT sub_end FROM users WHERE userid=%s"
        val = (message.from_user.id, )
        cursor.execute(sql, val)
        result = cursor.fetchall()
        for time in result:
            sub_end_time = time[0]
        print(sub_end_time)
        
        #*********************************************************

        if sub_end_time < nowTime:
            markup = types.InlineKeyboardMarkup()
            bot.delete_message(message.chat.id, message.message_id)
            item_btn_subs = types.InlineKeyboardButton(text = 'Подписка', callback_data='sub')
            item_btn_back = types.InlineKeyboardButton(text='◀ Назад', callback_data='back')
            markup.add(item_btn_subs, item_btn_back)
            bot.send_message(message.chat.id, "Срок действия подписки истек. Оформи новую чтобы продолжить пользоваться услугами бота", reply_markup=markup)
        else:
            #Получение расписания пользователя по группе
            markup = types.InlineKeyboardMarkup()
            bot.delete_message(message.chat.id, message.message_id)
            item_btn_tablelist_day = types.InlineKeyboardButton(text='💛 Сегодня', callback_data='now')
            item_btn_tablelist_tomorrow = types.InlineKeyboardButton(text='💚 Завтра', callback_data='twomorrow')
            item_btn_tablelist_week = types.InlineKeyboardButton(text='🧡 Неделя', callback_data='first_week')
            item_btn_back = types.InlineKeyboardButton(text='◀ Назад', callback_data='back')
            markup.add(item_btn_tablelist_day, item_btn_tablelist_tomorrow, item_btn_tablelist_week, item_btn_back)
            sql = 'SELECT * FROM tablelist WHERE group_name=%s'
            val = (userGroup, )
            cursor.execute(sql, val)
            lists = cursor.fetchall()
            for list in lists:
                if today == 0:
                    bot.send_message(message.chat.id, "Расписание группы " + list[1] + " на сегодня:\n\n" + list[3], reply_markup=markup)
                elif today == 1:
                    bot.send_message(message.chat.id, "Расписание группы " + list[1] + " на сегодня:\n\n" + list[4], reply_markup=markup)
                elif today == 2:
                    bot.send_message(message.chat.id, "Расписание группы " + list[1] + " на сегодня:\n\n" + list[5],reply_markup=markup )
                elif today == 3:
                    bot.send_message(message.chat.id, "Расписание группы " + list[1] + " на сегодня:\n\n" +  list[6], reply_markup=markup)
                elif today == 4:
                    bot.send_message(message.chat.id, "Расписание группы " + list[1] + " на сегодня:\n\n" + list[7], reply_markup=markup)
                elif today == 5:
                    bot.send_message(message.chat.id, "Сегодня у тебя выходой", reply_markup=markup)
                elif today == 6:
                    bot.send_message(message.chat.id, "Сегодня у тебя выходой", reply_markup=markup)

            cursor.close()
            db.close()
    except Exception as e:
        bot.reply_to(message, 'Error #2')
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#поиск Расписание на завтра по 1 неделе
def process_tablelisttomorrowtopweek_step(message):
    try:
        db = mysql.connector.connect(
        host=config.host,
        user=config.user,
        password=config.password,
        port=config.port,
        database=config.database
        )
        cursor = db.cursor()

        #Получение наименования группы пользователя
        sql = "SELECT user_group FROM users WHERE userid=%s"
        val = (message.from_user.id, )
        cursor.execute(sql, val)
        groups = cursor.fetchall()
        for group in groups:
            userGroup = group[0]


        #*********************************************************
        sql = "SELECT sub_end FROM users WHERE userid=%s"
        val = (message.from_user.id, )
        cursor.execute(sql, val)
        result = cursor.fetchall()
        for time in result:
            sub_end_time = time[0]
        print(sub_end_time)
        #*********************************************************

        if sub_end_time < nowTime:
            markup = types.InlineKeyboardMarkup()
            bot.delete_message(message.chat.id, message.message_id)
            item_btn_subs = types.InlineKeyboardButton(text = 'Подписка', callback_data='sub')
            item_btn_back = types.InlineKeyboardButton(text='◀ Назад', callback_data='back')
            markup.add(item_btn_subs, item_btn_back)
            bot.send_message(message.chat.id, "Срок действия подписки истек. Оформи новую чтобы продолжить пользоваться услугами бота", reply_markup=markup)
        else:
            markup = types.InlineKeyboardMarkup()
            bot.delete_message(message.chat.id, message.message_id)
            item_btn_tablelist_dat = types.InlineKeyboardButton(text='💛 Сегодня', callback_data='now')
            item_btn_tablelist_tomorrow = types.InlineKeyboardButton(text='💚 Завтра', callback_data='twomorrow')
            item_btn_tablelist_week = types.InlineKeyboardButton(text='🧡 Неделя', callback_data='first_week')
            item_btn_back = types.InlineKeyboardButton(text='◀ Назад', callback_data='back')
            markup.add(item_btn_tablelist_dat, item_btn_tablelist_tomorrow, item_btn_tablelist_week, item_btn_back)
            #Получение расписания пользователя по группе
            sql = 'SELECT * FROM tablelist WHERE group_name=%s'
            val = (userGroup, )
            cursor.execute(sql, val)
            lists = cursor.fetchall()
            for list in lists:
                if today == 0:
                    bot.send_message(message.chat.id, "Расписание группы " + list[1] + " на завтра:\n\n" + list[4], reply_markup=markup)
                elif today == 1:
                    bot.send_message(message.chat.id, "Расписание группы " + list[1] + " на завтра:\n\n" + list[5], reply_markup=markup)
                elif today == 2:
                    bot.send_message(message.chat.id, "Расписание группы " + list[1] + " на завтра:\n\n" + list[6], reply_markup=markup)
                elif today == 3:
                    bot.send_message(message.chat.id, "Расписание группы " + list[1] + " на завтра:\n\n" +  list[7], reply_markup=markup)
                elif today == 4:
                    bot.send_message(message.chat.id, "Завтра у тебя выходой", reply_markup=markup)
                elif today == 5:
                    bot.send_message(message.chat.id, "Завтра у тебя выходой", reply_markup=markup)
                elif today == 6:
                    bot.send_message(message.chat.id, "Расписание группы " + list[1] + " на завтра:\n\n" + list[3], reply_markup=markup)
            cursor.close()
            db.close()
    except Exception as e:
        bot.reply_to(message, 'Error #222')
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#поиск Расписание на 1 неделю
def process_tablelisttopweek_step(message):
    try:
        db = mysql.connector.connect(
        host=config.host,
        user=config.user,
        password=config.password,
        port=config.port,
        database=config.database
        )
        cursor = db.cursor()
        #*********************************************************
        sql = "SELECT sub_end FROM users WHERE userid=%s"
        val = (message.from_user.id, )
        cursor.execute(sql, val)
        result = cursor.fetchall()
        for time in result:
            sub_end_time = time[0]
        print(sub_end_time)
        #*********************************************************

        if sub_end_time < nowTime:
            markup = types.InlineKeyboardMarkup()
            bot.delete_message(message.chat.id, message.message_id)
            item_btn_subs = types.InlineKeyboardButton(text = 'Подписка', callback_data='sub')
            item_btn_back = types.InlineKeyboardButton(text='◀ Назад', callback_data='back')
            markup.add(item_btn_subs, item_btn_back)
            bot.send_message(message.chat.id, "Срок действия подписки истек. Оформи новую чтобы продолжить пользоваться услугами бота", reply_markup=markup)
        else:

            markup = types.InlineKeyboardMarkup()
            bot.delete_message(message.chat.id, message.message_id)
            item_btn_tablelist_dat = types.InlineKeyboardButton(text='💛 Сегодня', callback_data='now')
            item_btn_tablelist_tomorrow = types.InlineKeyboardButton(text='💚 Завтра', callback_data='twomorrow')
            item_btn_tablelist_week = types.InlineKeyboardButton(text='🧡 Неделя', callback_data='first_week')
            item_btn_back = types.InlineKeyboardButton(text='◀ Назад', callback_data='back')
            markup.add(item_btn_tablelist_dat, item_btn_tablelist_tomorrow, item_btn_tablelist_week, item_btn_back)
            #Получение наименования группы пользователя
            sql = "SELECT user_group FROM users WHERE userid=%s"
            val = (message.from_user.id, )
            cursor.execute(sql, val)
            groups = cursor.fetchall()
            for group in groups:
                userGroup = group[0]


            
            sql = 'SELECT * FROM tablelist WHERE group_name=%s'
            val = (userGroup, )
            cursor.execute(sql,val)
            test = cursor.fetchall()
            for testi in test:
                bot.send_message(message.chat.id, "Расписание группы " + testi[1] + " по 1 неделе:\n\n" + "🔸 Понедельник:\n" + testi[3] + "\n\n" + "🔸 Вторник:\n" + testi[4] + "\n\n" + "🔸 Среда:\n" +  testi[5] + "\n\n" + "🔸 Четверг:\n" +  testi[6] + "\n\n" + "🔸 Пятница:\n"+  testi[7], reply_markup=markup )
            #bot.delete_message(message.chat.id, message.message_id)
            cursor.close()
            db.close()
    except Exception as e:
        bot.reply_to(message, 'Error #33')
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#поиск Расписание на сегодня по 2 неделе
def process_tablelistdaylowweek_step(message):
    try:

        db = mysql.connector.connect(
        host=config.host,
        user=config.user,
        password=config.password,
        port=config.port,
        database=config.database
        )
        cursor = db.cursor()
        #Получение наименования группы пользователя
        sql = "SELECT user_group FROM users WHERE userid=%s"
        val = (message.from_user.id, )
        cursor.execute(sql, val)
        groups = cursor.fetchall()
        for group in groups:
            userGroup = group[0]


        #*********************************************************
        sql = "SELECT sub_end FROM users WHERE userid=%s"
        val = (message.from_user.id, )
        cursor.execute(sql, val)
        result = cursor.fetchall()
        for time in result:
            sub_end_time = time[0]
        print(sub_end_time)
        #*********************************************************

        if sub_end_time < nowTime:
            markup = types.InlineKeyboardMarkup()
            bot.delete_message(message.chat.id, message.message_id)
            item_btn_subs = types.InlineKeyboardButton(text = 'Подписка', callback_data='sub')
            item_btn_back = types.InlineKeyboardButton(text='◀ Назад', callback_data='back')
            markup.add(item_btn_subs, item_btn_back)
            bot.send_message(message.chat.id, "Срок действия подписки истек. Оформи новую чтобы продолжить пользоваться услугами бота", reply_markup=markup)
        else:
            markup = types.InlineKeyboardMarkup()
            bot.delete_message(message.chat.id, message.message_id)
            item_btn_tablelist_day = types.InlineKeyboardButton(text='💙 Сегодня', callback_data='now_two')
            item_btn_tablelist_tomorrow = types.InlineKeyboardButton(text='💜 Завтра', callback_data='twomorrow_two')
            item_btn_tablelist_week = types.InlineKeyboardButton(text='🖤 Неделя', callback_data='second_week')
            item_btn_back = types.InlineKeyboardButton(text='◀ Назад', callback_data='back')
            markup.add(item_btn_tablelist_day, item_btn_tablelist_tomorrow, item_btn_tablelist_week, item_btn_back)

            #Получение расписания пользователя по группе
            sql = 'SELECT * FROM tablelist WHERE group_name=%s'
            val = (userGroup, )
            cursor.execute(sql, val)
            lists = cursor.fetchall()
            for list in lists:
                if today == 0:
                    bot.send_message(message.chat.id, "Расписание группы " + list[1] + " на сегодня:\n\n" + list[8], reply_markup=markup)
                elif today == 1:
                    bot.send_message(message.chat.id, "Расписание группы " + list[1] + " на сегодня:\n\n" + list[9], reply_markup=markup)
                elif today == 2:
                    bot.send_message(message.chat.id, "Расписание группы " + list[1] + " на сегодня:\n\n" + list[10], reply_markup=markup)
                elif today == 3:
                    bot.send_message(message.chat.id, "Расписание группы " + list[1] + " на сегодня:\n\n" +  list[11], reply_markup=markup)
                elif today == 4:
                    bot.send_message(message.chat.id, "Расписание группы " + list[1] + " на сегодня:\n\n" + list[12], reply_markup=markup)
                elif today == 5:
                    bot.send_message(message.chat.id, "Сегодня у тебя выходой", reply_markup=markup)
                elif today == 6:
                    bot.send_message(message.chat.id, "Сегодня у тебя выходой", reply_markup=markup)
            cursor.close()
            db.close()
    except Exception as e:
        bot.reply_to(message, 'Error #4')
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#поиск Расписание на завтра по 2 неделе
def process_tablelisttomorrowlowweek_step(message):
    try:
        db = mysql.connector.connect(
        host=config.host,
        user=config.user,
        password=config.password,
        port=config.port,
        database=config.database
        )
        cursor = db.cursor()
        #Получение наименования группы пользователя
        sql = "SELECT user_group FROM users WHERE userid=%s"
        val = (message.from_user.id, )
        cursor.execute(sql, val)
        groups = cursor.fetchall()
        for group in groups:
            userGroup = group[0]

        #*********************************************************
        sql = "SELECT sub_end FROM users WHERE userid=%s"
        val = (message.from_user.id, )
        cursor.execute(sql, val)
        result = cursor.fetchall()
        for time in result:
            sub_end_time = time[0]
        print(sub_end_time)
        #*********************************************************

        if sub_end_time < nowTime:
            markup = types.InlineKeyboardMarkup()
            bot.delete_message(message.chat.id, message.message_id)
            item_btn_subs = types.InlineKeyboardButton(text = 'Подписка', callback_data='sub')
            item_btn_back = types.InlineKeyboardButton(text='◀ Назад', callback_data='back')
            markup.add(item_btn_subs, item_btn_back)
            bot.send_message(message.chat.id, "Срок действия подписки истек. Оформи новую чтобы продолжить пользоваться услугами бота", reply_markup=markup)
        else:

            markup = types.InlineKeyboardMarkup()
            bot.delete_message(message.chat.id, message.message_id)
            item_btn_tablelist_day = types.InlineKeyboardButton(text='💙 Сегодня', callback_data='now_two')
            item_btn_tablelist_tomorrow = types.InlineKeyboardButton(text='💜 Завтра', callback_data='twomorrow_two')
            item_btn_tablelist_week = types.InlineKeyboardButton(text='🖤 Неделя', callback_data='second_week')
            item_btn_back = types.InlineKeyboardButton(text='◀ Назад', callback_data='back')
            markup.add(item_btn_tablelist_day, item_btn_tablelist_tomorrow, item_btn_tablelist_week, item_btn_back)


            #Получение расписания пользователя по группе
            sql = 'SELECT * FROM tablelist WHERE group_name=%s'
            val = (userGroup, )
            cursor.execute(sql, val)
            lists = cursor.fetchall()
            for list in lists:
                if today == 0:
                    bot.send_message(message.chat.id, "Расписание группы " + list[1] + " на завтра:\n\n" + list[9], reply_markup=markup)
                elif today == 1:
                    bot.send_message(message.chat.id, "Расписание группы " + list[1] + " на завтра:\n\n" + list[10], reply_markup=markup)
                elif today == 2:
                    bot.send_message(message.chat.id, "Расписание группы " + list[1] + " на завтра:\n\n" + list[11], reply_markup=markup)
                elif today == 3:
                    bot.send_message(message.chat.id, "Расписание группы " + list[1] + " на завтра:\n\n" +  list[12], reply_markup=markup)
                elif today == 4:
                    bot.send_message(message.chat.id, "Завтра у тебя выходой", reply_markup=markup)
                elif today == 5:
                    bot.send_message(message.chat.id, "Завтра у тебя выходой", reply_markup=markup)
                elif today == 6:
                    bot.send_message(message.chat.id, "Расписание группы " + list[1] + " на завтра:\n\n" + list[8], reply_markup=markup)
            cursor.close()
            db.close()
    except Exception as e:
        bot.reply_to(message, 'Error #22234')
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#поиск Расписание на 2 неделю
def process_tablelistlowweek_step(message):
    try:
        db = mysql.connector.connect(
        host=config.host,
        user=config.user,
        password=config.password,
        port=config.port,
        database=config.database
        )
        cursor = db.cursor()
        #Получение наименования группы пользователя
        sql = "SELECT user_group FROM users WHERE userid=%s"
        val = (message.from_user.id, )
        cursor.execute(sql, val)
        groups = cursor.fetchall()
        for group in groups:
            userGroup = group[0]

        #*********************************************************
        sql = "SELECT sub_end FROM users WHERE userid=%s"
        val = (message.from_user.id, )
        cursor.execute(sql, val)
        result = cursor.fetchall()
        for time in result:
            sub_end_time = time[0]
        print(sub_end_time)
        #*********************************************************

        if sub_end_time < nowTime:
            markup = types.InlineKeyboardMarkup()
            bot.delete_message(message.chat.id, message.message_id)
            item_btn_subs = types.InlineKeyboardButton(text = 'Подписка', callback_data='sub')
            item_btn_back = types.InlineKeyboardButton(text='◀ Назад', callback_data='back')
            markup.add(item_btn_subs, item_btn_back)
            bot.send_message(message.chat.id, "Срок действия подписки истек. Оформи новую чтобы продолжить пользоваться услугами бота", reply_markup=markup)
        else:

            markup = types.InlineKeyboardMarkup()
            bot.delete_message(message.chat.id, message.message_id)
            item_btn_tablelist_day = types.InlineKeyboardButton(text='💙 Сегодня', callback_data='now_two')
            item_btn_tablelist_tomorrow = types.InlineKeyboardButton(text='💜 Завтра', callback_data='twomorrow_two')
            item_btn_tablelist_week = types.InlineKeyboardButton(text='🖤 Неделя', callback_data='second_week')
            item_btn_back = types.InlineKeyboardButton(text='◀ Назад', callback_data='back')
            markup.add(item_btn_tablelist_day, item_btn_tablelist_tomorrow, item_btn_tablelist_week, item_btn_back)
            
            sql = 'SELECT * FROM tablelist WHERE group_name=%s'
            val = (userGroup, )
            cursor.execute(sql,val)
            test = cursor.fetchall()
            for testi in test:
                bot.send_message(message.chat.id, "Расписание группы " + testi[1] + " по 1 неделе:\n\n" + "🔹 Понедельник:\n" + testi[8] + "\n\n" + "🔹 Вторник:\n" + testi[9] + "\n\n" + "🔹 Среда:\n" +  testi[10] + "\n\n" + "🔹 Четверг:\n" +  testi[11] + "\n\n" + "🔹 Пятница:\n"+  testi[12], reply_markup=markup)
            #bot.delete_message(message.chat.id, message.message_id)
            cursor.close()
            db.close()

    except Exception as e:
        bot.reply_to(message, 'Error #33')
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#Изменение группы
def process_changegroup_step(message):
    try:
        #Изменение группы
        sql = "UPDATE users SET user_group=%s WHERE userid={0}".format(message.from_user.id)
        val = (message.text, )
        cursor.execute(sql, val)
        db.commit()
        
        bot.send_message(message.chat.id, "Вы успешно изменили свою группу на " + message.text)
        markup = types.InlineKeyboardMarkup()
        item_btn_my_group = types.InlineKeyboardButton(text = '🔥 Моя', callback_data='my_group')
        item_btn_change_group = types.InlineKeyboardButton(text = 'Изменить', callback_data='change_group')
        item_btn_list_group = types.InlineKeyboardButton(text = '📌Список', callback_data='list_group')
        item_btn_back = types.InlineKeyboardButton(text = '◀ Назад', callback_data='back')
        markup.add(item_btn_my_group, item_btn_change_group, item_btn_list_group, item_btn_back)
        bot.send_message(message.chat.id, 'Для продолжения используй меню', reply_markup=markup)

    except Exception as e:
        bot.reply_to(message, 'Error #33')
#-------------------------------------------------------------------------------------------------------------------------------------------------------------




def days_to_seconds(days):
    return days * 24 * 60 * 60



# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)

