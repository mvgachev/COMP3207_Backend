import logging
import json
import azure.functions as func

from GetUserById.db_operations import fetchUserByid


def main(req: func.HttpRequest) -> func.HttpResponse:

    userid = req.params.get('userid')
    if not userid:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            userid = req_body.get('userid')

    if not userid:
        return func.HttpResponse(
            "Please input a user id",
            status_code=400
        )
    else:
        id = int(userid)
        res = fetchUserByid(id)
        if(type(res) is dict):
            return func.HttpResponse(
                json.dumps(res),
                status_code=200
            )
        else:    
            return func.HttpResponse(
                res,
                status_code=400
            )
