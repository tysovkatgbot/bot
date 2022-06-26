from bot.msgs.emojis import emoji_4, emoji_5, emoji_6, emoji_7, emoji_8, emoji_9, emoji_10, \
                            emoji_11, emoji_12, emoji_13, emoji_14, emoji_15, emoji_16, emoji_17, \
                            emoji_18, emoji_19, emoji_20, emoji_21, emoji_22, emoji_23
from bot.tools.string_escape import string_escape

msg_1 = 'привет{a}! {b}'
msg_2 = f'{{a}}я напомню {{b}} о днях рождения {{c}} друзей {emoji_19}\n' \
        f'создатель — @{{d}} {emoji_6}{{e}}'
msg_3 = f'как мне тебя называть? {emoji_11}'
msg_4 = f'*{{a}}* уже в *тусовке* {emoji_5}\n' \
        f'попробуй еще раз {emoji_17}'
msg_5 = f'как, говоришь? {emoji_7}'
msg_6 = f'выбери свой пол {emoji_11}'
msg_7 = f'не совсем тебя понял {emoji_7}'
msg_8 = f'введи свою *дату рождения* в формате ДД.ММ.ГГГГ {emoji_11}'
msg_9 = f'неверный формат, попробуй ещё раз {emoji_7}'
msg_10 = f'запомнил, *{{a}}* {emoji_14}'
msg_11 = f'{{a}} сегодня {{b}}! {emoji_8}\n' \
         f'не забудь {{c}} поздравить {{d}}'
msg_12 = f'{{a}} {{b}} через {{c}}! {emoji_22}'
msg_13 = f'{{a}} сегодня {{b}}! {emoji_23}'
msg_14 = f'для получения уведомлений определи свой *список людей* {emoji_16}'
msg_15 = f'теперь ты *{{a}}* на уведомления {emoji_8}\n' \
         f'они будут приходить к тебе ровно в {{b}} {emoji_20}\n' \
         f'определи свой *список людей* {emoji_21}\n' \
         f'и, если хочешь, установи собственное *время* прихода уведомлений {emoji_22}'
msg_16 = f'ты уже *{{a}}* на уведомления {emoji_14}'
msg_17 = f'ты только что *{{a}}* от уведомлений {emoji_18}'
msg_18 = f'ты уже *{{a}}* от уведомлений {emoji_12}'
msg_19 = f'введи *время* в формате ЧЧ:ММ {emoji_15}'
msg_20 = f'для редактирования *времени* подпишись на уведомления {emoji_16}'
msg_21 = 'по умолчанию *({a})*'
msg_22 = 'на *{a}*'
msg_23 = '*время* прихода уведомлений установлено {a}, ' \
         'что бы изменить *время*, нажми на кнопку ниже {b}'
msg_24 = f'тебе уже приходило уведомление о том, что {{a}} сегодня {{b}}!\n' \
         f'напомнить ещё раз в *{{c}}*? {emoji_11}'
msg_25 = '*время* установлено на *{a}* {b}'
msg_26 = f'для редактирования *списка людей* подпишись на уведомления {emoji_16}'
msg_27 = f'*список люди*, о чьих днях рождения\n' \
         f'ты будешь получать уведомления {emoji_21}'
msg_28 = f'в *списке* пока нет людей {emoji_7}'
msg_29 = f'охрана отменена, я могу для тебя что-нибудь ещё сделать? {emoji_9}'
msg_30 = f'охрана отменена, ты получишь уведомление через *{{a}}* {emoji_13}\n' \
         f'я могу для тебя что-нибудь ещё сделать? {emoji_9}'
msg_31 = f'охрана отменена, *сегодня* больше напоминать не буду {emoji_10}\n' \
         f'я могу для тебя что-нибудь ещё сделать? {emoji_9}'
msg_32 = f'охраны отмены не будет, отменять то и нечего {emoji_7}'
msg_33 = 'добро пожаловать в *тусовку*{a}! {b}'
msg_34 = f'пока, удачи{{a}}! {emoji_4}'
msg_35 = f'для редактирования *настроек* подпишись на уведомления {emoji_16}'
msg_36 = f'что хочешь изменить? {emoji_11}'
msg_37 = f'для редактирования *праздников* подпишись на уведомления {emoji_16}'
msg_38 = f'что бы добавить праздники, введи, через запятую: *дату праздника* в формате ДД.ММ и ' \
         f'*сообщение*, которое будет отправлено в тусовку {emoji_8}\n\n' \
         f'что бы удалить праздники, введи *даты праздников* в формате ДД.ММ {emoji_18}\n\n' \
         f'каждый праздник разделяй переносом строки {emoji_15}'
msg_39 = f'*список праздников* пуст {emoji_7}'
msg_40 = f'произошла ошибка {emoji_17}'

msg_1 = string_escape(msg_1, '!')
msg_8 = string_escape(msg_8, '.')
msg_11 = string_escape(msg_11, '!')
msg_19 = string_escape(msg_19, '-')
msg_21 = string_escape(msg_21, '()')
msg_24 = string_escape(msg_24, '!')
msg_29 = string_escape(msg_29, '-')
msg_30 = string_escape(msg_30, '-')
msg_31 = string_escape(msg_31, '-')
msg_33 = string_escape(msg_33, '!')
msg_34 = string_escape(msg_34, '()!')
msg_35 = string_escape(msg_35, '!')
msg_37 = string_escape(msg_37, '!')
msg_38 = string_escape(msg_38, '().')
msg_39 = string_escape(msg_39, '.')
