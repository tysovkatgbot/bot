from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from bot.config import CREATOR_MARKUP, HOLIDAY_ADDED, END
from bot.msgs import msg_9, msg_37, msg_38, msg_39, msg_40
from bot.msgs.emojis import holidays_emoji, emoji_17
from bot.sql.get import get_holidays
from bot.sql.get import get_user
from bot.sql.insert import insert_holiday
from bot.sql.update import update_holidays
from bot.sql.update import update_user
from bot.tools.chat_check import chat_check
from bot.tools.datetime_check import datetime_check
from bot.tools.string_escape import string_escape
from bot.tools.list_join import list_join


def holidays_layout(data):
    holidays = []
    for date, text in list(data.items()):
        chars = '[]()>#+-=|{}.!'
        date = string_escape(date, chars)
        text = string_escape(text, chars)
        holidays.append(f'— {date}: {text}')
    holidays = '\n'.join(holidays)
    out = f'*праздники* {holidays_emoji()}\n\n{holidays}'
    return out


@chat_check('creator')
def holidays_msg(update, context):
    bot = context.bot
    user = update.effective_user
    user_id = user['id']
    db_user = get_user(user_id)
    step = db_user[9]
    if step != 'settings':
        substate = db_user[7]
        if substate:
            update_user('step', 'NULL', user_id)
            holidays_rows = get_holidays()
            if holidays_rows:
                if holidays_rows[0]:
                    msg = holidays_layout(holidays_rows[0])
                    button_text = 'изменить праздники'
                else:
                    msg = msg_39
                    button_text = 'добавить праздники'
            else:
                msg = msg_39
                button_text = 'добавить праздники'
            button = [[InlineKeyboardButton(text=button_text, callback_data='h_btn')]]
            markup = InlineKeyboardMarkup(button)
            bot.send_message(user_id, msg, reply_markup=markup)
        else:
            update_user('step', "'holidays'", user_id)
            bot.send_message(user_id, msg_37, reply_markup=CREATOR_MARKUP)
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
        return END


@chat_check('creator')
def holidays_cb(update, context):
    bot = context.bot
    user = update.effective_user
    user_id = user['id']
    query = update.callback_query
    data = query['data']
    db_user = get_user(user_id)
    substate = db_user[7]
    if substate:
        if data == 'h_btn':
            update_user('step', "'holidays'", user_id)
            bot.send_message(user_id, msg_38, reply_markup=CREATOR_MARKUP)
            query.answer()
            update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
            return HOLIDAY_ADDED
        else:
            query.answer()
            return None
    else:
        update_user('step', "'holidays'", user_id)
        bot.send_message(user_id, msg_37, reply_markup=CREATOR_MARKUP)
        query.answer()
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
    return END


def process_holidays(update, context):
    bot = context.bot
    user = update.effective_user
    user_id = user['id']
    message = update.effective_message
    txt = message.text
    holidays_rows = get_holidays()
    vals = [x.split(', ', 1) for x in txt.split('\n')]
    if len(vals[0]) in [1, 2] and len(set(([len(x) for x in vals]))) == 1:
        if len(vals[0]) == 2:
            keys = [x[0] for x in vals]
            seen_keys, dupl_keys = {}, []
            for x in keys:
                if x not in seen_keys:
                    seen_keys[x] = 1
                else:
                    if seen_keys[x] == 1:
                        dupl_keys.append(x)
                    seen_keys[x] += 1
            dupl_keys_vals = [x[1] for x in vals if x[0] in set(dupl_keys)]
            if all([datetime_check(x[0], '%d.%m') for x in vals]) and len(set(dupl_keys_vals)) < 2:
                vals = [[x[0], string_escape(x[1], '\'"\\')] for x in vals]
                if holidays_rows:
                    data_subquery = 'data'
                    for x in vals:
                        date, text = x
                        data_subquery += f""" || '{{"{date}":"{text}"}}'::jsonb"""
                    update_holidays('data', data_subquery)
                    holidays_msg(update, context)
                else:
                    data_list = []
                    for x in vals:
                        date, text = x
                        data_list.append(f'"{date}": "{text}"')
                    data_string = ', '.join(data_list)
                    data_subquery = f"""('{{{data_string}}}'::jsonb)"""
                    inserted = insert_holiday('data', data_subquery)
                    if inserted:
                        holidays_msg(update, context)
                    else:
                        bot.send_message(user_id, msg_40, reply_markup=CREATOR_MARKUP)
                        return HOLIDAY_ADDED
            else:
                bot.send_message(user_id, msg_9, reply_markup=CREATOR_MARKUP)
                return HOLIDAY_ADDED
        else:
            if all([datetime_check(x[0], '%d.%m') for x in vals]):
                data_subquery = 'data'
                data = holidays_rows[0] if holidays_rows else {}
                absent = [x[0] for x in vals if x[0] not in list(data.keys())]
                if not absent:
                    for x in vals:
                        date = x[0]
                        data_subquery += f" - '{date}'"
                else:
                    absent = [f'*{x}*' for x in absent]
                    absent = list_join(absent)
                    if len(absent) > 1:
                        msg = f'праздники {absent} не существуют {emoji_17}'
                    else:
                        msg = f'праздник {absent} не существуeт {emoji_17}'
                    bot.send_message(user_id, msg, reply_markup=CREATOR_MARKUP)
                    return HOLIDAY_ADDED
                update_holidays('data', data_subquery)
                holidays_msg(update, context)
            else:
                bot.send_message(user_id, msg_9, reply_markup=CREATOR_MARKUP)
                return HOLIDAY_ADDED
    else:
        bot.send_message(user_id, msg_9, reply_markup=CREATOR_MARKUP)
        return HOLIDAY_ADDED
    update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
    return END
