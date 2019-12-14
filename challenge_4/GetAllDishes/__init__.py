import logging
import os
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import azure.functions as func
import pprint

def getele(item, index):
    out = "Dish " + str(index) + "{\n"
    out0 = "\t id : " + item['id'] + "\n"
    out1 = "\t name : " + item['name'] + "\n" 
    out2 = "\t dish : " + item['dish'] + "\n" 
    out3 = "\t vegetarian : " + str(item['vegetarian']) + "\n" 
    out4 = "\t vegen : " + str(item['vegen']) + "\n" 
    out = out + out0 + out1 + out2 + out3 + out4 + "}"
    return out

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    endpoint = "https://localhost:8081"
    key = os.environ['key']
    client = CosmosClient(endpoint, key)
    database_name = 'AzureDatabase'
    database = client.create_database_if_not_exists(id=database_name)
    container_name = 'DishesContainer'
    container = database.create_container_if_not_exists(
        id=container_name, 
        partition_key=PartitionKey(path="/name"),
        offer_throughput=400
    )
    query = "SELECT * FROM ALL"
    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))
    out = ""
    index = 1
    for item in items:
        ele = getele(item,index)
        out = out + ele + "\n"
        index = index + 1
    return func.HttpResponse(
        body = out,
        status_code = 200
    )
