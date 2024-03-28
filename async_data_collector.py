import aiohttp
import asyncio
import xmljson
from xml.etree import ElementTree as ET
from datetime import datetime
import pytz
import json
import logging


class AsyncDataCollector:
    def __init__(self, base_url, resources_path):
        self.base_url = base_url
        self.resources_path = resources_path
        self.kst_zone = pytz.timezone('Asia/Seoul')
        self.session = aiohttp.ClientSession()
        
        with open(f"{self.resources_path}/station.json", "r") as f:
            self.station_map = json.load(f)

        with open(f"{self.resources_path}/crawlering_route_ids.json", "r") as f:
            self.route_ids = json.load(f)

    async def fetch_data(self, route_id, route_name):
        buses = []
        url = self.base_url.format(route_id)
        async with self.session.get(url) as response:
            xml_str = await response.text()
            xml_element = ET.fromstring(xml_str)
            json_data = xmljson.parker.data(xml_element)
            
            if 'msgBody' not in json_data or 'busLocationList' not in json_data['msgBody']:
                logging.warning(f"No busLocationList found in the response for route_id {route_id}")
                return buses
            
            bus_locations = json_data["msgBody"]["busLocationList"]
            if not isinstance(bus_locations, list):
                logging.error(f"Unexpected busLocationList type for route_id {route_id}: {type(bus_locations)}")
                return buses
            
            if json_data["msgHeader"]["resultCode"] != 0:
                logging.warning(f"Request ignored or result is unexpected: {json_data}")
                return buses

            for data in bus_locations:
                time_str = datetime.now(pytz.utc).astimezone(self.kst_zone).strftime("%Y-%m-%d %H:%M:%S")
                time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                plate_no = data.get("plateNo")
                plate_type = data.get("plateType")
                remain_seat_cnt = data.get("remainSeatCnt", -1)
                station_id = str(data.get("stationId"))
                station_name = self.station_map.get(str(station_id), "Unknown Station")
                station_seq = data.get("stationSeq")
                
                buses.append({
                    "time": time,
                    "plate_no": plate_no,
                    "plate_type": plate_type,
                    "remain_seat_cnt": remain_seat_cnt,
                    "route_id": route_id,
                    "route_name": route_name,
                    "station_id": station_id,
                    "station_name": station_name,
                    "station_seq": station_seq
                })

        return buses

    async def collect_data(self):
        tasks = [self.fetch_data(route_id, route_name) for route_id, route_name in self.route_ids]
        results = await asyncio.gather(*tasks)

        buses = [bus for result in results for bus in result if result]
        return buses
    
    async def open(self):
        if not self.session:
            self.session = await aiohttp.ClientSession()

    async def close(self):
        await self.session.close()
