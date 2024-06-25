import configparser

import firebase_admin
from firebase_admin import credentials, storage

config_path = configparser.ConfigParser()
config_path.read('firebase-path.properties')

cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)

default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': f'{config_path['default']['databaseURL']}',
    'storageBucket': f'{config_path['default']['storageBucket']}',
})

bucket = storage.bucket()
