import logging

import azure.functions as func
from Login.db_operations import checkIfPasswordMatch

from Registration.db_operations import checkIfEmailExists
import logging



def main(req: func.HttpRequest) -> func.HttpResponse:

    email = req.params.get('email')
    password = req.params.get('password')
    if not (email and password):
        try:
            req_body = req.get_json()
        except ValueError:
            return func.HttpResponse(
                "Bad Request",
                status_code=400
            )
        else:
            email = req_body.get('email')
            password = req_body.get('password')

    if not email:
        return func.HttpResponse(
            "Email is not provided.",
            status_code=400
        )
    else:
        response = checkEmail(email)
        if response is not None:
            return response
    if not password:
        return func.HttpResponse(
            "Password is not provided.",
            status_code=400
        )
    else:
        return checkPassword(password, email)
            

def checkEmail(email):

    if checkIfEmailExists(email) == False:
        logging.info("Email does not exist.")
        return func.HttpResponse(
            "User with this email does not exist.",
            status_code=401
        )
    else:
        return None

def checkPassword(password, email):

    if checkIfPasswordMatch(password, email) == False:

        return func.HttpResponse(
            "Password is incorrect",
            status_code=401
        )
    else:
        return func.HttpResponse(
            "You have logged in successfully",
            status_code=200
        )                


