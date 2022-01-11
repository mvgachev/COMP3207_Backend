import logging
import json
import azure.functions as func

from SearchFirstKCvs.db_operations import fetchFirstKCvs


def main(req: func.HttpRequest) -> func.HttpResponse:

    k = req.params.get('k')
    n = req.params.get('n')
    if not k:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            k = req_body.get('k')
    if not n:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            n = req_body.get('n')
    
    if not k:
        return func.HttpResponse(
            "Invalid Range - Wrong / Missing Starting index",
            status_code=400
        )
    
    if not n:
        return func.HttpResponse(
            "Invalid Range - Wrong / Missing End Index",
            status_code=400
        )

    start_index = int(k)
    end_index = int(n)

    if start_index <= 0:
        return func.HttpResponse(
            "Please input a number greater than 0 for start of range",
            status_code=400)
    if end_index <= 0:
        return func.HttpResponse(
            "Please enter a number greater than 0 for end of range",
            status_code=400
        )
    list = fetchFirstKCvs(start_index,end_index)
    return func.HttpResponse(
        json.dumps(list),
        status_code=200
    )
