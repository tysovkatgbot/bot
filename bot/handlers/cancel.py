from datetime import datetime

from bot.config import TIMEZONE, CREATOR_ID, DEFAULT_MARKUP, CREATOR_MARKUP, END
from bot.msgs import msg_29, msg_30, msg_31, msg_32
from bot.sql.get import get_user, get_table, get_birthday, get_switched, get_prompted, get_ignored
from bot.sql.update import update_user, update_people
from bot.tools.chat_check import chat_check
from bot.tools.time_left import time_left


@chat_check('verified')
def cancel_msg(update, context):
    bot = context.bot
    user = update.effective_user
    user_id = user['id']
    db_user = get_user(user_id)
    step = db_user[9]
    markup = CREATOR_MARKUP if user_id == CREATOR_ID else DEFAULT_MARKUP
    if step in ['people', 'time', 'settings', 'holidays']:
        update_user('step', 'NULL', user_id)
        bot.send_message(user_id, msg_29, reply_markup=markup)
    elif step in ['on', 'off']:
        update_user('step', 'NULL', user_id)
        if get_table(user_id):
            birthday_list = [x[0] for x in get_birthday(TIMEZONE, user_id)]
            switched_list = get_switched(user_id, True)
            desired_list = list(set(birthday_list) & set(switched_list))
            if desired_list:
                ignored_list = get_ignored(user_id)
                refined_list = list(set(desired_list) - set(ignored_list))
                prompted_list = get_prompted(user_id)
                repeated_list = list(set(refined_list) & set(prompted_list))
                now = datetime.now(TIMEZONE)
                timesetting = db_user[8]
                timesetting_time = time_left(
                    now.replace(second=now.second+1 if now.second != 59 else 0, microsecond=0),
                    now.replace(hour=int(timesetting[:2]), minute=int(timesetting[-2:]), second=0,
                                microsecond=0))
                if step == 'on':
                    if repeated_list and timesetting_time:
                        for userid in repeated_list:
                            update_people(user_id, 'ignored', True, userid)
                        bot.send_message(user_id, msg_31, reply_markup=markup)
                    else:
                        bot.send_message(user_id, msg_32, reply_markup=markup)
                else:
                    if repeated_list and timesetting_time:
                        for userid in repeated_list:
                            update_people(user_id, 'ignored', False, userid)
                        msg = msg_30.format(a=timesetting_time)
                        bot.send_message(user_id, msg, reply_markup=markup)
                    else:
                        bot.send_message(user_id, msg_32, reply_markup=markup)
            else:
                bot.send_message(user_id, msg_32, reply_markup=markup)
        else:
            bot.send_message(user_id, msg_32, reply_markup=markup)
    else:
        bot.send_message(user_id, msg_32, reply_markup=markup)
    update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
    return END
