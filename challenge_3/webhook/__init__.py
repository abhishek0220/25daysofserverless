import logging
import azure.functions as func
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import uuid

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    con =0
    try:
        req_body = req.get_json()
        path_url = req_body['repository']['full_name']
        files_added = req_body['commits'][0]['added']
    except:
        pass
    else:
        url = "https://raw.githubusercontent.com/"
        res=[]
        for i in files_added:
            if(i[-4:]!=".png"):
                continue
            filename = i
            final_url = url + path_url + "/master/" + filename
            res.append(final_url)
        con = 1

    if con:
        if(len(res)>0):
            na = "Image Saved"
            endpoint = "endpoint"
            key = 'key'
            client = CosmosClient(endpoint, key)
            database_name = 'imagedata'
            database = client.create_database_if_not_exists(id=database_name)
            container_name = 'information'
            container = database.create_container_if_not_exists(
                id=container_name, 
                partition_key=PartitionKey(path="/name"),
                offer_throughput=400
            )
            dat = {
                'id' : str(uuid.uuid4()),
                'url': ""
            }
            items = res
            for item in items:
                dat['url'] = item
                container.create_item(body=dat)
        else:
            na = "No Image"
        return func.HttpResponse(na)
    else:
        return func.HttpResponse(
             "Not valid request",
             status_code=400
        )
