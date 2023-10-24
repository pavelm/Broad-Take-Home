import logging
from enum import IntEnum
import asyncio
import aiohttp

# Set up logging
logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.INFO)

# Create an enumeration for RailType
class RailType(IntEnum):
    LIGHT = 0
    HEAVY = 1

class MBTAStopsFetcher:
    def __init__(self, api_base_url, api_key):
        self.api_base_url = api_base_url
        self.api_key = api_key

    # Create a coroutine to fetch data from the API
    async def fetch_data(self, session, subway_id):
        url = f"{self.api_base_url}/stops?filter[route]={subway_id}"
        headers = {"x-api-key": self.api_key}
        async with session.get(url, headers=headers, ssl=False) as response:
            return await response.json()

    # Get a list of tasks for fetching data
    def get_tasks(self, session, list_of_subway_route_ids):
        return [self.fetch_data(session, subway_id) for subway_id in list_of_subway_route_ids]

    # Get a dictionary of routes and their corresponding stops
    async def get_dict_of_routes_and_stops(self, list_of_subway_route_ids, mbta_routes_long_names):
        async with aiohttp.ClientSession() as session:
            tasks = self.get_tasks(session, list_of_subway_route_ids)
            data = await asyncio.gather(*tasks)

            route_stop_dict = {}

            for index, subway_id in enumerate(list_of_subway_route_ids):
                subway_line_data = data[index]["data"]
                route_name = mbta_routes_long_names[index]
                stops = [stop["attributes"]["name"] for stop in subway_line_data]
                route_stop_dict[route_name] = stops

            return route_stop_dict

    def run_get_dict_of_routes_and_stops(self, list_of_subway_route_ids, mbta_routes_long_names):
        return asyncio.run(self.get_dict_of_routes_and_stops(list_of_subway_route_ids, mbta_routes_long_names))
