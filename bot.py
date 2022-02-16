from telegram.ext import Updater
import os.path as pt
from instagrapi import Client
from telegram import Update
from telegram import InputMediaPhoto, InputMediaVideo
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler,MessageHandler,Filters
import random
import time
import json

"""functions for inst and credentials"""

def getCreds(cred:str) -> str :
    with open(pt.abspath('creds.json')) as file :
        data = json.load(file)
        
        if cred == 'sessionId' :
            sessionId = data['sessionId']
        
            return sessionId
        elif cred == 'token' :
            token = data['token']

            return token

def getMedia(url:str) -> dict :
    cl = Client()
    sessionId = getCreds(cred='sessionId')
    cl.login_by_sessionid(sessionid=sessionId)

    media = cl.media_pk_from_url(url)
    med= cl.media_info(media).dict()


    items = []

    try:
        if len(med['resources']) != 0 :
            resources = med['resources']
            for res in resources :
                if res['video_url'] == None:
                    m = {
                        'type' : 'photo',
                        'link' : str(res['thumbnail_url'])
                    }
                    items.append(m)
                else:
                    m = {
                        'type' : 'video' ,
                        'link' : str(res['video_url'])
                    }
                    items.append(m)
        elif med['video_url'] == None:
            m = {
                'type' : 'photo',
                'link' : str(med['thumbnail_url'])
            }
            items.append(m)
        elif med['video_url'] != None:
            m = {
                'type' : 'video',
                'link' : str(med['video_url'])
            }
            items.append(m)
        result = {
            'ok' : 'true',
            'text' : med['caption_text'],
            'items' : items
        }
    except AssertionError:
        result = {
            'ok' : 'false',
            'text' : 'Надо заменить sessionId'
        }
    return result

"""Telegram bot part"""

token = getCreds(cred='token')
updater = Updater(token= token, use_context=True)
dispatcher = updater.dispatcher

def sendMedia(update: Update, context: CallbackContext) :
    url = update.message.text
    if 'https' in url :
        media = getMedia(url)

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
        context.bot.send_message(chat_id=update.effective_chat.id, text='Это не ссылка, не могу скачать пост')

def start(update: Update, context: CallbackContext) :
    context.bot.send_message(chat_id=update.effective_chat.id, text='Чтобы получить контент из поста Инстаграм, просто пришли мне ссылку на пост')

if __name__ == '__main__' :
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    post_handler = MessageHandler(Filters.text & (~Filters.command), sendMedia)
    dispatcher.add_handler(post_handler)

    updater.start_polling()