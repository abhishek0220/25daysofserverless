import logging
import azure.functions as func
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import os


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    id = str(req.route_params.get('id'))
    if id:
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
        for item in items:
            if(str(item['id']) == id):
                container.delete_item(item,item['name'])
                return func.HttpResponse(f"Deleted dish having {id}!")
        return func.HttpResponse(
             "Element not found",
             status_code=404
        )

    else:
        return func.HttpResponse(
             "Please pass a dish ID",
             status_code=400
        )
