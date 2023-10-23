import logging
import time
from enum import IntEnum
import requests
import asyncio
import aiohttp

logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.INFO)

# create an enumeration for RailType
class RailType(IntEnum):
    LIGHT = 0
    HEAVY = 1

class MBTAStopsFetcher:
    def __init__(self, api_base_url, api_key):
        self.api_base_url = api_base_url
        self.api_key = api_key

    

    # Coroutines are computer program components that allow execution
    # to be suspended and resumed, generalizing subroutines for cooperative multitasking
    # https://en.wikipedia.org/wiki/Coroutine
    # we can get a set of all scheduled and running tasks
    def get_tasks(self, session, list_of_subway_route_ids):
        tasks = []
        for subway_id in list_of_subway_route_ids:
            tasks.append(asyncio.create_task(
                session.get(f'{self.api_base_url}/stops?filter[route]=' + str(subway_id),
                        headers={"x-api-key": self.api_key}, ssl=False)))
        return tasks


    # gets a dictionary of routes and their corresponding stops
    # https://www.youtube.com/watch?v=nFn4_nA_yk8
    # https://groups.google.com/g/massdotdevelopers/c/WiJUyGIpHdI
    async def get_dict_of_routes_and_stops(self, list_of_subway_route_ids):
        async with aiohttp.ClientSession() as session:

            tasks = self.get_tasks(session, list_of_subway_route_ids)
            data = await asyncio.gather(*tasks)

            # create an empty dictionary
            route_stop_dict = {}

            for index in range(len(data)):
                # get teh subway line data
                subway_line_data = await (data[index]).json()

                subway_line_data = subway_line_data['data']

                route_stop_dict[list_of_subway_route_ids[index]] = []

                for stops in subway_line_data:
                    route_stop_dict[list_of_subway_route_ids[index]].append((stops['attributes']['name']))

            return route_stop_dict
        
    def get_route_stops(self, list_of_subway_route_ids):
        return asyncio.run(self.get_dict_of_routes_and_stops(list_of_subway_route_ids))
