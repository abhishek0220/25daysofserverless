import logging
import uuid
import os
import azure.functions as func
from azure.cosmos import exceptions, CosmosClient, PartitionKey

def new_item(name, dish, veg, vegen):
	sample_item = {
        'id': str(uuid.uuid4()),
        'name': name,
        'dish': dish,
        "vegetarian": veg,
	  	"vegen": vegen
	}
	return sample_item

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    con = 0
    try:
        req_body = req.get_json()
        name = req_body['name']
        dish = req_body['dish']
        veg = req_body['vegetarian']
        vegen = req_body['vegan']
    except:
        pass
    else:
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
        dish = new_item(name, dish, veg, vegen)
        items = [dish]
        for item in items:
            container.create_item(body=item)
        con = 1

    if (con == 1):
        return func.HttpResponse(f"Dish feeded")
    else:
        return func.HttpResponse(
             "Please pass a valid query in the request body",
             status_code=400
        )
