import requests
import xmljson
import xml.etree.ElementTree as ET
import datetime
import logging
import json
import pytz

class DataCollector:
    def __init__(self, base_url, resources_path):
        self.base_url = base_url
        self.resource_path = resources_path
        self.kst_zone = pytz.timezone('Asia/Seoul')
        
        with open(f"{self.resource_path}/station.json", "r") as f:
            self.station_map = json.load(f)
        
        with open(f"{self.resource_path}/crawlering_route_ids.json", "r") as f:
            self.route_ids = json.load(f)

    def collect_data(self):
        buses = []
        for route_id, route_name in self.route_ids:
            print(route_id, route_name)
            url = self.base_url.format(route_id)
            response = requests.get(url)
            xml_str = response.text

            xml_element = ET.fromstring(xml_str)
            json_data = xmljson.parker.data(xml_element)
            
            # Check Data from external API
            
            if 'msgBody' not in json_data or 'busLocationList' not in json_data['msgBody']:
                logging.warning(f"No busLocationList found in the response for route_id {route_id}")
                continue  
            
            bus_locations = json_data["msgBody"]["busLocationList"]
            
            if not isinstance(bus_locations, list):
                logging.error(f"Unexpected busLocationList type for route_id {route_id}: {type(bus_locations)}")
                continue
            
            if len(json_data) == 1 or json_data["msgHeader"]["resultCode"] != 0:
                logging.warning(f"Request ignored or result is unexpected: {json_data}")
                continue

            for data in json_data["msgBody"]["busLocationList"]:
                time = datetime.datetime.now(pytz.utc).astimezone(self.kst_zone).strftime("%Y-%m-%d %H:%M:%S")
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
                    "route_id": route_id,
                    "route_name": route_name,
                    "remain_seat_cnt": remain_seat_cnt,
                    "station_id": station_id,
                    "station_name": station_name,
                    "station_seq": station_seq
                })
        return buses
