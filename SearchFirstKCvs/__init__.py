import logging
import json
import azure.functions as func

from SearchFirstKCvs.db_operations import fetchFirstKCvs


def main(req: func.HttpRequest) -> func.HttpResponse:

    k = req.params.get('k')
    if not k:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            k = req_body.get('k')

    to_get = int(k)

    if to_get <= 0:
        return func.HttpResponse(
            "Please input a number greater than 0",
            status_code=400)
    else:
        list = fetchFirstKCvs(to_get)
        return func.HttpResponse(
            json.dumps(list),
            status_code=200
        )
