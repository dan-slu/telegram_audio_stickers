import os
import json
import telebot

NUMBER_OF_SERVICE_ARGUMENTS = 4
USERS_FOLDER = "Users"

#Read json file function in order to create list for inline query
def read_jsonfile(userID):
    pathJson = USERS_FOLDER+os.path.sep+str(userID)+os.path.sep+str(userID)+".json"
    with open(pathJson, encoding="utf-8") as f:
        return json.load(f)

#check if str is int
def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

#adds audio file to json
def addFileToJson(message):
    userID = message.chat.id
    pathJson = USERS_FOLDER+os.path.sep+str(userID)+os.path.sep+str(userID)+".json"
    userAudioDict = read_jsonfile(userID)

    audioNum = str(len(userAudioDict)-NUMBER_OF_SERVICE_ARGUMENTS+1)
    audioType = message.content_type
    if audioType == "audio":
        audioID = message.audio.file_id
    elif audioType == "voice":
        audioID = message.voice.file_id

    userAudioDict.update({audioNum:[message.content_type, audioID]})
    userAudioDict["newAudioN"] = audioNum

    with open(pathJson, 'w', encoding="utf-8") as f:
        json.dump(userAudioDict, f)

#changes the argument in json
def userJsonArgument(userID, arg, renamName = None):
    pathJson = USERS_FOLDER+os.path.sep+str(userID)+os.path.sep+str(userID)+".json"
    userAudioDict = read_jsonfile(userID)
    if renamName == None:
        if arg == "newAudioN":
            userAudioDict["newAudioN"] = "voice"
        if arg == "delAudioN":
            userAudioDict["delAudioN"] = True
        if arg == "renamAudioN":
            userAudioDict["renamAudioN"] = True
        if arg == "renamAudioName":
            userAudioDict["renamAudioName"] = True
    else:
        if arg == "renamAudioN":
            userAudioDict["renamAudioN"] = renamName

    with open(pathJson, 'w', encoding="utf-8") as f:
        json.dump(userAudioDict, f)

#return the state of parameter
def userJsonCheck(userID, paramCheck):
    pathJson = USERS_FOLDER+os.path.sep+str(userID)+os.path.sep+str(userID)+".json"
    userAudioDict = read_jsonfile(userID)

    if userAudioDict[paramCheck] == "":
        return False
    else:
        return True

#Names the track in Json
def userNameTrack(message):
    userID = message.chat.id
    pathJson = USERS_FOLDER+os.path.sep+str(userID)+os.path.sep+str(userID)+".json"
    userAudioDict = read_jsonfile(userID)

    userAudioDict[userAudioDict["newAudioN"]][0] = str(message.text)
    userAudioDict["newAudioN"] = ""

    with open(pathJson, 'w', encoding="utf-8") as f:
        json.dump(userAudioDict, f)

#creates a list of buttons of audios
def userAudioList(message):
    userID = message.chat.id
    pathJson = USERS_FOLDER+os.path.sep+str(userID)+os.path.sep+str(userID)+".json"
    userAudioDict = read_jsonfile(userID)

    listOfAudio = []

    for audioN in userAudioDict:
        if RepresentsInt(audioN):
            listOfAudio.append(telebot.types.KeyboardButton(userAudioDict[audioN][0]))

    return listOfAudio

#get audio Number by Name
def getAudioNumberbyName(message):
    userID = message.chat.id
    pathJson = USERS_FOLDER+os.path.sep+str(userID)+os.path.sep+str(userID)+".json"
    userAudioDict = read_jsonfile(userID)

    audioNum = 0

    for audioTrack in userAudioDict:
        if RepresentsInt(audioTrack):
            if userAudioDict[audioTrack][0] == str(message.text):
                audioNum = audioTrack

    return audioNum

#function to move all the audio tracks if one is deleted, assist functon to userDeleteAudio
def userDeleteAudioAssist(userDict, audioDelN):
    audioDelNn = str(int(audioDelN)+1)
    userDict[audioDelN] = userDict[audioDelNn]
    del userDict[audioDelNn]
    if str(int(audioDelNn)+1) in userDict:
        return userDeleteAudioAssist(userDict, audioDelNn)
    else:
        return userDict

#deletes an audio for user
def userDeleteAudio(message):
    userID = message.chat.id
    pathJson = USERS_FOLDER+os.path.sep+str(userID)+os.path.sep+str(userID)+".json"
    userAudioDict = read_jsonfile(userID)

    audioNumDel = getAudioNumberbyName(message)

    #the case when audio is last in dict
    if int(audioNumDel) == (len(userAudioDict)-NUMBER_OF_SERVICE_ARGUMENTS):
        del userAudioDict[audioNumDel]
    else:
        del userAudioDict[audioNumDel]
        userAudioDict = userDeleteAudioAssist(userAudioDict, audioNumDel)

    userAudioDict["delAudioN"] = ""

    with open(pathJson, 'w', encoding="utf-8") as f:
        json.dump(userAudioDict, f)

#function to check if any tracks left to delete
def checkDelPos(message):
    userAudioDict = read_jsonfile(message.chat.id)
    if len(userAudioDict) == NUMBER_OF_SERVICE_ARGUMENTS:
        return False
    else:
        return True

#function to check if there are more than 50 tracks
def checkMaxAud(message):
    userAudioDict = read_jsonfile(message.chat.id)
    if len(userAudioDict) == (NUMBER_OF_SERVICE_ARGUMENTS + 50):
        return True

#Check if such audio exist
def checkAudioExist(message):
    audioList = userAudioList(message)
    for audioButton in audioList:
        if audioButton.text == str(message.text):
            return True
    return False

#renames audio
def userRenameAudio(message):
    userID = message.chat.id
    pathJson = USERS_FOLDER+os.path.sep+str(userID)+os.path.sep+str(userID)+".json"
    userAudioDict = read_jsonfile(userID)
    audioNumRenam = userAudioDict["renamAudioN"]

    for audioTrack in userAudioDict:
        if RepresentsInt(audioTrack):
            if audioTrack == audioNumRenam:
                userAudioDict[audioTrack][0] = str(message.text)

    userAudioDict["renamAudioN"] = ""
    userAudioDict["renamAudioName"] = ""

    with open(pathJson, 'w', encoding="utf-8") as f:
        json.dump(userAudioDict, f)
