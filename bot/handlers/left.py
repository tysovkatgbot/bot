from telegram.utils.helpers import mention_markdown

from bot.config import CREATOR_ID
from bot.msgs import msg_34
from bot.sql.delete import delete_user
from bot.sql.get import get_users, get_user
from bot.tools.chat_check import chat_check


@chat_check('tysovka')
def left_msg(update, context):
    message = update.effective_message
    left_user = message.left_chat_member
    if not left_user.is_bot and left_user.id != CREATOR_ID:
        userid = str(left_user.id)
        userid_list = [row[0] for row in get_users()]
        if userid in userid_list:
            username = get_user(userid)[1]
            if username:
                mention = mention_markdown(userid, username, version=2)
                delete_user(userid)
                message.reply_text(msg_34.format(a=', ' + mention))
            else:
                delete_user(userid)
                message.reply_text(msg_34.format(a=''))
        else:
            message.reply_text(msg_34.format(a=''))
    else:
        return None
