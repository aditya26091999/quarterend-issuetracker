from flask import Flask, request, jsonify, Blueprint
import mysql.connector
import dbQueries
import uuid
from database import *

issueTracker = Blueprint('issueTracker', __name__)


@issueTracker.route('/', methods=['GET'])
def showIssues():
    endpoint = '/issueTracker'
    showIssuesStatus = "failed"
    requestPayload = request.json

    return {"endpoint": endpoint, 'status': showIssuesStatus, 'message': 'All issues fetched for your company'}
