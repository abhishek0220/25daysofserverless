import logging
import os
import azure.functions as func
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials

subscription_key = os.environ["TEXT_ANALYTICS_SUBSCRIPTION_KEY"]
endpoint = os.environ["TEXT_ANALYTICS_ENDPOINT"]

def authenticateClient():
    credentials = CognitiveServicesCredentials(subscription_key)
    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint, credentials=credentials)
    return text_analytics_client

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    con = 0
    try:
        req_body = req.get_json()
    except:
        pass
    else:
        documents=[]
        index = 0 
        direc = []
        for ele in req_body:
            name = ele['who'] 
            message = ele['message']
            sample = {}
            sample['id'] = index
            sample['text'] = message
            documents.append(sample)
            li_ap = [name,message]
            direc.append(li_ap)
            index = index + 1
        client = authenticateClient()
        response = client.detect_language(documents=documents)
        for ele in response.documents:
            index = int(ele.id)
            documents[index]['language'] = ele.detected_languages[0].iso6391_name
        response = client.sentiment(documents=documents)
        out = []
        for ele in response.documents:
            index = int(ele.id)
            sample = {}
            sample['who'] = direc[index][0]
            sample['message'] = direc[index][1]
            sample['result'] = 'naughty'
            sample['sentiment'] = round(ele.score,3)
            if(ele.score>=0.5):
                sample['result'] = 'nice'
            out.append(sample)
        out = str(out)
        con = 1

    if con:
        return func.HttpResponse(f"{out}")
    else:
        return func.HttpResponse(
             "Please pass a valid JSON body",
             status_code=400
        )
