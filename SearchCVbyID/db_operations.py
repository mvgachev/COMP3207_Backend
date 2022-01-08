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


def searchCvBycvId(cvId):
    cursor = connectToDatabase()
    query = "SELECT * FROM Cvs WHERE cvId = ?"
    cursor.execute(query,cvId)
    
    sql_res = cursor.fetchall()
    columns = ['cvId','userId','jobTitle','jobOffers','cvFile']
    results = []
    logging.info(type(results))

    for r in sql_res:
        results.append(dict(zip(columns,r)))
    
    for r in results:
        logging.info(type(r))
        logging.info(r)
        r['cvFile'] = r['cvFile'].decode("utf-8")
        logging.info(r)
    
    cursor.commit()
    cursor.close()
    return results 


