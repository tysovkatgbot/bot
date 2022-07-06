from bot.config import CREATOR_ID, DEFAULT_MARKUP, CREATOR_MARKUP, GENDER_START_MARKUP, \
                       USERNAME_STORED, GENDER_STORED, BIRTHDAY_STORED, END
from bot.msgs import msg_3, msg_6, msg_8, msg_16, msg_17
from bot.sql.get import get_user
from bot.sql.update import update_user
from bot.tools.chat_check import chat_check
from bot.tools.word_form import word_form


@chat_check('registered')
def sub_msg(update, context):
    bot = context.bot
    user = update.effective_user
    user_id = user['id']
    db_user = get_user(user_id)
    step = db_user[9]
    if step != 'settings':
        username, gender, birthday = db_user[1], db_user[2], db_user[3]
        if not all([username, gender, birthday]):
            update_user('step', "'sub'", user_id)
            if not username:
                bot.send_message(user_id, msg_3)
                return USERNAME_STORED
            elif not gender:
                bot.send_message(user_id, msg_6, reply_markup=GENDER_START_MARKUP)
                return GENDER_STORED
            elif not birthday:
                bot.send_message(user_id, msg_8)
                return BIRTHDAY_STORED
        else:
            substate, step = db_user[7], db_user[9]
            update_user('substate', True, user_id)
            if not substate and step == 'people':
                import bot.handlers.people as people
                people.people_msg(update, context)
            elif not substate and step == 'time':
                import bot.handlers.time as time
                time.time_msg(update, context)
            elif not substate and step == 'settings':
                import bot.handlers.settings as settings
                settings.settings_msg(update, context)
            elif not substate and step == 'holidays':
                import bot.handlers.holidays as holidays
                holidays.holidays_msg(update, context)
            else:
                update_user('step', 'NULL', user_id)
                word = word_form('подписан', gender)
                substate = db_user[7]
                if substate:
                    msg = msg_17.format(a=word)
                else:
                    verified, timesetting = db_user[6], db_user[8]
                    if not verified:
                        update_user('verified', True, user_id)
                    msg = msg_16.format(a=word, b=timesetting)
                markup = CREATOR_MARKUP if user_id == CREATOR_ID else DEFAULT_MARKUP
                bot.send_message(user_id, msg, reply_markup=markup)
                update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
        return END
