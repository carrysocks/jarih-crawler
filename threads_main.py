from dotenv import load_dotenv
import os
import time
import json

from threads_data_collector import ThreadsDataCollector
from threads_database_manager import ThreadsDatabaseManager


def load_routes(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def threads_main():
    load_dotenv(override=True)
    dsn = os.getenv('DB_URL')

    base_url = "http://openapi.gbis.go.kr/ws/rest/buslocationservice?serviceKey=1234567890&routeId={}"
    resource_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")

    database_manager = ThreadsDatabaseManager(dsn)
    data_collector = ThreadsDataCollector(base_url, resource_path)

    while True:
        start_collect_time = time.time()
        buses = data_collector.collect_data()
        end_collect_time = time.time()
        if buses:
            print("Finish Collecting. Saving...")
            start_save_time = time.time()
            database_manager.save_data(buses)
            end_save_time = time.time()
            print(f"Loaded {len(buses)} bus data entries.")
        else:
            print("Cannot collect bus data")

        elapsed_collect_time = end_collect_time - start_collect_time
        elapsed_save_time = end_save_time - start_save_time
        elapsed_all_time = elapsed_collect_time + elapsed_save_time
        print(
            f"멀티 스레딩 수집 시간 : {elapsed_collect_time}초, 멀티 스레딩 저장 시간 : {elapsed_save_time}초, 멀티 스레딩 총 시간 : {elapsed_all_time}초"
        )
        print("Sleeping...")
        time.sleep(60)
