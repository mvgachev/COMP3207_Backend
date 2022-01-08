import logging
import json
import azure.functions as func

from SearchCV.db_operations import searchCvByJobTitle


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    cvId = req.params.get('cvId')
    if not jobTitle:
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
        list = searchCvBycvId(cvId)
        return func.HttpResponse(
             json.dumps(list),
             status_code=200
        )
