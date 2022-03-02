import sqlite3
import os.path as pt
import json

#conn = sqlite3.connect(pt.abspath('db/database.db'))
#cursor = conn.cursor()
#query = """CREATE TABLE profiles (user_pk text , login text, profile_pic text, lastpostpk text, lastpost_url, is_active text)"""
#cursor.execute(query)
#conn.commit()

class Database() :

    def getAllProfiles(self) -> dict :
        conn = sqlite3.connect(pt.abspath('db/database.db'))
        cursor = conn.cursor()

        query = """SELECT * FROM profiles"""
        cursor.execute(query)
        profiles = cursor.fetchall()
        resultItems = []

        for item in profiles :
            profile = {
                'userPk' : item[0],
                'login' : item[1],
                'profilePic' : item[2],
                'lastpostPk' : item[3],
                'lastpostUrl' : item[4],
                'isActive' : item[5]
            }
            resultItems.append(profile)
        
        result = {
            'ok' : True,
            'profiles' : resultItems,
            'message' : 'Аккаунты получены успешно'
        }

        return result
    
    def createNewProfile(self, info:dict) -> dict :
        allProfiles = self.getAllProfiles()
        if len(allProfiles['profiles']) != 0:
            for item in allProfiles['profiles'] :
                if item['login'] == info['login'] or len(allProfiles['profiles']) == 0 :
                    result = {
                        'ok' : False,
                        'message' : 'Данный аккаунт уже добавлен'
                    }

                    return result
                else:
                    conn = sqlite3.connect(pt.abspath('db/database.db'))
                    cursor = conn.cursor()

                    query = f"""INSERT INTO profiles VALUES ( '{info['userPk']}','{info['login']}', '{info['profilePic']}' , '{info['lastpostPk']}', '{info['lastpostUrl']}' ,'Y' )"""
                    cursor.execute(query)
                    conn.commit()

                    result = {
                        'ok' : True,
                        'message' : 'Аккаунт добавлен успешно'
                    }

                    return result
        else :
            conn = sqlite3.connect(pt.abspath('db/database.db'))
            cursor = conn.cursor()

            query = f"""INSERT INTO profiles VALUES ( '{info['userPk']}','{info['login']}', '{info['profilePic']}' , '{info['lastpostPk']}', '{info['lastpostUrl']}' ,'Y' )"""
            cursor.execute(query)
            conn.commit()

            result = {
                    'ok' : True,
                    'message' : 'Аккаунт добавлен успешно'
            }

            return result
    
    def updateProfilePost(self, info:dict) -> dict :
        pass

    def changeProfileActivity(self, login:str, activity:str) -> dict :
        conn = sqlite3.connect(pt.abspath('db/database.db'))
        cursor = conn.cursor()

        if activity == 'N':

            query = f"""UPDATE profiles SET is_active = 'N' WHERE login = '{login}'"""
            cursor.execute(query)
            conn.commit()

            result = {
                'ok' : True,
                'message' : 'Profile deactivated'
            }

            return result
        else:
            query = f"""UPDATE profiles SET is_active = 'Y' WHERE login = '{login}'"""
            cursor.execute(query)
            conn.commit()

            result = {
                'ok' : True,
                'message' : 'Profile activated'
            }

            return result

    def getCreds(self,cred=None) -> str :
        with open(pt.abspath('db/creds.json')) as file :
            data = json.load(file)
            
            if cred == 'sessionId' :
                sessionId = data['sessionId']
                return sessionId
            elif cred == 'token' :
                token = data['token']
                return token
            else: 
                return data