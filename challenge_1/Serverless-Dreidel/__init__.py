import logging
import random
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    index = random.randint(0,3)
    values = ['ג','ה','ש','נ']
    out =str(values[0])
    return func.HttpResponse(out)
