from flask import Flask, request, jsonify, Blueprint
import mysql.connector
import dbQueries
import uuid
from database import *

user = Blueprint('user', __name__)


@user.route('/register', methods=['POST'])
def userRegister():
    endpoint = '/user/register'
    userRegsiterStatus = "failed"

    userId = str(uuid.uuid4())
    requestPayload = request.json

    #Check if company exists
    sql = dbQueries.lookupCompanyUIDForUserRegisteration_sql
    val = (requestPayload['companyName'],)
    globalMySQLCursor.execute(sql,val)
    companyUID = globalMySQLCursor.fetchone()

    if not companyUID:
        return {'status': userRegsiterStatus, 'endpoint': endpoint, 'message': 'Invalid Company Name / Contact company admin'}

    try:
        sql = dbQueries.userRegisteration_sql.format(companyUID[0])
        val = (userId,requestPayload['userName'],requestPayload['userEmail'],requestPayload['userPassword'])
        globalMySQLCursor.execute(sql,val)
        globalMySQLConnector.commit()
        userRegsiterStatus="success"
    except Exception as e:
        print(e)
        return {"endpoint": endpoint, 'status': userRegsiterStatus,'message' : 'User already exists for company!'}

    return {"endpoint": endpoint, 'status': userRegsiterStatus,'message' : 'User registered into company tenant!'}


@user.route('/login', methods=['POST'])
def userLogin():
    endpoint = '/user/login'
    userLoginStatus = "failed"
    requestPayload = request.json

    try:
        sql = dbQueries.lookupCompanyUIDForUserRegisteration_sql
        val = (requestPayload['companyName'],)
        globalMySQLCursor.execute(sql, val)
        companyUID = globalMySQLCursor.fetchone()

        if not companyUID:
            return {"endpoint": endpoint, 'status': userLoginStatus,'message': 'Company doesnot exist / Contact Admin'}

        sql = dbQueries.userLogin_sql.format(companyUID[0])
        val = (requestPayload['userEmail'],requestPayload['userPassword'])
        globalMySQLCursor.execute(sql,val)
        user = globalMySQLCursor.fetchone()

        if not user:
            return {"endpoint": endpoint, 'status': userLoginStatus,'message': 'Invalid Login Credentials! / User doesnot exists'}

        userLoginStatus = "success"
    except Exception as e:
        print(e)
        return {"endpoint": endpoint, 'status': userLoginStatus,'message' : 'Check login credentials, try again!'}

    return {"endpoint": endpoint, 'status': userLoginStatus,'message' : 'Login successful!','userName':user[0]}
