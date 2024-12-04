from pymongo import MongoClient
import os

class Config:
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb+srv://modingeroliver:Olivercolopa1@clustertst.cb6tmee.mongodb.net/'
    MERCADOPAGO_PUBLIC_KEY = os.environ.get('TEST-447ece78-f359-4489-8871-c077286be222') or 'TEST-447ece78-f359-4489-8871-c077286be222'
    MERCADOPAGO_ACCESS_TOKEN = os.environ.get('TEST-1333197382936437-120318-f7dfa2c4fac13e5929914bd1b2c43552-182457169') or 'TEST-1333197382936437-120318-f7dfa2c4fac13e5929914bd1b2c43552-182457169'