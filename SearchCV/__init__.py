import logging
import json
import azure.functions as func

from SearchCV.db_operations import searchCvByJobTitle


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    jobTitle = req.params.get('jobTitle')
    if not jobTitle:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            jobTitle = req_body.get('jobTitle')

    if not jobTitle:
        return func.HttpResponse(
            "Enter Job Title",
            status_code=400
        )
    else:
        list = searchCvByJobTitle(jobTitle)
        return func.HttpResponse(
             json.dumps(list),
             status_code=200
        )
