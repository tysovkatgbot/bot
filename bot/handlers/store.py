import re

from datetime import datetime
from dateutil.relativedelta import relativedelta

from bot.config import TIMEZONE, CREATOR_ID, DEFAULT_MARKUP, CREATOR_MARKUP, GENDER_START_MARKUP, \
                       GENDER_SETTINGS_MARKUP, SETTINGS_MARKUP, USERNAME_STORED, GENDER_STORED, \
                       BIRTHDAY_STORED, SETTING_CHOSEN, END
from bot.handlers.settings import settings_msg
from bot.handlers.sub import sub_msg
from bot.msgs import msg_3, msg_4, msg_5, msg_6, msg_7, msg_8, msg_9, msg_10, msg_37
from bot.sql.get import get_users, get_user
from bot.sql.update import update_user
from bot.tools.chat_check import chat_check
from bot.tools.datetime_check import datetime_check
from bot.tools.string_escape import string_escape
from bot.tools.word_shorten import word_shorten


@chat_check('registered')
def store_username(update, context):
    bot = context.bot
    user = update.effective_user
    user_id = user['id']
    message = update.effective_message
    txt = message.text.lower()
    username = txt.title()
    db_user = get_user(user_id)
    step = db_user[9]
    usernames = {row[1]: row[0] for row in get_users() if row[1]}
    if step == 'settings' and txt == 'имя':
        bot.send_message(user_id, msg_3)
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
        return USERNAME_STORED
    elif step == 'settings' and txt == 'пол':
        bot.send_message(user_id, msg_6, reply_markup=GENDER_SETTINGS_MARKUP)
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
        return GENDER_STORED
    elif step == 'settings' and txt == 'дата рождения':
        bot.send_message(user_id, msg_8)
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
        return BIRTHDAY_STORED
    elif username in list(usernames.keys()) and usernames[username] != user_id:
        msg = msg_4.format(a=string_escape(username, '.'))
        bot.send_message(user_id, msg)
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
        return USERNAME_STORED
    elif all([re.compile(r'^[а-яА-Я]+$').findall(x) or
              re.compile(r'^[А-ЩЬЮЯҐЄІЇа-щьюяґєії]+$').findall(x) or
              re.compile(r'^[a-zA-Z]+$').findall(x) for x in username.split(' ')]):
        if len(username) > 12:
            username_split = username.split(' ')
            if len(username_split) > 1:
                main = username_split[0]
                initials = username_split[1:]
                max_main_length = 12 - len(initials) * 3
                if len(main) > max_main_length:
                    main = word_shorten(main[:max_main_length]) + '.'
                username = main + ' ' + ' '.join([x[0] + '.' for x in initials])
            else:
                username = word_shorten(username[:11]) + '.'
        gender, birthday = db_user[2], db_user[3]
        update_user('username', f"'{username}'", user_id)
        if not gender:
            msg = msg_10.format(a=string_escape(username, '.')) + '\nтеперь ' + msg_6
            markup = GENDER_START_MARKUP if step == 'sub' else GENDER_SETTINGS_MARKUP
            bot.send_message(user_id, msg, reply_markup=markup)
            update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
            return GENDER_STORED
        elif not birthday:
            msg = msg_10.format(a=string_escape(username, '.')) + '\nтеперь ' + msg_8
            bot.send_message(user_id, msg)
            update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
            return BIRTHDAY_STORED
        else:
            update_user('step', 'NULL', user_id)
            msg = msg_10.format(a=string_escape(username, '.'))
            markup = CREATOR_MARKUP if user_id == CREATOR_ID else DEFAULT_MARKUP
            bot.send_message(user_id, msg, reply_markup=markup)
            update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
            if step == 'sub':
                sub_msg(update, context)
            elif step == 'settings':
                settings_msg(update, context)
    else:
        bot.send_message(user_id, msg_5)
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
        return USERNAME_STORED
    return END


