from MBTARoutesFetcher import MBTARoutesFetcher, RailType
from MBTAStopsFetcher import MBTAStopsFetcher
import os
from dotenv import load_dotenv
import logging
import time
from problem2 import get_all_stops, get_connecting_stops, get_connecting_stops_and_route

logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.INFO)

# Load environment variables from .env
load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")


def get_line_dict(connecting_stops, route_stops):
    line_dict = {}

    # Create a set of all route IDs
    all_route_ids = set(route_stops.keys())

    for route_id in all_route_ids:
        line_dict[route_id] = []

        for stops_list in connecting_stops.values():
            if route_id in stops_list:
                # Add all unique route IDs from the stops_list to the current route_id's list
                line_dict[route_id].extend(set(stops_list) - {route_id})

    return line_dict



# https://stackabuse.com/courses/graphs-in-python-theory-and-implementation/lessons/depth-first-search-dfs-algorithm/
# depth first search graph searching algorithm traverses as far as it can go down one branch until it has to backtrack
def dfs(start, target, line_dict, path=[], visited=set()):

    path.append(start)
    visited.add(start)

    if start == target:
        return path

    for neighbour in line_dict[start]:

        if neighbour not in visited:

            if target in line_dict[start]:
                path.append(target)
                return path

            result = dfs(neighbour, target, line_dict, path, visited)
            if result is not None:
                return result

    path.pop()
    return None

def find_line_for_station(station, dict_of_routes_and_stops):
    for subway_route, subway_stops in dict_of_routes_and_stops.items():
        if station in subway_stops:
            return subway_route
    return None

# finds the path of a starting and final destination
def find_subway_path(start, finish, dict_of_routes_and_stops, line_dict):

    starting_line = find_line_for_station(start, dict_of_routes_and_stops)
    if starting_line is None:
        logging.error("Starting location does not exist")
        return None

    # Find the subway line for the finishing station
    finish_line = find_line_for_station(finish, dict_of_routes_and_stops)
    if finish_line is None:
        logging.error("Finish location does not exist")
        return None

    return dfs(starting_line, finish_line, line_dict)


def main():
    start_location = input("Starting point station: ")

    finish_location = input("Final point station: ")

    start = time.time()

    mbtaRoutesFetcher = MBTARoutesFetcher(API_BASE_URL, API_KEY)
    mbtaStopsFetcher = MBTAStopsFetcher(API_BASE_URL, API_KEY)

    # get all mbta_routes (an array of all mbta_routes with Light and Heavy Rail Types)
    mbta_routes = mbtaRoutesFetcher.fetch_mbta_routes([RailType.LIGHT, RailType.HEAVY])

    list_of_subway_route_ids = mbtaRoutesFetcher.get_route_data(mbta_routes, ['id'])
    mbta_routes_long_names = mbtaRoutesFetcher.get_route_data(mbta_routes, ['attributes', 'long_name'])

    # get the routes and their corresponding stops
    dict_of_routes_and_stops = mbtaStopsFetcher.run_get_dict_of_routes_and_stops(list_of_subway_route_ids, mbta_routes_long_names)

    # all stops
    all_stops = get_all_stops(dict_of_routes_and_stops)

    # all the connecting stops 
    connecting_stops = get_connecting_stops(all_stops)

    # every connecting stop and its associated route
    connecting_stops_and_route = get_connecting_stops_and_route(dict_of_routes_and_stops, connecting_stops)

    line_dict = get_line_dict(connecting_stops_and_route, dict_of_routes_and_stops)


    logging.info(find_subway_path(start_location, finish_location, dict_of_routes_and_stops, line_dict))

    end = time.time()
    # Alewife, Lechmere

    logging.info("Run time: " + str(end - start))


if __name__ == '__main__':
    main()