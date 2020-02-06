import logging
import azure.functions as func
from github import Github
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    req_body = req.get_json()
    action = req_body.get('action')
    if action != 'opened':
        return func.HttpResponse(
            "Not an opened issue",
            status_code=204
        )
    github = Github(os.environ["GITHUB_PAT"])
    repo = github.get_repo("abhishek0220/Support_Repo_for_25daysofserverless")
    issue = repo.get_issue(number=req_body['issue']['number'])
    username = req_body['issue']['user']['login']
    issue.create_comment('Thank you @' + username + '  you for submitting this issue. ' +'We will take this on board and get back to you shortly!')
    return func.HttpResponse(
        "Thank you",
        status_code=200
    )
