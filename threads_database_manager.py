import traceback

import psycopg2
from psycopg2 import extras


class ThreadsDatabaseManager:
    def __init__(self, dsn):
        self.dsn = dsn
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = psycopg2.connect(self.dsn)
        self.cursor = self.conn.cursor()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def save_data(self, buses):
        try:
            print("save1")
            self.connect()
            print("save2")
            insert_query = """
                        INSERT INTO bus_data (
                            time, plate_no, plate_type, route_id, route_name,
                            remain_seat_cnt, station_id, station_name, station_seq
                        ) VALUES %s
                    """
            data = [(
                bus['time'], bus['plate_no'], bus['plate_type'], bus['route_id'],
                bus['route_name'], bus['remain_seat_cnt'], bus['station_id'], bus['station_name'],
                bus['station_seq']
            ) for bus in buses]
            extras.execute_values(self.cursor, insert_query, data)
            self.conn.commit()
            print(f"Saved {len(buses)} bus data entries to the database.")
        except (psycopg2.Error, Exception) as e:
            self.conn.rollback()
            print(f"Error while saving data to the database: {e}")
            traceback.print_exc()
        finally:
            self.close()