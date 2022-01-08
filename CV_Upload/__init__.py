import logging

import azure.functions as func

from CV_Upload.db_operations import uploadCV


def main(req: func.HttpRequest) -> func.HttpResponse:

    userId = req.params.get('userId')
    jobTitle = req.params.get('jobTitle')
    jobOffers = req.params.get('jobOffers')
    cvFile = req.params.get('cvFile')
    if not (userId and jobTitle and jobOffers and cvFile):
        try:
            req_form = req.form
            req_files = req.files
        except ValueError:
            return func.HttpResponse(
                "Bad Request",
                status_code=400
            )
        else:
            userId = req_form.get('userId')
            jobTitle = req_form.get('jobTitle')
            jobOffers = req_form.get('jobOffers')
            cvFile = req_files.get('cvFile')

    if not userId:
        return func.HttpResponse(
            "Log in required.",
            status_code=400
        )
    
    if not jobTitle:
        return func.HttpResponse(
            "Job Title required.",
            status_code=400
        )
    
    if not jobOffers:
        return func.HttpResponse(
            "Job offers required.",
            status_code=400
        )

    if not cvFile:
        return func.HttpResponse(
            "CV file required.",
            status_code=400
        )
    
    return uploadCV(userId, jobTitle, jobOffers, cvFile)

    
