from flask import Flask
from pymongo import MongoClient

def create_app():
    app = Flask(__name__)

    # Initialize MongoDB client
    client = MongoClient("mongodb+srv://modingeroliver:Olivercolopa1@clustertst.cb6tmee.mongodb.net/")
    app.db = client['parkingSys']

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app