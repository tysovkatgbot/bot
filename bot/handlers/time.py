from datetime import datetime
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from bot.config import TIMEZONE, CREATOR_ID, DEFAULT_MARKUP, OPTIONS_MARKUP, TIME_ENTERED, \
                       TIME_REPEATED, CREATOR_MARKUP, END
from bot.handlers.scheduler import mention_layout
from bot.msgs import msg_7, msg_9, msg_19, msg_20, msg_21, msg_22, msg_23, msg_24, msg_25
from bot.msgs.emojis import emoji_10, emoji_13, emoji_21
from bot.sql.get import get_user, get_table, get_birthday, get_switched, get_prompted, get_ignored
from bot.sql.update import update_user, update_people
from bot.tools.chat_check import chat_check
from bot.tools.datetime_check import datetime_check
from bot.tools.time_emoji import time_emoji
from bot.tools.time_left import time_left


@chat_check('verified')
def time_msg(update, context):
    bot = context.bot
    user = update.effective_user
    user_id = user['id']
    db_user = get_user(user_id)
    step = db_user[9]
    if step != 'settings':
        substate = db_user[7]
        if substate:
            update_user('step', 'NULL', user_id)
            timesetting = db_user[8]
            if timesetting == '00:00':
                timesetting_type = msg_21.format(a=timesetting)
            else:
                timesetting_type = msg_22.format(a=timesetting)
            clock_emoji = time_emoji(timesetting)
            msg = msg_23.format(a=timesetting_type, b=clock_emoji)
            button = [[InlineKeyboardButton(text='изменить время', callback_data='t_btn')]]
            markup = InlineKeyboardMarkup(button)
            bot.send_message(user_id, msg, reply_markup=markup)
        else:
            update_user('step', "'time'", user_id)
            markup = CREATOR_MARKUP if user_id == CREATOR_ID else DEFAULT_MARKUP
            bot.send_message(user_id, msg_20, reply_markup=markup)
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
        return END


@chat_check('verified')
def time_cb(update, context):
    bot = context.bot
    user = update.effective_user
    user_id = user['id']
    query = update.callback_query
    query_data = query['data']
    db_user = get_user(user_id)
    substate = db_user[7]
    if substate:
        if query_data == 't_btn':
            update_user('step', 'NULL', user_id)
            step = db_user[9]
            if step == 'settings':
                markup = CREATOR_MARKUP if user_id == CREATOR_ID else DEFAULT_MARKUP
            else:
                markup = None
            bot.send_message(user_id, msg_19, reply_markup=markup)
            query.answer()
            update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
            return TIME_ENTERED
        else:
            query.answer()
            return None
    else:
        update_user('step', "'time'", user_id)
        markup = CREATOR_MARKUP if user_id == CREATOR_ID else DEFAULT_MARKUP
        bot.send_message(user_id, msg_20, reply_markup=markup)
        query.answer()
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
    return END


