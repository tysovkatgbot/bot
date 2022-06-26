from datetime import datetime

from bot.config import TIMEZONE, CREATOR_ID, CREATOR_USERNAME, SUB_MARKUP, DEFAULT_MARKUP, \
                       CREATOR_MARKUP, GENDER_START_MARKUP, USERNAME_STORED, GENDER_STORED, \
                       BIRTHDAY_STORED, END
from bot.msgs import msg_1, msg_2, msg_3, msg_6, msg_8
from bot.msgs.emojis import emoji_5, emoji_9, greeting_emoji
from bot.sql.get import get_user
from bot.sql.update import update_user
from bot.tools.chat_check import chat_check
from bot.tools.string_escape import string_escape
from bot.tools.version_get import version_get


@chat_check('exists')
def start_msg(update, context):
    bot = context.bot
    user = update.effective_user
    user_id = user['id']
    db_user = get_user(user_id)
    username, step = db_user[1], db_user[9]
    if step == 'sub':
        gender, birthday = db_user[2], db_user[3]
        if not username:
            bot.send_message(user_id, msg_3)
            return USERNAME_STORED
        elif not gender:
            bot.send_message(user_id, msg_6, reply_markup=GENDER_START_MARKUP)
            return GENDER_STORED
        elif not birthday:
            bot.send_message(user_id, msg_8)
            return BIRTHDAY_STORED
    update_user('step', 'NULL', user_id)
    registered, verified = db_user[5], db_user[6]
    line = string_escape(f'я — *бот тусовки!* {emoji_5}\n', '!')
    version = version_get()
    introduction = msg_2.format(a=line, b='тебе', c='твоих', d=CREATOR_USERNAME,
                                e=f'\nверсия {version} {emoji_9}' if version else '')
    if registered:
        now = datetime.now(TIMEZONE)
        latest = db_user[11]
        minutes = int((now-latest).total_seconds() / 60)
        if minutes >= 60:
            greeting = msg_1.format(a=f', *{username}*', b=greeting_emoji()) + '\n'
            introduction = greeting + introduction
    else:
        update_user('registered', "'now()'::TIMESTAMPTZ", user_id)
        greeting = msg_1.format(a='', b=greeting_emoji()) + '\n'
        introduction = greeting + introduction
    if verified:
        markup = CREATOR_MARKUP if user_id == CREATOR_ID else DEFAULT_MARKUP
        bot.send_message(user_id, introduction, reply_markup=markup)
    else:
        bot.send_message(user_id, introduction, reply_markup=SUB_MARKUP)
    update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
    return END
