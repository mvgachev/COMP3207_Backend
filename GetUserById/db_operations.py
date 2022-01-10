import pyodbc
import logging
import json
import azure.functions as func


def connectToDatabase():
    server = 'cvlibrary-server.database.windows.net'
    database = 'CVLibraryDB'
    username = 'mg5u19'
    password = 'COMP3207@'
    driver= '{ODBC Driver 17 for SQL Server}'

    connection = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = connection.cursor()
    return cursor

def fetchUserByid(id):
    cursor = connectToDatabase()
    query = "SELECT lastName, firstName, education, gender FROM Users WHERE id = ?"
    cursor.execute(query,id)
    
    sql_res = cursor.fetchall()
    if not sql_res:
        return "No Such User ID exists"
    else:
        columns = ['lastName','firstName','education','gender']
        result = dict(zip(columns,sql_res[0]))
        return result
