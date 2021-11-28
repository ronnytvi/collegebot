from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

markup_main = InlineKeyboardMarkup(row_width=2)
item_btn_tablelist = InlineKeyboardButton(text = 'Расписание', callback_data='callsTablelist')
item_btn_option = InlineKeyboardButton(text = '⚙ Опции', callback_data='callsOption')
item_btn_subs = InlineKeyboardButton(text = 'Подписка', callback_data='callsSubmonth')
item_btn_about_bot = InlineKeyboardButton(text = '🌍 Что это?', callback_data='callsAboutBot')
markup_main.insert(item_btn_tablelist)
markup_main.insert(item_btn_option)