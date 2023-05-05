#Проверка повтрного названия
#Добавление мп3
#Change the order
import telebot
import os
from startCom import *
from InlineQue import *
from procfunc import *
#from testing import *

bot = telebot.TeleBot('1071045217:AAEb_yL_Rq6RrYeiryTrcYKliNX7osIQOrI') #bot tokem
storChanId = -1001298194112 #id of storage chanel

#uses for force reply
markup = telebot.types.ForceReply(selective=False)

keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Удалить запись', "Переименовать запись")

@bot.message_handler(commands=['start'])
def startM(message):
    start_message(message, bot, keyboard1)

@bot.message_handler(commands=['test1'])
def testM(message):
    send_default(message, bot)

@bot.message_handler(content_types=['text'])
def send_text(message):
    print(message)

    #name the new audio track
    if userJsonCheck(message.chat.id, "newAudioN") == True:
        userNameTrack(message)
        bot.reply_to(message, "Ваша звуковая запись сохранена, спасибо 😘", reply_markup=keyboard1)

    #delete an audio
    elif message.text == 'Удалить запись':
        if checkDelPos(message):
            keyboardDelete = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)
            for buttonAudio in userAudioList(message):
                keyboardDelete.add(buttonAudio)
            userJsonArgument(message.chat.id, "delAudioN")
            bot.reply_to(message, "Какую аудиозапись вы бы хотели удалить?", reply_markup=keyboardDelete)
        else:
            bot.reply_to(message, "Вы и так уже всё удалили, хватит...", reply_markup=keyboard1)
    elif userJsonCheck(message.chat.id, "delAudioN") == True:
        userDeleteAudio(message)
        bot.reply_to(message, "Данная аудио запись удалена", reply_markup=keyboard1)

    #rename an audio step 1
    elif message.text == 'Переименовать запись':
        if checkDelPos(message):
            keyboardRename = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)
            for buttonAudio in userAudioList(message):
                keyboardRename.add(buttonAudio)
            userJsonArgument(message.chat.id, "renamAudioN")
            bot.reply_to(message, "Какую аудиозапись вы бы хотели переименовать?", reply_markup=keyboardRename)
        else:
            bot.reply_to(message, "А переименовать и нечего...", reply_markup=keyboard1)
    #step 2, record which audio to rename, also check if audio exist
    elif (userJsonCheck(message.chat.id, "renamAudioN") and not(userJsonCheck(message.chat.id, "renamAudioName"))):
        print("step 2")
        if checkAudioExist(message):
             userJsonArgument(message.chat.id, "renamAudioN", renamName = getAudioNumberbyName(message))
             userJsonArgument(message.chat.id, "renamAudioName")
             bot.reply_to(message, "Какое название вам кажется лучше подойдет?")
        else:
            bot.reply_to(message, "Простите, такого аудио нет. Попробуй еще раз")
    #step 3 to rename
    elif (userJsonCheck(message.chat.id, "renamAudioN") and userJsonCheck(message.chat.id, "renamAudioName")):
        print("step 3")
        userRenameAudio(message)
        bot.reply_to(message, "Аудио запись переименована!", reply_markup=keyboard1)

    #if message doesnt make sence
    else:
        bot.send_message(message.chat.id, 'Я не понял, что конкретно вы имели в виду', reply_markup=keyboard1)

#Forward the recorded voice to storage and create a record in json
@bot.message_handler(content_types=['voice'])
def function_name(message):
    print(message)

    if not (checkMaxAud(message)):
        bot.forward_message(storChanId, message.chat.id, message.message_id)
        userJsonArgument(message.chat.id, "newAudioN")
        addFileToJson(message)

        bot.reply_to(message, "Пожалуйста, назовите вашу аудиозапись:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Вы добавили максимум аудио, удалите что-нибудь', reply_markup=keyboard1)

#Forward the audio file to storage
@bot.message_handler(content_types=['audio'])
def creating_new_file(message):
    print(message)
    bot.reply_to(message, "Простите, данная функция еще не реализована")

#Inline handler, the inline function in InlineQue.py
@bot.inline_handler(func=lambda query: True)
def query_text(inline_query):
    inline_que(inline_query, bot)

bot.polling()
