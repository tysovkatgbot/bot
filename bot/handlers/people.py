from datetime import datetime, date
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import MAX_ANSWER_CALLBACK_QUERY_TEXT_LENGTH

from bot.config import TIMEZONE, CREATOR_ID, DEFAULT_MARKUP, CREATOR_MARKUP, END
from bot.msgs import msg_12, msg_13, msg_27, msg_28, msg_29
from bot.sql.get import get_users, get_user, get_people, get_every, get_switched
from bot.sql.update import update_user, update_switchstate, update_global_switchstate
from bot.tools.chat_check import chat_check
from bot.tools.date_convert import date_convert
from bot.tools.list_join import list_join
from bot.tools.list_sort import list_sort
from bot.tools.time_left import time_left


def people_birthdays(user_id, userid=None):
    userid_list = [row[0] for row in get_people(user_id)]
    desired_list = {row[0]: [row[1], row[3]] for row in get_users()
                    if row[0] != user_id and row[0] in userid_list}
    now = datetime.now(TIMEZONE)
    date_today = date.today()
    current_year = date_today.year
    age_subquery = "date_part('years', age(current_date, " \
                   "(SELECT birthday FROM users WHERE userid = {0})))"
    if userid:
        age = get_user(userid)[4]
        username, birthday = desired_list[userid]
        update_user('age', age_subquery.format(userid), userid)
        birthday = birthday.replace(
            year=current_year+1
            if (birthday.replace(year=current_year)-date_today).total_seconds() < 0
            else current_year)
        birthday_time = time_left(now, now.replace(
            year=birthday.year, month=birthday.month, day=birthday.day,
            hour=0, minute=0, second=0, microsecond=0))
        if birthday_time:
            line = 'будет праздновать своё {0}-летие'.format(int(age) + 1)
            msg = msg_12.format(a=username, b=line, c=birthday_time)
        else:
            line = 'празднует своё {0}-летие'.format(int(age) + 1)
            msg = msg_13.format(a=username, b=line)
    else:
        birthdays = [(x[0], [x[1][0], x[1][1].replace(
                        year=current_year+1
                        if (x[1][1].replace(year=current_year)-date_today).total_seconds() < 0
                        else current_year)])
                     for x in list(desired_list.items())]
        birthdays_sorted = sorted(birthdays, key=lambda x: abs(x[1][1] - date_today))
        closest = []
        for x in birthdays_sorted:
            if not closest or closest[-1][1][1] == x[1][1]:
                closest.append(x)
        birthday = closest[0][1][1]
        birthday_time = time_left(now, now.replace(
            year=birthday.year, month=birthday.month, day=birthday.day,
            hour=0, minute=0, second=0, microsecond=0))
        if birthday_time:
            if len(closest) == 1:
                userid = closest[0][0]
                age = get_user(userid)[4]
                update_user('age', age_subquery.format(userid), userid)
                line = 'будет праздновать своё {0}-летие'.format(int(age) + 1)
            else:
                line = 'будут праздновать свои дни рождения'
            msg_len = len(msg_12.format(a='', b=line, c=birthday_time))
            usernames = list_join(sorted([x[1][0] for x in closest]),
                                  MAX_ANSWER_CALLBACK_QUERY_TEXT_LENGTH - msg_len)
            msg = msg_12.format(a=usernames, b=line, c=birthday_time)
        else:
            if len(closest) == 1:
                userid = closest[0][0]
                age = get_user(userid)[4]
                update_user('age', age_subquery.format(userid), userid)
                line = 'празднует своё {0}-летие'.format(int(age) + 1)
            else:
                line = 'празднуют свои дни рождения'
            msg_len = len(msg_13.format(a='', b=line))
            usernames = list_join(sorted([x[1][0] for x in closest]),
                                  MAX_ANSWER_CALLBACK_QUERY_TEXT_LENGTH - msg_len)
            msg = msg_13.format(a=usernames, b=line)
    return msg


