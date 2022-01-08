import logging
import json
import azure.functions as func

from SearchCVbyID.db_operations import searchCvByCvId


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    cvId = req.params.get('cvId')
    if not cvId:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            cvId = req_body.get('cvId')

    if not cvId:
        return func.HttpResponse(
            "Enter the id of the CV",
            status_code=400
        )
    else:
        result = searchCvByCvId(cvId)
        return func.HttpResponse(
             json.dumps(result),
             status_code=200
        )
