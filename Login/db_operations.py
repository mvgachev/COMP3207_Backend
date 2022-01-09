import pyodbc

from Registration.db_operations import getUserWithEmail


def connectToDatabase():
    server = 'cvlibrary-server.database.windows.net'
    database = 'CVLibraryDB'
    username = 'mg5u19'
    password = 'COMP3207@'
    driver= '{ODBC Driver 17 for SQL Server}'

    conn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = conn.cursor()
    return cursor

def getPasswordOfUser(user):
    cursor = connectToDatabase()
    userId = user[0]
    cursor.execute('SELECT * FROM Passwords WHERE userId = ?', userId)
    userAuth = cursor.fetchone()
    return userAuth[1]

def checkIfPasswordMatch(password: str, email: str):
    user = getUserWithEmail(email)
    if getPasswordOfUser(user) == password:
        return True
    else:
        return False
