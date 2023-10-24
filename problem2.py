import logging
import time
from collections import Counter, OrderedDict
from MBTARoutesFetcher import MBTARoutesFetcher, RailType
from MBTAStopsFetcher import MBTAStopsFetcher
from dotenv import load_dotenv
import os

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")

logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.INFO)


# get all the subway stops
def get_all_stops(route_stops):
   return [stop for stops in route_stops.values() for stop in stops]

def get_connecting_stops(all_stops):
   return dict(sorted(Counter(all_stops).items(), key=lambda item: item[1], reverse=True))

def get_connecting_stops_and_route(route_stops, stop_counts):
    connecting_stops = {}
    
    for stop, count in stop_counts.items():
        if count > 1:
            connecting_stops[stop] = [route for route, stops in route_stops.items() if stop in stops]

    return connecting_stops

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
    logging.info("Number of stops: %s\n", min_elements)

def log_multi_route_stops(subway_stops):
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

    # get all mbta_routes (an array of all mbta_routes with Light and Heavy Rail Types)
    mbta_routes = mbtaRoutesFetcher.fetch_mbta_routes([RailType.LIGHT, RailType.HEAVY])

    list_of_subway_route_ids = mbtaRoutesFetcher.get_route_data(mbta_routes, ['id'])

    # get the routes and their corresponding stops
    route_stops = mbtaStopsFetcher.get_route_stops(list_of_subway_route_ids)

    most_and_least_elements(route_stops)

    all_stops = get_all_stops(route_stops)

    connecting_stops = get_connecting_stops(all_stops)

    connecting_stops_and_route = get_connecting_stops_and_route(route_stops, connecting_stops)
    

    log_multi_route_stops(connecting_stops_and_route)

    end = time.time()

    logging.info("Run time: " + str(end - start))


if __name__ == "__main__":
    main()