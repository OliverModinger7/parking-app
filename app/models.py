from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb+srv://modingeroliver:Olivercolopa1@clustertst.cb6tmee.mongodb.net/")
db = client['parkingSys']
collection = db['registros_patentes']
events_collection = db['logs_evento']
qr_collection = db['qr_codes']

class DataModel:
    def __init__(self, patente, ubicacion="Entrada principal"):
        self.patente = patente
        self.timestamp = datetime.now().isoformat()
        self.ubicacion = ubicacion

    def save_to_db(self):
        collection.insert_one({
            'patente': self.patente,
            'timestamp': self.timestamp,
            'ubicacion': self.ubicacion
        })

    @staticmethod
    def get_data(patente):
        return collection.find_one({'patente': patente})

class EventModel:
    def __init__(self, patente):
        self.patente = patente
        self.start_time = datetime.now().isoformat()
        self.end_time = None

    def start_event(self):
        events_collection.insert_one({
            'patente': self.patente,
            'start_time': self.start_time,
            'end_time': self.end_time
        })

    @staticmethod
    def stop_event(patente):
        event = events_collection.find_one({'patente': patente, 'end_time': None})
        if event:
            end_time = datetime.now().isoformat()
            events_collection.update_one({'_id': event['_id']}, {'$set': {'end_time': end_time}})
            return end_time
        return None

    @staticmethod
    def get_event(patente):
        return events_collection.find_one({'patente': patente})

class QRModel:
    def __init__(self, patente, qr_code):
        self.patente = patente
        self.qr_code = qr_code
        self.timestamp = datetime.now().isoformat()

    def save_to_db(self):
        qr_collection.insert_one({
            'patente': self.patente,
            'qr_code': self.qr_code,
            'timestamp': self.timestamp
        })

    @staticmethod
    def get_qr(patente):
        return qr_collection.find_one({'patente': patente})