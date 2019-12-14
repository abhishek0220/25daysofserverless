import logging
import azure.functions as func
import os
from azure.cosmos import exceptions, CosmosClient, PartitionKey


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    id = str(req.route_params.get('id'))
    try:
        req_body = req.get_json()
    except:
        pass
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
                try:
                    req_body = req.get_json()
                except:
                    return func.HttpResponse(
                        "Invalid body passes",
                        status_code=404
                    )
                new_it = item
                for par in req_body:
                    if(req_body.get(par)):
                        new_it[par] = req_body[par]
                container.create_item(body=new_it)
                return func.HttpResponse(f"Updated dish having id {id}")
        return func.HttpResponse(
             "Element not found",
             status_code=404
        )

    else:
        return func.HttpResponse(
             "Please pass a dish ID",
             status_code=400
        )
