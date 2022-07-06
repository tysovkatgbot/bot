from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from bot.config import CREATOR_ID, DEFAULT_MARKUP, CREATOR_MARKUP, GENDER_SETTINGS_MARKUP, \
                       SETTINGS_MARKUP, USERNAME_STORED, GENDER_STORED, BIRTHDAY_STORED, \
                       SETTING_CHOSEN, END
from bot.msgs import msg_3, msg_6, msg_7, msg_8, msg_36, msg_37
from bot.msgs.emojis import emoji_54
from bot.sql.get import get_user
from bot.sql.update import update_user
from bot.tools.chat_check import chat_check
from bot.tools.string_escape import string_escape


@chat_check('verified')
def settings_msg(update, context):
    bot = context.bot
    user = update.effective_user
    user_id = user['id']
    db_user = get_user(user_id)
    step = db_user[9]
    if step != 'settings':
        username, gender, birthday, substate = db_user[1], db_user[2], db_user[3], db_user[7]
        if substate:
            if all([username, gender, birthday]):
                update_user('step', 'NULL', user_id)
                gender = 'мужской' if gender == 'm' else 'женский'
                birthday = birthday.strftime('%d.%m.%Y')
                msg = f'*настройки* {emoji_54}\n\n' \
                      f'— имя: *{username}*\n' \
                      f'— пол: *{gender}*\n' \
                      f'— дата рождения: *{birthday}*'
                button = [[InlineKeyboardButton(text='изменить настройки', callback_data='s_btn')]]
                markup = InlineKeyboardMarkup(button)
                bot.send_message(user_id, string_escape(msg, '.'), reply_markup=markup)
            elif not username:
                bot.send_message(user_id, msg_3, reply_markup=SETTINGS_MARKUP)
                return USERNAME_STORED
            elif not gender:
                bot.send_message(user_id, msg_6, reply_markup=GENDER_SETTINGS_MARKUP)
                return GENDER_STORED
            elif not birthday:
                bot.send_message(user_id, msg_8, reply_markup=SETTINGS_MARKUP)
                return BIRTHDAY_STORED
        else:
            update_user('step', "'settings'", user_id)
            markup = CREATOR_MARKUP if user_id == CREATOR_ID else DEFAULT_MARKUP
            bot.send_message(user_id, msg_36, reply_markup=markup)
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
        return END


@chat_check('verified')
def settings_cb(update, context):
    bot = context.bot
    user = update.effective_user
    user_id = user['id']
    query = update.callback_query
    query_data = query['data']
    db_user = get_user(user_id)
    substate = db_user[7]
    if substate:
        if query_data == 's_btn':
            update_user('step', "'settings'", user_id)
            bot.send_message(user_id, msg_37, reply_markup=SETTINGS_MARKUP)
            query.answer()
            update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
            return SETTING_CHOSEN
        else:
            query.answer()
            return None
    else:
        update_user('step', "'settings'", user_id)
        markup = CREATOR_MARKUP if user_id == CREATOR_ID else DEFAULT_MARKUP
        bot.send_message(user_id, msg_36, reply_markup=markup)
        query.answer()
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
    return END


def choose_setting(update, context):
    bot = context.bot
    user = update.effective_user
    user_id = user['id']
    message = update.effective_message
    txt = message.text.lower()
    update_user('step', "'settings'", user_id)
    if txt == 'имя':
        bot.send_message(user_id, msg_3, reply_markup=SETTINGS_MARKUP)
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
        return USERNAME_STORED
    elif txt == 'пол':
        bot.send_message(user_id, msg_6, reply_markup=GENDER_SETTINGS_MARKUP)
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
        return GENDER_STORED
    elif txt == 'дата рождения':
        bot.send_message(user_id, msg_8, reply_markup=SETTINGS_MARKUP)
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
        return BIRTHDAY_STORED
    else:
        bot.send_message(user_id, msg_7, reply_markup=SETTINGS_MARKUP)
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
        return SETTING_CHOSEN
    return END
