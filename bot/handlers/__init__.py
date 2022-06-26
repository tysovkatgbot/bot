import re

from telegram.ext import MessageHandler, CallbackQueryHandler, ConversationHandler, Filters

from bot.config import LOGGER, CREATOR_ID, USERNAME_STORED, GENDER_STORED, BIRTHDAY_STORED, \
                       TIME_ENTERED, TIME_REPEATED, SETTING_CHOSEN, HOLIDAY_ADDED, END
from bot.handlers.cancel import cancel_msg
from bot.handlers.holidays import holidays_msg, holidays_cb, process_holidays
from bot.handlers.left import left_msg
from bot.handlers.new import new_msg
from bot.handlers.people import people_msg, people_cb
from bot.handlers.settings import settings_msg, choose_setting, settings_cb
from bot.handlers.start import start_msg
from bot.handlers.store import store_username, store_gender, store_birthday
from bot.handlers.sub import sub_msg
from bot.handlers.time import time_msg, enter_time, repeat_time, time_cb
from bot.handlers.unsub import unsub_msg


def exit_conversation(update, context):
    return END


def error_cb(update, context):
    LOGGER.warning(context.error)


def register_handlers(dispatcher):
    creator_filter = Filters.chat(CREATOR_ID)
    start_filter = Filters.regex(re.compile(r'^/start$', re.IGNORECASE))
    sub_filter = Filters.regex(re.compile(r'^подписка$', re.IGNORECASE))
    unsub_filter = Filters.regex(re.compile(r'^отписка$', re.IGNORECASE))
    people_filter = Filters.regex(re.compile(r'^люди$', re.IGNORECASE))
    time_filter = Filters.regex(re.compile(r'^время$', re.IGNORECASE))
    settings_filter = Filters.regex(re.compile(r'^настройки$', re.IGNORECASE))
    holidays_filter = Filters.regex(re.compile(r'^праздники$', re.IGNORECASE))
    cancel_filter = Filters.regex(re.compile(r'^отмена$', re.IGNORECASE))
    include_filter = start_filter | sub_filter | unsub_filter | people_filter | time_filter | \
        settings_filter | (holidays_filter & creator_filter) | cancel_filter
    exclude_filter = ~start_filter & ~sub_filter & ~unsub_filter & ~people_filter & \
        ~time_filter & ~settings_filter & ~(holidays_filter & creator_filter) & ~cancel_filter
    start_msg_handler = MessageHandler(start_filter, start_msg)
    sub_msg_handler = MessageHandler(sub_filter, sub_msg)
    unsub_msg_handler = MessageHandler(unsub_filter, unsub_msg)
    people_msg_handler = MessageHandler(people_filter, people_msg)
    time_msg_handler = MessageHandler(time_filter, time_msg)
    settings_msg_handler = MessageHandler(settings_filter, settings_msg)
    holidays_msg_handler = MessageHandler(creator_filter & holidays_filter, holidays_msg)
    cancel_msg_handler = MessageHandler(cancel_filter, cancel_msg)
    new_msg_handler = MessageHandler(Filters.status_update.new_chat_members, new_msg)
    left_msg_handler = MessageHandler(Filters.status_update.left_chat_member, left_msg)
    time_cb_handler = CallbackQueryHandler(time_cb, pattern=r'^t_btn$')
    people_cb_handler = CallbackQueryHandler(people_cb, pattern=r'^s_ttl_btn_+\d*$|'
                                                                r'^s_tgl_btn_+\d*$|'
                                                                r'^d_ttl_btn_+\d*$|'
                                                                r'^d_tgl_btn_+\d*$|'
                                                                r'^p_btn$|^n_btn$|^g_btn$|'
                                                                r'^d_btn$|^c_btn$|^b_btn$')
    settings_cb_handler = CallbackQueryHandler(settings_cb, pattern=r'^s_btn$')
    holidays_cb_handler = CallbackQueryHandler(holidays_cb, pattern=r'^h_btn$')
    sub_cnv_handler = ConversationHandler(
        entry_points=[sub_msg_handler],
        states={USERNAME_STORED: [MessageHandler(Filters.text, store_username)],
                GENDER_STORED: [MessageHandler(Filters.text, store_gender)],
                BIRTHDAY_STORED: [MessageHandler(Filters.text, store_birthday)]},
        fallbacks=[MessageHandler(Filters.text, exit_conversation)],
        allow_reentry=True,
        name='SubConversationHandler')
    time_cnv_handler = ConversationHandler(
        entry_points=[time_cb_handler],
        states={TIME_ENTERED: [MessageHandler(exclude_filter, enter_time)],
                TIME_REPEATED: [MessageHandler(exclude_filter, repeat_time)]},
        fallbacks=[MessageHandler(include_filter, exit_conversation)],
        allow_reentry=True,
        name='TimeConversationHandler')
    settings_cnv_handler = ConversationHandler(
        entry_points=[settings_cb_handler],
        states={SETTING_CHOSEN: [MessageHandler(~cancel_filter, choose_setting)],
                USERNAME_STORED: [MessageHandler(~cancel_filter, store_username)],
                GENDER_STORED: [MessageHandler(~cancel_filter, store_gender)],
                BIRTHDAY_STORED: [MessageHandler(~cancel_filter, store_birthday)]},
        fallbacks=[MessageHandler(cancel_filter, exit_conversation)],
        allow_reentry=True,
        name='SettingsConversationHandler')
    holidays_cnv_handler = ConversationHandler(
        entry_points=[holidays_cb_handler],
        states={HOLIDAY_ADDED: [MessageHandler(exclude_filter, process_holidays)]},
        fallbacks=[MessageHandler(include_filter, exit_conversation)],
        allow_reentry=True,
        name='HolidaysConversationHandler')
    dispatcher.add_handler(start_msg_handler, 1)
    dispatcher.add_handler(sub_cnv_handler, 1)
    dispatcher.add_handler(unsub_msg_handler, 1)
    dispatcher.add_handler(time_msg_handler, 2)
    dispatcher.add_handler(time_cnv_handler, 3)
    dispatcher.add_handler(people_msg_handler, 1)
    dispatcher.add_handler(people_cb_handler, 1)
    dispatcher.add_handler(settings_msg_handler, 2)
    dispatcher.add_handler(settings_cnv_handler, 3)
    dispatcher.add_handler(holidays_msg_handler, 2)
    dispatcher.add_handler(holidays_cnv_handler, 3)
    dispatcher.add_handler(cancel_msg_handler, 1)
    dispatcher.add_handler(new_msg_handler, 1)
    dispatcher.add_handler(left_msg_handler, 1)
    dispatcher.add_error_handler(error_cb)