@chat_check('registered')
def store_gender(update, context):
    bot = context.bot
    user = update.effective_user
    user_id = user['id']
    message = update.effective_message
    txt = message.text.lower()
    db_user = get_user(user_id)
    step = db_user[9]
    if txt in ['мужской', 'женский']:
        username, birthday = db_user[1], db_user[3]
        update_user('gender', f"'{'m' if txt == 'мужской' else 'f'}'", user_id)
        if not username:
            msg = msg_10.format(a=txt) + '\nтеперь скажи, ' + msg_3
            bot.send_message(user_id, msg)
            update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
            return USERNAME_STORED
        elif not birthday:
            msg = msg_10.format(a=txt) + '\nтеперь ' + msg_8
            bot.send_message(user_id, msg)
            update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
            return BIRTHDAY_STORED
        else:
            update_user('step', 'NULL', user_id)
            msg = msg_10.format(a=txt)
            markup = CREATOR_MARKUP if user_id == CREATOR_ID else DEFAULT_MARKUP
            bot.send_message(user_id, msg, reply_markup=markup)
            update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
            if step == 'sub':
                sub_msg(update, context)
            elif step == 'settings':
                settings_msg(update, context)
    elif txt == 'назад':
        update_user('step', "'settings'", user_id)
        bot.send_message(user_id, msg_37, reply_markup=SETTINGS_MARKUP)
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
        return SETTING_CHOSEN
    else:
        markup = GENDER_START_MARKUP if step == 'sub' else GENDER_SETTINGS_MARKUP
        bot.send_message(user_id, msg_7, reply_markup=markup)
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
        return GENDER_STORED
    return END


@chat_check('registered')
def store_birthday(update, context):
    bot = context.bot
    user = update.effective_user
    user_id = user['id']
    message = update.effective_message
    txt = message.text.lower()
    db_user = get_user(user_id)
    step = db_user[9]
    if step == 'settings' and txt == 'имя':
        bot.send_message(user_id, msg_3)
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
        return USERNAME_STORED
    elif step == 'settings' and txt == 'пол':
        bot.send_message(user_id, msg_6, reply_markup=GENDER_SETTINGS_MARKUP)
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
        return GENDER_STORED
    elif step == 'settings' and txt == 'дата рождения':
        bot.send_message(user_id, msg_8)
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
        return BIRTHDAY_STORED
    elif datetime_check(txt, '%d.%m.%Y'):
        now = datetime.now(TIMEZONE)
        birthday = datetime.strptime(txt, '%d.%m.%Y').replace(tzinfo=TIMEZONE)
        if 16 <= relativedelta(now, birthday).years <= 120:
            username, gender = db_user[1], db_user[2]
            update_user('birthday', f"'{birthday.strftime('%Y-%m-%d')}'", user_id)
            if not username:
                msg = msg_10.format(a=string_escape(txt.title(), '.')) + '\nтеперь скажи, ' + msg_3
                bot.send_message(user_id, msg)
                update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
                return USERNAME_STORED
            elif not gender:
                msg = msg_10.format(a=string_escape(txt.title(), '.')) + '\nтеперь ' + msg_6
                markup = GENDER_START_MARKUP if step == 'sub' else GENDER_SETTINGS_MARKUP
                bot.send_message(user_id, msg, reply_markup=markup)
                update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
                return GENDER_STORED
            else:
                update_user('step', 'NULL', user_id)
                msg = msg_10.format(a=string_escape(txt.title(), '.'))
                markup = CREATOR_MARKUP if user_id == CREATOR_ID else DEFAULT_MARKUP
                bot.send_message(user_id, msg, reply_markup=markup)
                update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
                if step == 'sub':
                    sub_msg(update, context)
                elif step == 'settings':
                    settings_msg(update, context)
        else:
            bot.send_message(user_id, msg_9)
            update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
            return BIRTHDAY_STORED
    else:
        bot.send_message(user_id, msg_9)
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
        return BIRTHDAY_STORED
    return END
