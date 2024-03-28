import json
import logging
import threading
import xml.etree.ElementTree as ET
from datetime import datetime

import pytz
import requests
import xmljson


def _load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


class ThreadsDataCollector:
    def __init__(self, base_url, resources_path):
        self.base_url = base_url
        self.resources_path = resources_path
        self.kst_zone = pytz.timezone('Asia/Seoul')
        self.station_map = _load_json(f"{self.resources_path}/station.json")
        self.route_ids = _load_json(f"{self.resources_path}/crawlering_route_ids.json")
        self.buses = []
        self.lock = threading.Lock()

    def clear_data(self):
        self.buses = []

    def _parse_bus_data(self, bus_data, route_id, route_name):
        time_str = datetime.now(pytz.utc).astimezone(self.kst_zone).strftime("%Y-%m-%d %H:%M:%S")
        time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        plate_no = bus_data.get("plateNo")
        plate_type = bus_data.get("plateType")
        remain_seat_cnt = bus_data.get("remainSeatCnt", -1)
        station_id = str(bus_data.get("stationId"))
        station_name = self.station_map.get(str(station_id), "Unknown Station")
        station_seq = bus_data.get("stationSeq")

        return {
            "time": time,
            "plate_no": plate_no,
            "plate_type": plate_type,
            "remain_seat_cnt": remain_seat_cnt,
            "route_id": route_id,
            "route_name": route_name,
            "station_id": station_id,
            "station_name": station_name,
            "station_seq": station_seq
        }

    def fetch_data(self, route_id, route_name):
        url = self.base_url.format(route_id)
        response = requests.get(url)
        xml_str = response.text
        xml_element = ET.fromstring(xml_str)
        json_data = xmljson.parker.data(xml_element)

        if 'msgBody' not in json_data or 'busLocationList' not in json_data['msgBody']:
            logging.warning(f"No busLocationList found in the response for route_id {route_id}")
            return

        bus_locations = json_data["msgBody"]["busLocationList"]
        if not isinstance(bus_locations, list):
            logging.error(f"Unexpected busLocationList type for route_id {route_id}: {type(bus_locations)}")
            return

        if json_data["msgHeader"]["resultCode"] != 0:
            logging.warning(f"Request ignored or result is unexpected: {json_data}")
            return

        parsed_buses = [self._parse_bus_data(bus_data, route_id, route_name) for bus_data in bus_locations]

        with self.lock:
            self.buses.extend(parsed_buses)

    def collect_data(self):
        self.clear_data()
        threads = []
        for route_id, route_name in self.route_ids:
            thread = threading.Thread(target=self.fetch_data, args=(route_id, route_name))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return self.buses