@chat_check('verified')
def enter_time(update, context):
    bot = context.bot
    bot_data = context.bot_data
    user = update.effective_user
    user_id = user['id']
    message = update.effective_message
    txt = message.text
    if datetime_check(txt, '%H:%M'):
        timesetting = f'{txt.zfill(5) if len(txt) == 4 else txt}'
        clock_emoji = time_emoji(timesetting)
        msg = msg_25.format(a=timesetting, b=clock_emoji)
        if get_table(user_id):
            switched_list = get_switched(user_id, True)
            if switched_list:
                if get_birthday(TIMEZONE, user_id):
                    birthday_list = [x[0] for x in get_birthday(TIMEZONE, user_id)]
                    desired_list = list(set(birthday_list) & set(switched_list))
                    ignored_list = get_ignored(user_id)
                    refined_list = list(set(desired_list) - set(ignored_list))
                    prompted_list = get_prompted(user_id)
                    repeated_list = list(set(refined_list) & set(prompted_list))
                    now = datetime.now(TIMEZONE)
                    timesetting_time = time_left(
                        now.replace(second=now.second+1 if now.second != 59 else 0, microsecond=0),
                        now.replace(hour=int(timesetting[:2]), minute=int(timesetting[-2:]),
                                    second=0, microsecond=0))
                    if repeated_list and timesetting_time:
                        update_user('step', "'time'", user_id)
                        bot_data[f'timesetting_{user_id}'] = timesetting
                        mentions, line, _ = mention_layout(user_id, repeated_list)
                        msg = msg_24.format(a=mentions, b=line, c=timesetting)
                        bot.send_message(user_id, msg, reply_markup=OPTIONS_MARKUP)
                        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
                        return TIME_REPEATED
                    else:
                        update_user('step', 'NULL', user_id)
                else:
                    update_user('step', 'NULL', user_id)
            else:
                update_user('step', 'NULL', user_id)
                msg += '\n' + f'не забудь определить свой *список людей* {emoji_21}'
        else:
            update_user('step', 'NULL', user_id)
            msg += '\n' + f'не забудь определить свой *список людей* {emoji_21}'
        update_user('timesetting', f"'{timesetting}'", user_id)
        markup = CREATOR_MARKUP if user_id == CREATOR_ID else DEFAULT_MARKUP
        bot.send_message(user_id, msg, reply_markup=markup)
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
    else:
        update_user('step', "'time'", user_id)
        markup = CREATOR_MARKUP if user_id == CREATOR_ID else DEFAULT_MARKUP
        bot.send_message(user_id, msg_9, reply_markup=markup)
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
        return TIME_ENTERED
    return END


@chat_check('verified')
def repeat_time(update, context):
    bot = context.bot
    bot_data = context.bot_data
    user = update.effective_user
    user_id = user['id']
    message = update.effective_message
    txt = message.text.lower()
    if txt in ['да', 'нет']:
        timesetting = bot_data[f'timesetting_{user_id}']
        bot_data.pop(f'timesetting_{user_id}')
        update_user('timesetting', f"'{timesetting}'", user_id)
        clock_emoji = time_emoji(timesetting)
        msg = msg_25.format(a=timesetting, b=clock_emoji)
        if get_table(user_id):
            switched_list = get_switched(user_id, True)
            if switched_list:
                if get_birthday(TIMEZONE, user_id):
                    birthday_list = [x[0] for x in get_birthday(TIMEZONE, user_id)]
                    desired_list = list(set(birthday_list) & set(switched_list))
                    ignored_list = get_ignored(user_id)
                    refined_list = list(set(desired_list) - set(ignored_list))
                    prompted_list = get_prompted(user_id)
                    repeated_list = list(set(refined_list) & set(prompted_list))
                    now = datetime.now(TIMEZONE)
                    timesetting_time = time_left(
                        now.replace(second=now.second+1 if now.second != 59 else 0, microsecond=0),
                        now.replace(hour=int(timesetting[:2]), minute=int(timesetting[-2:]),
                                    second=0, microsecond=0))
                    if repeated_list and timesetting_time:
                        if txt == 'да':
                            update_user('step', "'on'", user_id)
                            for userid in repeated_list:
                                update_people(user_id, 'ignored', False, userid)
                            line = f'ты получишь уведомление через *{timesetting_time}* {emoji_13}'
                            msg += '\n' + line
                        else:
                            update_user('step', "'off'", user_id)
                            for userid in repeated_list:
                                update_people(user_id, 'ignored', True, userid)
                            line = f'сегодня больше напоминать не буду {emoji_10}'
                            msg += '\n' + line
                    else:
                        update_user('step', 'NULL', user_id)
                else:
                    update_user('step', 'NULL', user_id)
            else:
                update_user('step', 'NULL', user_id)
                msg += '\n' + f'не забудь определить свой *список людей* {emoji_21}'
        else:
            update_user('step', 'NULL', user_id)
            msg += '\n' + f'не забудь определить свой *список людей* {emoji_21}'
        markup = CREATOR_MARKUP if user_id == CREATOR_ID else DEFAULT_MARKUP
        bot.send_message(user_id, msg, reply_markup=markup)
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
    else:
        update_user('step', "'time'", user_id)
        bot.send_message(user_id, msg_7, reply_markup=OPTIONS_MARKUP)
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
        return TIME_REPEATED
    return END
