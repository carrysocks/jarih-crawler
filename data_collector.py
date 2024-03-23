import requests
import xmljson
import xml.etree.ElementTree as ET
import datetime
import logging
import json

class DataCollector:
    def __init__(self, base_url, route_id, route_name, resource_path):
        self.base_url = base_url
        self.route_id = route_id
        self.route_name = route_name
        self.resource_path = resource_path

    def collect_data(self):
        with open(f"{self.resource_path}/route.json", "r") as f:
            route_map = json.load(f)

        with open(f"{self.resource_path}/station.json", "r") as f:
            station_map = json.load(f)

        url = self.base_url.format(self.route_id)
        response = requests.get(url)
        xml_str = response.text

        xml_element = ET.fromstring(xml_str)
        json_data = xmljson.parker.data(xml_element)

        if len(json_data) == 1 or json_data["msgHeader"]["resultCode"] != 0:
            logging.warning(f"Request ignored or result is unexpected: {json_data}")
            return []

        buses = []
        for data in json_data["msgBody"]["busLocationList"]:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            plate_no = data.get("plateNo")
            plate_type = data.get("plateType")
            remain_seat_cnt = data.get("remainSeatCnt", -1)
            station_id = data.get("stationId")
            station_name = station_map.get(str(station_id), "Unknown Station")
            station_seq = data.get("stationSeq")

            buses.append({
                "time": now,
                "plate_no": plate_no,
                "plate_type": plate_type,
                "route_id": self.route_id,
                "route_name": self.route_name,
                "remain_seat_cnt": remain_seat_cnt,
                "station_id": station_id,
                "station_name": station_name,
                "station_seq": station_seq
            })
        return buses
