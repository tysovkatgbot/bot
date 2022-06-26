from datetime import datetime, timedelta
from telegram.error import TelegramError
from telegram.utils.helpers import mention_markdown

from bot.config import LOGGER, TIMEZONE, DEFAULT_TIMESETTING, TYSOVKA_ID
from bot.msgs import msg_1, msg_11, msg_14
from bot.msgs.emojis import greeting_emoji, birthday_emoji
from bot.sql.get import get_users, get_user, get_table, get_birthday, get_every, get_switched, \
                        get_prompted, get_ignored, get_holidays
from bot.sql.update import update_user, update_people, update_years, update_holidays
from bot.tools.list_join import list_join
from bot.tools.string_escape import string_escape


def mention_layout(user_id, dsr_list):
    birthday_rows = get_birthday(TIMEZONE, user_id)
    mention_list = []
    for row in birthday_rows:
        userid = row[0]
        if userid in dsr_list:
            username = row[1]
            mention = mention_markdown(userid, username, version=2)
            mention_list.append(mention)
            update_years(user_id, userid)
    if len(birthday_rows) == 1:
        userid = birthday_rows[0][0]
        gender = birthday_rows[0][2]
        age_subquery = f"date_part('years', age(current_date, " \
                       f"(SELECT birthday FROM users WHERE userid = {userid})))"
        update_user('age', age_subquery, userid)
        age = get_user(userid)[4]
        line = string_escape('празднует своё {0}-летие'.format(age), '-')
        pronoun = 'его' if gender == 'm' else 'её'
    else:
        line = 'празднуют свои дни рождения'
        pronoun = 'их'
    mentions = list_join(mention_list)
    return mentions, line, pronoun


def group_msgs(context):
    bot = context.bot
    now = datetime.now(TIMEZONE)
    if now.strftime('%H:%M') == DEFAULT_TIMESETTING:
        holidays_rows = get_holidays()
        if holidays_rows and all(holidays_rows):
            data, latest = holidays_rows
            for date, txt in list(data.items()):
                date_today = now.strftime('%d.%m')
                current_year = int(now.strftime('%Y'))
                datetime_date = datetime(current_year, int(date[-2:]),
                                         int(date[:2]))
                datetime_shifted = datetime_date + timedelta(days=1)
                date_shifted = datetime_shifted.strftime('%d.%m')
                if date_today == date:
                    try:
                        bot_msg = bot.send_message(TYSOVKA_ID, txt)
                        bot_msg_id = bot_msg['message_id']
                        update_holidays('latest', bot_msg_id)
                        bot.pin_chat_message(TYSOVKA_ID, bot_msg_id)
                    except (Exception, TelegramError) as error:
                        LOGGER.info(error)
                elif date_today == date_shifted:
                    try:
                        bot.unpin_chat_message(TYSOVKA_ID, latest)
                    except (Exception, TelegramError) as error:
                        LOGGER.info(error)
        else:
            return None
    else:
        return None


def scheduler(context):
    bot = context.bot
    group_msgs(context)
    users_rows = get_users()
    for row in users_rows:
        user_id = row[0]
        username = row[1]
        substate = row[7]
        now = datetime.now(TIMEZONE)
        if substate:
            latest = row[11]
            minutes = int((now-latest).total_seconds() / 60)
            if get_table(user_id):
                birthday_list = [x[0] for x in get_birthday(TIMEZONE, user_id)]
                switched_list = get_switched(user_id, True)
                desired_list = list(set(birthday_list) & set(switched_list))
                if desired_list:
                    timesetting = row[8]
                    ignored_list = get_ignored(user_id)
                    refined_list = list(set(desired_list) - set(ignored_list))
                    if now.strftime('%H:%M') == timesetting and refined_list:
                        update_user('step', "'birthday'", user_id)
                        greeting = msg_1.format(a=f', *{username}*', b=greeting_emoji()) + '\n'
                        prompted_list = get_prompted(user_id)
                        repeated_list = list(set(refined_list) & set(prompted_list))
                        mentions, line, pronoun = mention_layout(user_id, desired_list)
                        msg = f"{greeting if minutes >= 60 else ''}" + \
                            f"{'напоминаю, что ' if repeated_list else ''}" + msg_11.format(
                                a=mentions, b=line, c=pronoun, d=birthday_emoji())
                        bot.send_message(user_id, msg)
                        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
                        if repeated_list:
                            for userid in repeated_list:
                                update_people(user_id, 'ignored', False, userid)
                if now.strftime('%H:%M') == DEFAULT_TIMESETTING:
                    age_subquery = f"date_part('years', age(current_date, " \
                                f"(SELECT birthday FROM users WHERE userid = {user_id})))"
                    update_user('age', age_subquery, user_id)
                    every_list = get_every(user_id)
                    if every_list:
                        for userid in every_list:
                            update_people(user_id, 'ignored', False, userid)
            if minutes == 5:
                if len(users_rows) > 1:
                    if not get_table(user_id):
                        bot.send_message(user_id, msg_14)
                    elif not get_switched(user_id, True):
                        bot.send_message(user_id, msg_14)
