import sqlite3
import os.path as pt
from db.db import Database
from instagram.inst import Inst

k = Inst()
x = Database()
i = {
    'login' : 'ilya.chuiko',
    'lastpost' : '2384408339091149866'
}
info = k.getInfoByUser(username='ilya.chuiko', dbAction=True)
print(info)