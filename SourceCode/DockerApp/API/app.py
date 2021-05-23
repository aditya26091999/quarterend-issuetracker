#Importing dependencies
from flask import Flask, request, jsonify,Blueprint
import mysql.connector

import database
from database import *
import dbQueries

#import Submodules
from user import user
from admin import admin
from issueTracker import issueTracker

#Create the Flask app
app = Flask(__name__)
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(issueTracker, url_prefix='/issueTracker')

#PingTest to check API/DB server status
@app.route('/',methods=['GET'])
def pingTest():
    return {"status": status, "messageType": "log", "API": "Flask is up and running", "DB": dbStatus}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
