from flask import Flask, request, jsonify, Blueprint
import mysql.connector
import dbQueries
from database import *

admin = Blueprint('admin', __name__)

#Admin-Register webservice
@admin.route('/register',methods=['POST'])
def adminRegister():

    adminRegisterStatus = "failed"
    endpoint = "/admin/register"
    requestPayload = request.json

    #prepare new-admin insert sql query
    sql = dbQueries.companyRegisteration_sql
    val = (requestPayload['companyUID'],requestPayload['companyName'],requestPayload['companyAddress'],requestPayload['companyAdminEmail'],requestPayload['companyAdminPassword'])
    try:
        globalMySQLCursor.execute(sql, val)
        globalMySQLConnector.commit()

        #prepare new-company schema creation query [Multi-Tenancy]
        sql = dbQueries.companySpecificSchemaCreation_sql + requestPayload['companyUID']
        globalMySQLCursor.execute(sql)
        globalMySQLConnector.commit()

        #Connect to new company-database to create User/IssueTracker Table
        companySpecificSchemaConnector = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="aditya",
            database=requestPayload['companyUID']
        )
        companySpecificSchemaCursor = companySpecificSchemaConnector.cursor()

        #prepare User-Table creation SQL query
        sql = dbQueries.userTableCreation_sql.format(requestPayload['companyUID'])
        companySpecificSchemaCursor.execute(sql)
        companySpecificSchemaConnector.commit()

        #prepare IssueTracker-Table creation SQL query
        sql = dbQueries.issueTrackerTableCreation_sql.format(requestPayload['companyUID'],requestPayload['companyUID'],requestPayload['companyUID'])
        companySpecificSchemaCursor.execute(sql)
        companySpecificSchemaConnector.commit()

        #All tasks for Admin-Registeration done
        adminRegisterStatus = "success"
        companySpecificSchemaCursor.close()
        companySpecificSchemaConnector.close()
    except Exception as e:
        print(e)
        return {'status': adminRegisterStatus, 'endpoint': endpoint, 'companyUID': requestPayload['companyUID'],
                'message': 'Company registeration failed - Account Already exists', 'companyAdminEmail': requestPayload['companyAdminEmail']}

    return {'status':adminRegisterStatus,'endpoint':endpoint, 'companyUID':requestPayload['companyUID'], 'message':'Company Registered', 'companyAdminEmail':requestPayload['companyAdminEmail']}

#Admin-Login webservice
@admin.route('/login',methods=['POST'])
def adminLogin():

    adminLoginStatus = "failed"
    endpoint = "/admin/login"
    requestPayload = request.json

    #prepare admin-login query to verify credentials
    sql = dbQueries.adminLogin_sql
    val = (requestPayload['username'],requestPayload['password'])
    globalMySQLCursor.execute(sql,val)
    adminRecord = globalMySQLCursor.fetchone()

    if not adminRecord:
        return {'status':adminLoginStatus,'endpoint':endpoint,'message':'Incorrect Password / User not found'}
    else:
        adminLoginStatus="success"

    return {'status':adminLoginStatus,'endpoint':endpoint,'message':'Login Successful!','companyUID':adminRecord[0],'companyName':adminRecord[1],'companyAddress':adminRecord[2],'companyAdminEmail':adminRecord[3]}

@admin.route('/forgot-password',methods=['POST'])
def adminForgotPassword():
    adminFPStatus = "failed"
    endpoint = "/admin/forgot-password"

    return {'status':adminFPStatus,'endpoint':endpoint}
