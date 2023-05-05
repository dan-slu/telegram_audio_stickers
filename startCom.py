import os
import telebot
import json
from procfunc import * #To import users_folder name

def start_message(message, bot, keyboard1):
    pathUser =USERS_FOLDER+os.path.sep+ str(message.chat.id)

    #if no folder for this user ID, create new one
    if(os.path.exists(pathUser)) == False:
        os.mkdir(pathUser) #creates directory
        pathUserJson =pathUser+os.path.sep+str(message.chat.id)+".json"

        defaultAudioID = "AwACAgIAAxkBAAIB0l8mHcGqTdll2paplcmXnUCo_ybwAAKcBgACrmY5SVvpWYi_EDwJGgQ"
        defaultAudio = {"newAudioN":"", "delAudioN":"", "renamAudioN":"", "renamAudioName":"", "1": ["Welcome Audio", defaultAudioID]}

        with open(pathUserJson, 'w', encoding="utf-8") as f:
            json.dump(defaultAudio, f)

        bot.send_message(message.chat.id, 'Привет, {0}! Ты стал бета-тестером!'.format(message.chat.first_name), reply_markup=keyboard1)
    else:
        bot.send_message(message.chat.id, 'Добро пожаловать, снова', reply_markup=keyboard1)
