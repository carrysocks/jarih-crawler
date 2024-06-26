import asyncio
from dotenv import load_dotenv
from async_data_collector import AsyncDataCollector
from async_database_manager import AsyncDatabaseManager
import os
import time


async def async_main():
    load_dotenv(override=True)
    dsn = os.getenv('DB_URL')
    
    base_url = "http://openapi.gbis.go.kr/ws/rest/buslocationservice?serviceKey=1234567890&routeId={}"
    resource_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")

    database_manager = AsyncDatabaseManager(dsn)
    data_collector = AsyncDataCollector(base_url, resource_path)
    
    await data_collector.open()
    while True:   
        start_collect_time = time.time()
        buses = await data_collector.collect_data()
        end_collect_time = time.time()
        
        if buses:
            print("Collect finish. Saving...")
            start_save_time = time.time()
            await database_manager.save_data(buses)
            end_save_time = time.time()
            print(f"Loaded {len(buses)} bus data entries.")
        else:
            print("Cannot collect bus data")        
        
        elapsed_collect_time = end_collect_time - start_collect_time
        elapsed_save_time = end_save_time - start_save_time
        print(f"비동기 수집 시간 : {elapsed_collect_time}초, 비동기 저장 시간 : {elapsed_save_time}초, 비동기 총 시간 : {elapsed_collect_time + elapsed_save_time}초")
        
        print("Sleeping...")
        await asyncio.sleep(60)

