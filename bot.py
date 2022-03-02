from telegram.ext import Updater
import os.path as pt
from telegram import Update
from telegram import InputMediaPhoto, InputMediaVideo
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler,MessageHandler,Filters
import random
import time
import json
from db.db import Database
from instagram.inst import Inst

db = Database()
ig = Inst()
token = db.getCreds(cred='token')
updater = Updater(token= token, use_context=True)
dispatcher = updater.dispatcher

def msgHndlr(update: Update, context: CallbackContext) :
    url = update.message.text
    if 'https://www.instagram.com/p/' in url:
        media = ig.getMedia(url)
        items = []
        for item in media['items'] :
            if item['type'] == 'photo' :
                med = InputMediaPhoto(media=item['link'])
            elif item['type'] == 'video' :
                med = InputMediaVideo(media=item['link'])
            items.append(med)
        context.bot.send_media_group(chat_id=update.effective_chat.id,media = items)
        if media['text'] != '' :
            context.bot.send_message(chat_id=update.effective_chat.id, text=media['text'])
    else:
        userInfo = ig.getUserInfo(url)
        db.createNewProfile(userInfo)
        context.bot.send_message(chat_id=update.effective_chat.id, text='Аккаунт добавлен')

def start(update: Update, context: CallbackContext) :
    context.bot.send_message(chat_id=update.effective_chat.id, text='Чтобы получить контент из поста Инстаграм, просто пришли мне ссылку на пост')

if __name__ == '__main__' :
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    post_handler = MessageHandler(Filters.text & (~Filters.command), msgHndlr)
    dispatcher.add_handler(post_handler)

    updater.start_polling()