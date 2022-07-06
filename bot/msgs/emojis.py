import emoji
import random

emoji_1 = emoji.emojize(':victory_hand_light_skin_tone:')
emoji_2 = emoji.emojize(':vulcan_salute_light_skin_tone:')
emoji_3 = emoji.emojize(':call_me_hand_light_skin_tone:')
emoji_4 = emoji.emojize(':waving_hand_light_skin_tone:')
emoji_5 = emoji.emojize(':pizza:')
emoji_6 = emoji.emojize(':man_technologist_light_skin_tone:')
emoji_7 = emoji.emojize(':man_shrugging_light_skin_tone:')
emoji_8 = emoji.emojize(':grinning_face_with_smiling_eyes:')
emoji_9 = emoji.emojize(':grinning_face_with_sweat:')
emoji_10 = emoji.emojize(':face_with_hand_over_mouth:')
emoji_11 = emoji.emojize(':face_with_raised_eyebrow:')
emoji_12 = emoji.emojize(':neutral_face:')
emoji_13 = emoji.emojize(':winking_face:')
emoji_14 = emoji.emojize(':relieved_face:')
emoji_15 = emoji.emojize(':nerd_face:')
emoji_16 = emoji.emojize(':sleeping_face:')
emoji_17 = emoji.emojize(':grimacing_face:')
emoji_18 = emoji.emojize(':unamused_face:')
emoji_19 = emoji.emojize(':see_no_evil:')
emoji_20 = emoji.emojize(':rocket:')
emoji_21 = emoji.emojize(':spiral_notepad:')
emoji_22 = emoji.emojize(':hourglass_flowing_sand:')
emoji_23 = emoji.emojize(':partying_face:')
emoji_24 = emoji.emojize(':party_popper:')
emoji_25 = emoji.emojize(':wrapped_gift:')
emoji_26 = emoji.emojize(':birthday_cake:')
emoji_27 = emoji.emojize(':balloon:')
emoji_28 = emoji.emojize(':bottle_with_popping_cork:')
emoji_29 = emoji.emojize(':shortcake:')
emoji_30 = emoji.emojize(':twelve_o’clock:')
emoji_31 = emoji.emojize(':twelve-thirty:')
emoji_32 = emoji.emojize(':one_o’clock:')
emoji_33 = emoji.emojize(':one-thirty:')
emoji_34 = emoji.emojize(':two_o’clock:')
emoji_35 = emoji.emojize(':two-thirty:')
emoji_36 = emoji.emojize(':three_o’clock:')
emoji_37 = emoji.emojize(':three-thirty:')
emoji_38 = emoji.emojize(':four_o’clock:')
emoji_39 = emoji.emojize(':four-thirty:')
emoji_40 = emoji.emojize(':five_o’clock:')
emoji_41 = emoji.emojize(':five-thirty:')
emoji_42 = emoji.emojize(':six_o’clock:')
emoji_43 = emoji.emojize(':six-thirty:')
emoji_44 = emoji.emojize(':seven_o’clock:')
emoji_45 = emoji.emojize(':seven-thirty:')
emoji_46 = emoji.emojize(':eight_o’clock:')
emoji_47 = emoji.emojize(':eight-thirty:')
emoji_48 = emoji.emojize(':nine_o’clock:')
emoji_49 = emoji.emojize(':nine-thirty:')
emoji_50 = emoji.emojize(':ten_o’clock:')
emoji_51 = emoji.emojize(':ten-thirty:')
emoji_52 = emoji.emojize(':eleven_o’clock:')
emoji_53 = emoji.emojize(':eleven-thirty:')
emoji_54 = emoji.emojize(':gear:')


def greeting_emoji():
    return random.choice([emoji_1, emoji_2, emoji_3])


def birthday_emoji():
    return random.choice([emoji_23 + emoji_24 + emoji_25,
                          emoji_23 + emoji_26 + emoji_27,
                          emoji_23 + emoji_28 + emoji_29])


def holidays_emoji():
    return random.choice([emoji_24, emoji_25, emoji_26,
                          emoji_27, emoji_28, emoji_29])
