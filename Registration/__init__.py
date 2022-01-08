
import azure.functions as func
import re

from Registration.db_operations import checkIfEmailExists, registerUser


def main(req: func.HttpRequest) -> func.HttpResponse:

    email = req.params.get('email')
    password = req.params.get('password')
    firstName = req.params.get('firstName')
    lastName = req.params.get('lastName')
    dateOfBirth = req.params.get('dateOfBirth')
    education = req.params.get('education')
    address = req.params.get('address')
    gender = req.params.get('gender')

    if not (email and password and firstName and lastName and dateOfBirth and education and address and gender):
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
            firstName = req_body.get('firstName')
            lastName = req_body.get('lastName')
            dateOfBirth = req_body.get('dateOfBirth')
            education = req_body.get('education')
            address = req_body.get('address')
            gender = req_body.get('gender')

    if not email:
        return func.HttpResponse(
            "Email is not provided.",
            status_code=400
        )
    else:
        response = validateEmail(email)
        if response is not None:
            return response
    if not password:
        return func.HttpResponse(
            "Password is not provided.",
            status_code=400
        )
    else:
        response = validatePassword(password)
        if response is not None:
            return response
    if not firstName:
        return func.HttpResponse(
            "First name is not provided.",
            status_code=400
        )
    else:
        response = validateName(firstName, "first")
        if response is not None:
            return response
    if not lastName:
        return func.HttpResponse(
            "Last name is not provided.",
            status_code=400
        )
    else:
        response = validateName(lastName, "last")
        if response is not None:
            return response
    if not dateOfBirth:
        return func.HttpResponse(
            "Date of birth is not provided.",
            status_code=400
        )
    else:
        response = validateDate(dateOfBirth)
        if response is not None:
            return response
        
    if not education:
        return func.HttpResponse(
            "Education is not provided.",
            status_code=400
        )
    if not address:
        return func.HttpResponse(
            "Address is not provided.",
            status_code=400
        )
    if not gender:
        return func.HttpResponse(
            "Gender is not provided.",
            status_code=400
        )
    else:
        response = validateGender(gender)
        if response is not None:
            return response
    return registerUser(email, firstName, lastName, dateOfBirth, education, address, password, gender)
            
def validateDate(date):
	try:
		datetime.datetime.strptime(date, "%Y-%m-%d")
		return None
	except ValueError:
		return func.HttpResponse(
            "Please select a valid date of birth.",
            status_code=400
        )
                
def validateGender(gender):
    if (gender != 'Male' and gender != 'Female' and gender != 'Other' and gender != 'Prefer not to say' and gender == ''):
        return func.HttpResponse(
            "Please select a valid gender.",
            status_code=400
        )
    else:
        return None
    

def validateEmail(email):

    if checkIfEmailExists(email) == True:
        return func.HttpResponse(
            "Email already exists.",
            status_code=400
        )

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if(not (re.fullmatch(regex, email))):
        return func.HttpResponse(
            "Invalid email.",
            status_code=400
        )
    
    return None

def validatePassword(password):
    errorCode = -1
    responsemsg = [
        "Password is less than 8 characters",
        "Password must contain lower-case letters",
        "Password must contain uppercase letters",
        "Password must contain a number",
        "Password must contain a symbol",
        "Password must not contain whitespaces"
        ]
    isValid = True

    if (len(password) < 8):
        isValid = False
        errorCode = 0
    elif (not re.search("[a-z]", password)):
        isValid = False
        errorCode = 1
    elif not re.search("[A-Z]", password):
        isValid = False	
        errorCode = 2
    elif not re.search("[0-9]", password):
        isValid = False	
        errorCode = 3	
    elif not re.search("[_@$]", password):
        isValid = False
        errorCode = 4
    elif re.search("\s", password):
        isValid = False
        errorCode = 5
    
    if not isValid:
        errMsg = "Invalid Password - {}".format(responsemsg[errorCode])
        return func.HttpResponse(
            errMsg,
            status_code=400
        )

    return None

def validateName(name, str):
    regex = r'[a-zA-Z]{2,}'

    if(not (re.fullmatch(regex, str))):
        resp = "Invalid {} name".format(str)
        return func.HttpResponse(
            resp,
            status_code=400
        )

    return None

