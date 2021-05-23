import mysql.connector
import dbQueries


try:
    globalMySQLConnector = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="aditya"
    )
    dbStatus = "MySQL server is up and running!"
    status = "success"
    globalMySQLCursor = globalMySQLConnector.cursor()
    print('***DB Started***')
except Exception as e:
    print('Error occurred : ' + e)
    dbStatus = "MySQL server is not running"
    status = "failed"
