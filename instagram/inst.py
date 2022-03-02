from instagrapi import Client
from db.db import Database
import os.path as pt
import requests

class Inst() :

    def getMedia(self, url=None, pk=None) -> dict :
        cl = Client()
        db = Database()
        sessionId = db.getCreds(cred='sessionId')
        cl.login_by_sessionid(sessionid=sessionId)
        
        if pk == None : 
            media = cl.media_pk_from_url(url)
            med= cl.media_info(media).dict()
        else:
            med= cl.media_info(pk).dict()

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

    def getUserInfo(self,url:str) -> dict:
        indexIn = url.rfind('/')
        indexOut = url.rfind('?')
        if indexOut == -1 :
            login = url[indexIn+1:]
        else:
            login = url[indexIn+1:indexOut]

        cl = Client()
        db = Database()
        sessionId = db.getCreds(cred='sessionId')
        cl.login_by_sessionid(sessionid=sessionId)
        userId = cl.user_id_from_username(login)
        posts = cl.user_medias(userId)
        last = posts[1].dict()

        lastpost = last['pk']

        result = {
            'login' : login,
            'lastpost' : lastpost
        }

        ea = cl.media_info('2384408339091149866').dict()

        return result

    def getInstLinkByPk(self, pk:str) -> str:
        cl = Client()
        db = Database()
        sessionId = db.getCreds(cred='sessionId')
        cl.login_by_sessionid(sessionid=sessionId)

        code = cl.media_info(pk).dict()['code']
        url = f'https://instagram.com/p/{code}/'

        return url


### NEW TYPES ###


    def getInfoByUser(self, username=None, url=None, dbAction=False) -> dict :
        cl = Client()
        db = Database()
        
        if username != None :
            login = username
        else:
            indexIn = url.rfind('/')
            indexOut = url.rfind('?')
            if indexOut == -1 :
                login = url[indexIn+1:]
            else:
                login = url[indexIn+1:indexOut]
        sessionId = db.getCreds(cred='sessionId')
        cl.login_by_sessionid(sessionid=sessionId)
        userInfo = cl.user_info_by_username(login).dict()
        posts = cl.user_medias(userInfo['pk'])
        lastpost = posts[1].dict()

        result = {
            'userPk' : userInfo['pk'],
            'login' : login,
            'profilePic' : str(userInfo['profile_pic_url_hd']),
            'lastpostPk' : lastpost['pk'],
            'lastpostUrl' : f"https://instagram.com/p/{lastpost['code']}/"
        }

        if dbAction == True :
            photoFilename = f'app/static/photos/{login}.png'
            flaskFilename = f'photos/{login}.png'
            with open(pt.abspath(photoFilename), 'wb') as file:
                res = requests.get(str(userInfo['profile_pic_url_hd']))
                file.write(res.content)
            result['profilePic'] = flaskFilename
            db.createNewProfile(result)
        
        return result


    def getMediaFromPost(self, url=None , pk=None , code=None) -> dict :
        cl = Client()
        db = Database()
        sessionId = db.getCreds(cred='sessionId')
        cl.login_by_sessionid(sessionid=sessionId)
        
        if url != None : 
            media = cl.media_pk_from_url(url)
            med= cl.media_info(media).dict()
        elif code != None:
            url = f"https://instagram.com/p/{code}/"
            media = cl.media_pk_from_url(url)
            med= cl.media_info(media).dict()
        else :    
            med= cl.media_info(pk).dict()
        
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
