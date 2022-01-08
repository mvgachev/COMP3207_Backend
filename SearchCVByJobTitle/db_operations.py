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


def searchCvByJobTitle(jobTitle):
    cursor = connectToDatabase()
    query = "SELECT cvId, userId, jobTitle, jobOffers FROM Cvs WHERE jobTitle = ?"
    cursor.execute(query,jobTitle)
    
    sql_res = cursor.fetchall()
    columns = ['cvId','userId','jobTitle','jobOffers']
    results = []

    for r in sql_res:
        results.append(dict(zip(columns,r)))
    
    
    cursor.commit()
    cursor.close()
    return results 


