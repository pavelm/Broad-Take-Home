import logging
import time
from MBTARoutesFetcher import MBTARoutesFetcher, RailType
import os

from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")


logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.INFO)


    
def main():
    start = time.time()
   
    # create class object  
    mbtaRoutesFetcher = MBTARoutesFetcher(API_BASE_URL, API_KEY)

    # get all mbta_routes (an array of all mbta_routes with Light and Heavy Rail Types)
    mbta_routes = mbtaRoutesFetcher.fetch_mbta_routes([RailType.LIGHT, RailType.HEAVY])
    
    # get the long names from mbta_routes
    mbta_routes_long_names = mbtaRoutesFetcher.get_long_names(mbta_routes)
    
    # print the long names of the mbta routes
    list(map(print, mbta_routes_long_names))

    end = time.time()
    
    logging.info("Run time: " + str(end - start))

if __name__ == "__main__":
    main()
