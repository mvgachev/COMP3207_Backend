import pyodbc
import logging
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



def getUserWithEmail(email: str):
    cursor = connectToDatabase()
    cursor.execute('SELECT * FROM Users WHERE email = ?', email)
    user = cursor.fetchone()
    
    return user

def checkIfEmailExists(email: str):
    user = getUserWithEmail(email)
    if user is None:
        return False
    else:
        return True

def registerUser(email: str, firstName: str, lastName: str, dateOfBirth: str, education: str, address: str, password: str):
    cursor = connectToDatabase()
    cursor.execute('INSERT INTO Users (email, firstName, lastName, dateOfBirth, education, address) VALUES(?,?,?,?,?,?)'
    , (email, firstName, lastName, dateOfBirth, education, address))
    cursor.connection.commit()
    if cursor.rowcount != 1:
        return func.HttpResponse(
            "Something went wrong with the registration request. Please try again!",
            status_code=400
        )  
    
    userId = getUserId(email)
    logging.info('Last user id was ' + str(userId))
    cursor.execute('INSERT INTO Passwords (userId, password) VALUES(?,?)', (userId, password))
    cursor.connection.commit()

    if cursor.rowcount == 1:
        return func.HttpResponse(
            "Registration was successful.",
            status_code=200
        )
    else:
        return func.HttpResponse(
            "Something was wrong with the registration request. Please try again!",
            status_code=400
        )      

def getUserId(email):
    cursor = connectToDatabase()
    cursor.execute('SELECT * FROM Users WHERE email = ?', email)
    user = cursor.fetchone()
    logging.info(email)
    logging.info(user)
    return user[0]