from flask import redirect, render_template
from app import app
from db.db import Database
from instagram.inst import Inst

### import classes for working with project
db = Database()
ig = Inst()


### pages routes with visual info
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/list')
def listing():
    profiles = db.getAllProfiles()['profiles']
    return render_template('list.html', profiles=profiles)

@app.route('/admin') 
def adminSettings():
    #return db.getCreds()
    return render_template('admin.html')


### API routes, not pages
@app.route('/api/profiles/')
def allProfiles() :

    return db.getAllProfiles()

@app.route('/api/profiles/<login>/deactivate')
def deactivateUser(login) :
    res = db.changeProfileActivity(login,'N')
    return res

@app.route('/api/profiles/<login>/activate')
def activateUser(login) :    
    res = db.changeProfileActivity(login,'Y')
    
    return res

