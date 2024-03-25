from dotenv import load_dotenv
from data_collector import DataCollector
from database_manager import DatabaseManager
import os
import time
import logging
import json

def load_routes(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

def main():
    load_dotenv(override=True)
    dsn = os.getenv('DB_URL')
    database_manager = DatabaseManager(dsn)
    
    base_url = "http://openapi.gbis.go.kr/ws/rest/buslocationservice?serviceKey=1234567890&routeId={}"
    resource_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")

    data_collector = DataCollector(base_url, resource_path)

    while True:
        buses = data_collector.collect_data()
        if buses:
            database_manager.save_data(buses)
            print(f"Loaded {len(buses)} bus data entries.")
        else:
            print("Can not collect bus data")
        time.sleep(60)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"Error in main: {e}")