def people_markup(user_id, page_type, page_num):
    people_rows = get_people(user_id)
    people, usernames = [], []
    for row in people_rows:
        userid = row[0]
        db_user = get_user(userid)
        username = db_user[1]
        usernames.append(username)
        if page_type == 's':
            switchstate = row[1]
            toggle = 'включено' if switchstate else 'выключено'
            ppl_btns = [
                InlineKeyboardButton(text=username, callback_data=f's_ttl_btn_{userid}'),
                InlineKeyboardButton(text=toggle, callback_data=f's_tgl_btn_{userid}')
            ]
        else:
            birthday = db_user[3]
            birthday = date_convert(birthday)
            ppl_btns = [
                InlineKeyboardButton(text=username, callback_data=f'd_ttl_btn_{userid}'),
                InlineKeyboardButton(text=birthday, callback_data=f'd_tgl_btn_{userid}')
            ]
        people.append(ppl_btns)
    pages = list_sort(people, usernames)
    entries = [pages[x:x + 5] for x in range(0, len(pages), 5)][page_num]
    nav_btns = [InlineKeyboardButton(text='<', callback_data='p_btn'),
                InlineKeyboardButton(text='>', callback_data='n_btn')]
    if page_type == 's':
        switched_len = len(get_switched(user_id, True))
        non_switched_len = len(get_switched(user_id, False))
        mass_tgl = 'выключить всё' if switched_len >= non_switched_len else 'включить всё'
        g_btn = [InlineKeyboardButton(text=mass_tgl, callback_data='g_btn')]
        d_btn = [InlineKeyboardButton(text='даты', callback_data='d_btn')]
        controls = [g_btn, d_btn]
    else:
        c_btn = [InlineKeyboardButton(text='ближайший', callback_data='c_btn')]
        b_btn = [InlineKeyboardButton(text='назад', callback_data='b_btn')]
        controls = [c_btn, b_btn]
    if len(pages) > 5:
        entries.append(nav_btns)
    entries += controls
    markup = InlineKeyboardMarkup(entries)
    return markup


@chat_check('verified')
def people_msg(update, context):
    user = update.effective_user
    user_id = user['id']
    bot = context.bot
    db_user = get_user(user_id)
    step = db_user[9]
    if step != 'settings':
        substate = db_user[7]
        markup = CREATOR_MARKUP if user_id == CREATOR_ID else DEFAULT_MARKUP
        if substate:
            update_user('step', 'NULL', user_id)
            if get_people(user_id):
                update_user('page', "'s_0'", user_id)
                bot.send_message(user_id, msg_28, reply_markup=people_markup(user_id, 's', 0))
            else:
                bot.send_message(user_id, msg_29, reply_markup=markup)
        else:
            update_user('step', "'people'", user_id)
            bot.send_message(user_id, msg_27, reply_markup=markup)
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
        return END


@chat_check('verified')
def people_cb(update, context):
    user = update.effective_user
    user_id = user['id']
    query = update.callback_query
    query_data = query['data']
    db_user = get_user(user_id)
    substate = db_user[7]
    if substate:
        update_user('step', 'NULL', user_id)
        every_list = get_every(user_id)
        if every_list:
            page = db_user[10]
            page_type = page[:1]
            page_num = int(page[2:])
            if query_data[:9] in ['s_ttl_btn', 's_tgl_btn']:
                update_switchstate(user_id, query_data[10:])
                query.edit_message_reply_markup(people_markup(user_id, 's', page_num))
                query.answer()
            elif query_data[:9] in ['d_ttl_btn', 'd_tgl_btn']:
                userid = int(query_data[10:])
                msg = people_birthdays(user_id, userid)
                query.answer(text=msg, show_alert=True)
            elif query_data in ['p_btn', 'n_btn']:
                pages_flt = len(every_list) / 5
                pages_int = int(pages_flt)
                pages_num = pages_int - 1 if pages_flt == pages_int else pages_int
                page_prv = page_num - 1 if page_num - 1 >= 0 else pages_num
                page_nxt = page_num + 1 if page_num + 1 <= pages_num else 0
                page_itr = page_prv if query_data == 'p_btn' else page_nxt
                update_user('page', f"'{page_type + '_' + str(page_itr)}'", user_id)
                query.edit_message_reply_markup(people_markup(user_id, page_type, page_itr))
                query.answer()
            elif query_data == 'g_btn':
                switched_len = len(get_switched(user_id, True))
                non_switched_len = len(get_switched(user_id, False))
                global_switchstate = False if switched_len >= non_switched_len else True
                update_global_switchstate(user_id, global_switchstate)
                query.edit_message_reply_markup(people_markup(user_id, page_type, page_num))
                query.answer()
            elif query_data == 'd_btn':
                update_user('page', f"'{'d_' + str(page_num)}'", user_id)
                query.edit_message_reply_markup(people_markup(user_id, 'd', page_num))
                query.answer()
            elif query_data == 'c_btn':
                msg = people_birthdays(user_id)
                query.answer(text=msg, show_alert=True)
            elif query_data == 'b_btn':
                update_user('page', f"'{'s_' + str(page_num)}'", user_id)
                query.edit_message_reply_markup(people_markup(user_id, 's', page_num))
                query.answer()
            else:
                query.answer()
                return None
        else:
            query.edit_message_reply_markup(None)
            query.edit_message_text(msg_29)
    else:
        update_user('step', "'people'", user_id)
        markup = CREATOR_MARKUP if user_id == CREATOR_ID else DEFAULT_MARKUP
        query.bot.send_message(user_id, msg_27, reply_markup=markup)
        query.answer()
    update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
    return END
