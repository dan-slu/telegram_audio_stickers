import os
import telebot
import json
from procfunc import *

def inline_que(queueury, bot):
    print(queueury)

    try:
        UserID = str(queueury.from_user.id)

        userAudio = read_jsonfile(UserID)
        print(userAudio)

        allQueries = []

        for fileNum in userAudio:
            print(fileNum)
            if RepresentsInt(fileNum):
                allQueries.append(telebot.types.InlineQueryResultCachedVoice(fileNum, userAudio[fileNum][1], userAudio[fileNum][0]))

        bot.answer_inline_query(queueury.id, allQueries, cache_time=30, is_personal=True)

    except Exception as e:
        print(e)
