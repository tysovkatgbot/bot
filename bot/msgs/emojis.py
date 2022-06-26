import emoji
import random

emoji_1 = emoji.emojize(':victory_hand_light_skin_tone:', use_aliases=True)
emoji_2 = emoji.emojize(':vulcan_salute_light_skin_tone:', use_aliases=True)
emoji_3 = emoji.emojize(':call_me_hand_light_skin_tone:', use_aliases=True)
emoji_4 = emoji.emojize(':waving_hand_light_skin_tone:', use_aliases=True)
emoji_5 = emoji.emojize(':pizza:', use_aliases=True)
emoji_6 = emoji.emojize(':man_technologist_light_skin_tone:', use_aliases=True)
emoji_7 = emoji.emojize(':man_shrugging_light_skin_tone:', use_aliases=True)
emoji_8 = emoji.emojize(':grinning_face_with_smiling_eyes:', use_aliases=True)
emoji_9 = emoji.emojize(':grinning_face_with_sweat:', use_aliases=True)
emoji_10 = emoji.emojize(':face_with_hand_over_mouth:', use_aliases=True)
emoji_11 = emoji.emojize(':face_with_raised_eyebrow:', use_aliases=True)
emoji_12 = emoji.emojize(':neutral_face:', use_aliases=True)
emoji_13 = emoji.emojize(':winking_face:', use_aliases=True)
emoji_14 = emoji.emojize(':relieved_face:', use_aliases=True)
emoji_15 = emoji.emojize(':nerd_face:', use_aliases=True)
emoji_16 = emoji.emojize(':sleeping_face:', use_aliases=True)
emoji_17 = emoji.emojize(':grimacing_face:', use_aliases=True)
emoji_18 = emoji.emojize(':unamused_face:', use_aliases=True)
emoji_19 = emoji.emojize(':see_no_evil:', use_aliases=True)
emoji_20 = emoji.emojize(':rocket:', use_aliases=True)
emoji_21 = emoji.emojize(':spiral_notepad:', use_aliases=True)
emoji_22 = emoji.emojize(':hourglass_flowing_sand:', use_aliases=True)
emoji_23 = emoji.emojize(':partying_face:', use_aliases=True)
emoji_24 = emoji.emojize(':party_popper:', use_aliases=True)
emoji_25 = emoji.emojize(':wrapped_gift:', use_aliases=True)
emoji_26 = emoji.emojize(':birthday_cake:', use_aliases=True)
emoji_27 = emoji.emojize(':balloon:', use_aliases=True)
emoji_28 = emoji.emojize(':bottle_with_popping_cork:', use_aliases=True)
emoji_29 = emoji.emojize(':shortcake:', use_aliases=True)
emoji_30 = emoji.emojize(':twelve_o’clock:', use_aliases=True)
emoji_31 = emoji.emojize(':twelve-thirty:', use_aliases=True)
emoji_32 = emoji.emojize(':one_o’clock:', use_aliases=True)
emoji_33 = emoji.emojize(':one-thirty:', use_aliases=True)
emoji_34 = emoji.emojize(':two_o’clock:', use_aliases=True)
emoji_35 = emoji.emojize(':two-thirty:', use_aliases=True)
emoji_36 = emoji.emojize(':three_o’clock:', use_aliases=True)
emoji_37 = emoji.emojize(':three-thirty:', use_aliases=True)
emoji_38 = emoji.emojize(':four_o’clock:', use_aliases=True)
emoji_39 = emoji.emojize(':four-thirty:', use_aliases=True)
emoji_40 = emoji.emojize(':five_o’clock:', use_aliases=True)
emoji_41 = emoji.emojize(':five-thirty:', use_aliases=True)
emoji_42 = emoji.emojize(':six_o’clock:', use_aliases=True)
emoji_43 = emoji.emojize(':six-thirty:', use_aliases=True)
emoji_44 = emoji.emojize(':seven_o’clock:', use_aliases=True)
emoji_45 = emoji.emojize(':seven-thirty:', use_aliases=True)
emoji_46 = emoji.emojize(':eight_o’clock:', use_aliases=True)
emoji_47 = emoji.emojize(':eight-thirty:', use_aliases=True)
emoji_48 = emoji.emojize(':nine_o’clock:', use_aliases=True)
emoji_49 = emoji.emojize(':nine-thirty:', use_aliases=True)
emoji_50 = emoji.emojize(':ten_o’clock:', use_aliases=True)
emoji_51 = emoji.emojize(':ten-thirty:', use_aliases=True)
emoji_52 = emoji.emojize(':eleven_o’clock:', use_aliases=True)
emoji_53 = emoji.emojize(':eleven-thirty:', use_aliases=True)
emoji_54 = emoji.emojize(':gear:', use_aliases=True)


def greeting_emoji():
    return random.choice([emoji_1, emoji_2, emoji_3])


def birthday_emoji():
    return random.choice([emoji_23 + emoji_24 + emoji_25,
                          emoji_23 + emoji_26 + emoji_27,
                          emoji_23 + emoji_28 + emoji_29])


def holidays_emoji():
    return random.choice([emoji_24, emoji_25, emoji_26,
                          emoji_27, emoji_28, emoji_29])
