from pymongo import MongoClient
import os

class Config:
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb+srv://modingeroliver:Olivercolopa1@clustertst.cb6tmee.mongodb.net/'