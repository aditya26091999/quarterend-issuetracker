from flask import Flask, request, jsonify, Blueprint
import mysql.connector
import dbQueries
import uuid
from database import *

issueTracker = Blueprint('issueTracker', __name__)

@issueTracker.route('/create', methods=['POST'])
def createIssues():
    endpoint = '/issueTracker/create'
    createIssuesStatus = "failed"

    requestPayload = request.json
    requestHeaders = request.headers

    try:
        submittedBy = requestPayload['issueSubmittedBy']
        sql = dbQueries.userIdlookup_sql.format(requestHeaders['X-Company-Id'])
        val = (submittedBy,)
        globalMySQLCursor.execute(sql,val)
        submittedById = globalMySQLCursor.fetchone()

        assignedTo = requestPayload['issueAssignedTo']
        sql = dbQueries.userIdlookup_sql.format(requestHeaders['X-Company-Id'])
        val = (assignedTo,)
        globalMySQLCursor.execute(sql,val)
        assignedToId = globalMySQLCursor.fetchone()

        if requestPayload['issueResolved'] == "Yes":
            resolved = 1
        else:
            resolved = 0

        if requestPayload['issuePriority'] == "":
            priority = 3
        else:
            priority = requestPayload['issuePriority']

        sql = dbQueries.issueTrackerIssueCreation_sql.format(requestHeaders['X-Company-Id'])
        val = (requestPayload['issueId'],requestPayload['issueTitle'],requestPayload['issueDescription'],submittedById[0],assignedToId[0],requestPayload['issueDate'],priority,resolved,requestPayload['issueSolution'])
        globalMySQLCursor.execute(sql,val)
        globalMySQLConnector.commit()
        createIssuesStatus="success"

    except Exception as e:
        print(e)
        return {'endpoint': endpoint, 'status': createIssuesStatus,'message': 'Error while inserting issue-data. Please check if all fields are valid'}

    return {"endpoint": endpoint, 'status': createIssuesStatus, 'message': 'Issue {} created in the org.'.format(requestPayload['issueId'])}

@issueTracker.route('/get', methods=['GET'])
def showIssues():
    endpoint = '/issueTracker/get'
    showIssuesStatus = "failed"
    requestHeaders = request.headers

    try:
        sql = dbQueries.issueTrackerShowIssues_sql.format(requestHeaders['X-Company-Id'],requestHeaders['X-Company-Id'],requestHeaders['X-Company-Id'],requestHeaders['X-Company-Id'],requestHeaders['X-Company-Id'],requestHeaders['X-Company-Id'])
        globalMySQLCursor.execute(sql)
        allIssues = globalMySQLCursor.fetchall()

        if not allIssues:
            showIssuesStatus = "success"
            return {'endpoint': endpoint, 'status': showIssuesStatus, 'message':'No current issues in the system'}
        else:
            responsePayload = list()
            for issue in allIssues:
                issueComponent = dict()
                issueComponent['issueId'] = issue[0]
                issueComponent['issueTitle'] = issue[1]
                issueComponent['issueDescription'] = issue[2]
                issueComponent['issueDate'] = issue[3].strftime("%d-%m-%Y")
                issueComponent['issuePriority'] = issue[4]
                if issue[5]==1:
                    issueComponent['issueResolved'] = "Yes"
                else:
                    issueComponent['issueResolved'] = "No"
                issueComponent['issueSolution'] = issue[6]
                issueComponent['issueSubmittedBy'] = issue[7]
                issueComponent['issueSubmittedByEmail'] = issue[8]
                issueComponent['issueAssignedTo'] = issue[9]
                issueComponent['issueAssignedToEmail'] = issue[10]
                responsePayload.append(issueComponent)
            showIssuesStatus = "success"

    except Exception as e:
        print(e)
        return {'endpoint': endpoint, 'status':showIssuesStatus, 'message':'Error while loading issues from tenant. Check after some time'}, 500

    return {"endpoint": endpoint, 'status': showIssuesStatus, 'message': 'All issues fetched for your company','data':responsePayload}
