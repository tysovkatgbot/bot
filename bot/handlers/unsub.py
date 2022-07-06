from bot.config import CREATOR_ID, DEFAULT_MARKUP, CREATOR_MARKUP, END
from bot.msgs import msg_18, msg_19
from bot.sql.get import get_user, get_table, get_ignored
from bot.sql.update import update_user, update_people, update_global_switchstate
from bot.tools.chat_check import chat_check
from bot.tools.word_form import word_form


@chat_check('verified')
def unsub_msg(update, context):
    bot = context.bot
    user = update.effective_user
    user_id = user['id']
    db_user = get_user(user_id)
    step = db_user[9]
    if step != 'settings':
        gender, substate = db_user[2], db_user[7]
        word = word_form('отписался', gender)
        update_user('step', 'NULL', user_id)
        markup = CREATOR_MARKUP if user_id == CREATOR_ID else DEFAULT_MARKUP
        if substate:
            update_user('substate', False, user_id)
            update_user('timesetting', "'00:00'", user_id)
            if get_table(user_id):
                update_global_switchstate(user_id, False)
                ignored_list = get_ignored(user_id)
                if ignored_list:
                    for userid in ignored_list:
                        update_people(user_id, 'ignored', False, userid)
            msg = msg_18.format(a=word)
            bot.send_message(user_id, msg, reply_markup=markup)
        else:
            msg = msg_19.format(a=word)
            bot.send_message(user_id, msg, reply_markup=markup)
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
        return END
