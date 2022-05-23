import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("./keys/safirebase.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://tesis-ebf9d-default-rtdb.firebaseio.com/'
})

def saveToDB(path, data):
    db.reference(path).set(data)

def retrieveFromDB(path):
    return db.reference(path).get()
