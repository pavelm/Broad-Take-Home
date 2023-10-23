import logging
from enum import IntEnum
import requests


logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.INFO)

# create an enumeration for RailType
class RailType(IntEnum):
    LIGHT = 0
    HEAVY = 1

class MBTARoutesFetcher:
    def __init__(self, api_base_url, api_key):
        self.api_base_url = api_base_url
        self.api_key = api_key

    def fetch_mbta_routes(self, rail_types):
        # converts the enum value to it's integer type and joins all by comma
        type_filter = ",".join(map(lambda x: str(x.value), rail_types))
   
        # endpoint for MBTA API
        endpoint = f'{self.api_base_url}/routes?filter[type]={type_filter}'
    
        try:
            response = requests.get(endpoint, headers={"x-api-key": self.api_key})
            # returns an HTTPError object if an error has occured during process
            response.raise_for_status()
            return response.json()['data']
    
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch data from MBTA API: {str(e)}")
            return []
   

    # appending each attribute to the json response 
    def get_nested_value(self, response, attribute):
        for key in attribute:
            response = response[key]
        return response
    
    # capable of reaching any part of data without creating duplicate functions appending different attributes to the end of the json object
    def get_route_data(self, subway_routes, attributes):
        return list(map(lambda subway_route: self.get_nested_value(subway_route, attributes), subway_routes))


