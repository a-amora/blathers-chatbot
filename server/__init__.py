import os
from flask import Flask, g
from flask_cors import CORS
from server.api.routes import stella_routes
from server.vector import initialize_db
from server.utils import load_llm

def run():
    app = Flask(__name__)
    CORS(app)
    
    initialize_db(app)
    load_llm(app)
    app.register_blueprint(stella_routes)

    return app