
from azure.functions._thirdparty.werkzeug.datastructures import FileStorage
from azure.functions._thirdparty.werkzeug.formparser import default_stream_factory
import pyodbc
import base64
import azure.functions as func
import io
import mimetypes

import logging


def connectToDatabase():
    server = 'cvlibrary-server.database.windows.net'
    database = 'CVLibraryDB'
    username = 'mg5u19'
    password = 'COMP3207@'
    driver= '{ODBC Driver 17 for SQL Server}'

    conn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = conn.cursor()
    return cursor

def uploadCV(userId: int, jobTitle: str, jobOffers: str, cvFile: FileStorage):
    cursor = connectToDatabase()
    data = cvFile.read()
    # logging.info(data)
    cursor.execute('INSERT INTO Cvs (userId, jobTitle, jobOffers, cvFile) VALUES(?,?,?,?)'
    , (userId, jobTitle, jobOffers, data))
    cursor.connection.commit()
    cursor.connection.close()
    if cursor.rowcount != 1:
        return func.HttpResponse(
            "Something went wrong with the CV upload. Please try again!",
            status_code=400
        )  
    else:
        return func.HttpResponse(
            "Upload was successful.",
            status_code=200
        ) 
