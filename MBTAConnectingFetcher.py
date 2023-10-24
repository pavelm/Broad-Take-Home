import logging
from collections import Counter


logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.INFO)


class MBTAConnectingFetcher:
    def __init__(self, api_base_url, api_key):
        self.api_base_url = api_base_url
        self.api_key = api_key


    def get_all_stops(self, route_stops):
        all_stops = []

        for stops in route_stops.values():
            if isinstance(stops, dict):
                self.get_all_stops(stops, all_stops)
            elif isinstance(stops, list):
                all_stops.extend(stops)

        return all_stops

    def get_connecting_stops(self, route_stops, min_count=2):
        all_stops = self.get_all_stops(route_stops)

        stop_counts = Counter(all_stops)

        # Filter stops based on the minimum count
        filtered_stops = {stop: count for stop, count in stop_counts.items() if count >= min_count}

        # Sort the stops by count in descending order
        sorted_stops = dict(sorted(filtered_stops.items(), key=lambda item: item[1], reverse=True))

        return sorted_stops

    def get_connecting_stops_and_route(self, route_stops, stop_counts):
        connecting_stops = {}
    
        for stop, count in stop_counts.items():
            if count > 1:
                connecting_stops[stop] = [route for route, stops in route_stops.items() if stop in stops]

        return connecting_stops