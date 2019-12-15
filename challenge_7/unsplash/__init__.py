import logging
import azure.functions as func
import os
import requests

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    text = req.params.get('text')
    if not text:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            text = req_body.get('text')

    if text:
        access_key = os.environ['UNSPLASH_ACCESS_KEY']
        secret_key = os.environ['UNSPLASH_SECRET_KEY']
        url = "https://api.unsplash.com/search/photos?client_id=" + access_key + "&client_secret=" + secret_key + "&query=" + text + "&count=1"
        res_get = requests.get(url)
        res_json = res_get.json()
        img = res_json['results'][0]['urls']['small']
        return func.HttpResponse(f"Search for image with keywords {text}. Got url: {img}")
    else:
        return func.HttpResponse(
             "Please pass a text on the query string or in the request body",
             status_code=400
        )
