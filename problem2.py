import logging
import time
from MBTARoutesFetcher import MBTARoutesFetcher
from MBTAStopsFetcher import MBTAStopsFetcher
from MBTAConnectingFetcher import MBTAConnectingFetcher
from RailTypeEnum import RailType
from dotenv import load_dotenv
import os

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")

logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.INFO)


def most_and_least_elements(dictionary):
    if not dictionary:
        print("The dictionary is empty.")
        return

    max_key = max(dictionary, key=lambda key: len(dictionary[key]))
    min_key = min(dictionary, key=lambda key: len(dictionary[key]))

    max_elements = len(dictionary[max_key])
    min_elements = len(dictionary[min_key])

    logging.info("Route with the most number of stops: %s", max_key)
    logging.info("Number of stops: %s", max_elements)

    print()

    logging.info("Route with the least number of stops: %s", min_key)
    logging.info("Number of stops: %s", min_elements)

def log_subway_stops_and_routes(subway_stops):
    if not subway_stops:
        logging.info("The subway stops dictionary is empty.")
        return

    multi_route_stops = {stop: routes for stop, routes in subway_stops.items() if len(routes) >= 2}

    for stop, routes in multi_route_stops.items():
        logging.info(f"Stop: {stop}")
        logging.info(f"Routes: {', '.join(routes)}")
        print()


def main():
    start = time.time()

    # gets the list of subway route ids
    # create class object  
    mbtaRoutesFetcher = MBTARoutesFetcher(API_BASE_URL, API_KEY)
    mbtaStopsFetcher = MBTAStopsFetcher(API_BASE_URL, API_KEY)
    mbtaConnectingFetcher = MBTAConnectingFetcher(API_BASE_URL, API_KEY)

    # get all mbta_routes (an array of all mbta_routes with Light and Heavy Rail Types)
    mbta_routes = mbtaRoutesFetcher.fetch_mbta_routes([RailType.LIGHT, RailType.HEAVY])

    list_of_subway_route_ids = mbtaRoutesFetcher.get_route_data(mbta_routes, ['id'])
    mbta_routes_long_names = mbtaRoutesFetcher.get_route_data(mbta_routes, ['attributes', 'long_name'])

    # get the routes and their corresponding stops
    dict_of_routes_and_stops = mbtaStopsFetcher.run_get_dict_of_routes_and_stops(list_of_subway_route_ids, mbta_routes_long_names)

    most_and_least_elements(dict_of_routes_and_stops)

    connecting_stops = mbtaConnectingFetcher.get_connecting_stops(dict_of_routes_and_stops)

    connecting_stops_and_route = mbtaConnectingFetcher.get_connecting_stops_and_route(dict_of_routes_and_stops, connecting_stops)
    
    log_subway_stops_and_routes(connecting_stops_and_route)

    end = time.time()

    logging.info("Run time: " + str(end - start))


if __name__ == "__main__":
    main()